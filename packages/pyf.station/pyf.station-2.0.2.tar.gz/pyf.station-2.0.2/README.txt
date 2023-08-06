Introduction
============

PyF.Station is a protocol with client and server to transfer python generators accross tcp networks. Items in the generator must be pyf.transport.Packet instances.

Best practice is to provide information about the flow in the first packet, identified as an header (containing for example authentication data, method, target, and so on).

Errors are passed on both ends.

Server
------

Please note that the server requires tgscheduler (to spawn tasks, passing generators) and twisted.

An example::

    from twisted.internet import reactor
    from pyf.station import FlowServer

    def sample_handler(flow, client=None):
        header = flow.next()
        print header
        for i, item in enumerate(flow):
            if not i%50:
                print i, item
        print "end of flow..."
        client.success("Done")

    factory = FlowServer(sample_handler)
    reactor.listenTCP(8000,factory)
    reactor.run()

The handler can be a simple callable, as in the example above, or a user defined class:

    from twisted.internet import reactor
    from pyf.station import FlowServer

    class SampleHandler(object):

        def __init__(self, flow, client):
            # The __init__ method must accept 'flow' and 'client' params
            self.flow = flow
            self.client = client

        def handle_data(self):
            # This method will be called by the FlowServer
            header = self.flow.next()
            print header 
            for i, item in enumerate(self.flow):
                if not i%50:
                   print i, item
            print "end of flow..."
            self.client.success("Done")
        
    factory = FlowServer(SampleHandler)
    reactor.listenTCP(8000,factory)
    reactor.run()

Another example, if you are in an already threaded env (like a wsgi server)::

    from tgscheduler import scheduler
    from twisted.internet import reactor
    from pyf.station import FlowServer
    from pyf.transport import Packet

    def sample_handler(flow, client=None):
        header = flow.next()
        print header

        for i, item in enumerate(flow):
            # every 50 items...
            if not i%50:
                print i, item
                # we send a message to the client
                client.message(Packet({'type': 'info',
                                       'message': 'hello ! (%s)' % i}))

        print "end of flow..."
        client.success("Done")        

    factory = FlowServer(sample_handler)
    reactor.listenTCP(8000,factory)
    scheduler.add_single_task(reactor.run,
                              kw=dict(installSignalHandlers=0),
                              initialdelay=0)

    # You cloud comment these lines if you were in wsgi application
    scheduler.start_scheduler() 
    while True:
        pass

Client
------

Example of client::
        
    from pyf.station import StationClient
    from pyf.transport import Packet

    client = StationClient('127.0.0.1', 8000, True)

    def message_handler(message_packet):
        # the handler for messages that come back from the server
        print "Message handler triggered: %s" % message_packet
    
    # we register our callback
    client.add_listener('message_received', message_handler)
    
    # we generate sample packets
    flow = (Packet(dict(Field1=i+1,
                        Field2=('titi', 'tata')[i%2], num=i+1,
                        Field3=(i+1)*10))
            for i in range(10000))

    values = client.call(
         flow,
         header=dict(authtkt='my false auth token :)',
                     action='my_action'))
    # here values is either "True" (saying that message has passed well) or a packet, comming back from the server.
    for i, value in enumerate(values):
        if not i % 5000:
            print i

        if isinstance(value, Packet):
            print value
