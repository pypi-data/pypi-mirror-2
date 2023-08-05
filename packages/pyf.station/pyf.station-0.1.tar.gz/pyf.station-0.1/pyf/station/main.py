from twisted.internet.protocol import ServerFactory, Factory, Protocol
from twisted.protocols import basic
from twisted.internet import reactor, defer
from simplejson import loads
from pyf.transport.packets import encode_packet_flow
import Queue

from tgscheduler import scheduler
from pyf.transport import decode_packet_flow, Packet

class BadFlowEnding(Exception):
    pass

class ServerError(Exception):
    pass

class PacketGeneratorAdapter(object):
    def __init__(self, generator):
        self.generator = iter(generator)
        self.inited = False
    
    def __iter__(self):
        return self
    
    def next(self):
        if self.inited:
            return self.adapted_generator.next()
        
        else:
            self.header_str = self.generator.next()
            self.header = Packet(data=loads(self.header_str),
                                 data_type="serialized")
            
            self.adapted_generator = decode_packet_flow(self.generator,
                                        decompress=self.header.get('compressed',
                                                                   False),
                                        pure_flow=True)
            self.inited = True
            return self.header        

class GeneratorAdapter(object):
    def __init__(self, client):
        self.client = client
        
    def __iter__(self):
        queue = self.client.data_queue
        i = 0
        while True:
            if self.client.data_queue.empty() and self.client.data_queue.finished:
                if self.client.data_queue.complete:
                    raise StopIteration
                else:
                    raise BadFlowEnding, \
                          'Bad ending in flow. Corrupted connection ?'
            item = queue.get()
            yield item
            i += 1
    
class FlowReceiver(basic.LineReceiver):
    delimiter='\r\n\0'
    
class DataFlowQueue(Queue.Queue):
    def __init__(self, *args, **kwargs):
        Queue.Queue.__init__(self, *args, **kwargs)
        self.finished = False
        self.complete = False

class FlowProtocol(FlowReceiver):
    go = Packet(dict(message='go', type='control'))
    nogo = Packet(dict(message='nogo',
                       type='control',
                       detail='error in initialization'))
    good = "good."
    ok = Packet(dict(message='ok', type='info'))
    
    def lineReceived(self, line):
        
        if line == self.good:
            self.data_queue.finished = True
            self.data_queue.complete = True
        else:
            self.data_queue.put(line)
#            self.message(self.ok)

    def message(self, message):
        if isinstance(message, Packet):
            for v in encode_packet_flow([message], separator=self.delimiter):
                self.transport.write(v)
        else:
            self.transport.write(message + self.delimiter)
        
    def connectionMade(self):
        try:
            self.factory.numProtocols = self.factory.numProtocols+1
            self.factory.clients.append(self)
            self.data_queue = DataFlowQueue(maxsize=self.factory.max_items)
            
            if self.factory.numProtocols > self.factory.max_clients:
                self.error(ServerError('Too many connections. Try again later.'))
            else:   
                flow = PacketGeneratorAdapter(GeneratorAdapter(self))
                scheduler.add_single_task(self.factory.data_handler,
                                          kw=dict(flow=flow,
                                                  client=self),
                                          initialdelay=0)
                self.message(self.go)
        except Exception, e:
            self.transport.loseConnection()
            raise e

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        self.factory.numProtocols = self.factory.numProtocols-1
        self.data_queue.finished = True
        
    def error(self, error):
        self.message(Packet(dict(type='error',
                                 message=str(error),
                                 error_type=type(error).__name__)))
        self.transport.loseConnection()
    
    def success(self, message):
        self.message(Packet(dict(type='success', message=message)))
        self.transport.loseConnection()
        
        
class FlowServer(ServerFactory):
    protocol = FlowProtocol
    
    def __init__(self, data_handler, max_items=1000, max_clients=100):
        self.max_items = max_items
        self.max_clients = max_clients
        self.data_handler = data_handler
        self.numProtocols = 0
        self.clients = list()

def launch_server():
    """This runs the protocol on port 8000"""
    scheduler.start_scheduler()
    
    def toto_plouf(flow, client=None):
        for i, item in enumerate(flow):
            if not i%50:
                print item.num
            
        print "end of flow..."
    
    factory = FlowServer(toto_plouf)
    reactor.listenTCP(8000,factory)
    scheduler.add_single_task(reactor.run,
                              kw=dict(installSignalHandlers=0),
                              initialdelay=0)
    while True:
        pass

# this only runs if the module was *not* imported
if __name__ == '__main__':
    launch_server()