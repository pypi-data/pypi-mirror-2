# legume. Copyright 2009 Dale Reidy. All rights reserved.
# See LICENSE for details.

'''
    A `Client` manages the connection to a `Server` instance elsewhere.
	Creating an instance of a `Client` and connecting to a server is done
	as shown in the minimalist example below::

        client = Client()
        # Server is running on localhost port 9000
        client.connect(('localhost', 9000))

        # This loop ensures that .update() is called.
        while True:
            client.update()
            # Add a small time delay to prevent pegging the CPU.
            time.sleep(0.0001)

    The `Client` has a number of events that can be hooked into that provide
    notifications of data sent from the server and state changes. An event
    consists of the sender and the argument(in the example below, this
    is the packet), eg::

        def my_message_handler(sender, packet):
            print "The greeting reads: %s" % packet.greeting.value

        my_client.OnMessage += my_message_handler

    For the `Client.OnMessage` handler example above the argument part of the
    event received is a re-assembled instance of the message that was sent, and
    the greeting field in the message is obtained via
    the fields `value` attribute.

    * `Client.OnConnectRequestAccepted` - Fired when a `Client.connect` request
        has been responded to by the server allowing the connection.
    * `Client.OnConnectRequestRejected` - Fired when a `Client.connect` request
        has been responded to by the server deneying the connection.
    * `Client.OnMessage` - Fired when a message is receieved from the server.
        See above example.
    * `Client.OnError` - An error has occured. The event argument is a string
        detailing the error.
    * `Client.OnDisconnect` - The connection was gracefully closed by the
        Server. If the connection was severed due to a time-out, the
        `Client.OnError` event would fire.

'''

__docformat__ = 'restructuredtext'

import packets
import netshared
import connection
import logging
from legume.nevent import Event, NEventError

LOG = logging.getLogger('legume.client')

class ClientError(Exception): pass

class Client(netshared.NetworkEndpoint):

    def __init__(self, packetFactory=packets.packetFactory):
        '''
        Create a Client endpoint. A Client is initially in the closed state
        until a call to `connect`.

        A packet factory is required to assemble and disassemble packets for
        pushing down the intertubes to the server endpoint. If a
        packetFactory is not explicitly specified then the global
        packetFactory will be used.

        :Parameters:
            packetFactory : `PacketFactory`
                A packet factory.

        '''
        netshared.NetworkEndpoint.__init__(self, packetFactory)
        #self.isserver = False
        self._address = None
        self._connection = None
        self._disconnecting = False

        self._OnConnectRequestRejected = Event()
        self._OnMessage = Event()
        self._OnConnectRequestAccepted = Event()
        self._OnError = Event()
        self._OnDisconnect = Event()

    @property
    def isserver(self):
        return False

    @property
    def latency(self):
        return self._connection.pingMeter.get_ping()

    def _getOnConnectRequestRejected(self):
        return self._OnConnectRequestRejected
    def _setOnConnectRequestRejected(self, event):
        if isinstance(event, Event):
            self._OnConnectRequestRejected = event
        else:
            raise NEventError, 'Event must subclass nevent.Event'
    OnConnectRequestRejected = property(
        _getOnConnectRequestRejected, _setOnConnectRequestRejected)

    def _getOnMessage(self):
        return self._OnMessage
    def _setOnMessage(self, event):
        if isinstance(event, Event):
            self._OnMessage = event
        else:
            raise NEventError, 'Event must subclass nevent.Event'
    OnMessage = property(
        _getOnMessage, _setOnMessage)

    def _getOnConnectRequestAccepted(self):
        return self._OnConnectRequestAccepted
    def _setOnConnectRequestAccepted(self, event):
        if isinstance(event, Event):
            self._OnConnectRequestAccepted = event
        else:
            raise NEventError, 'Event must subclass nevent.Event'
    OnConnectRequestAccepted = property(
        _getOnConnectRequestAccepted, _setOnConnectRequestAccepted)

    def _getOnError(self):
        return self._OnError
    def _setOnError(self, event):
        if isinstance(event, Event):
            self._OnError = event
        else:
            raise NEventError, 'Event must subclass nevent.Event'
    OnError = property(
        _getOnError, _setOnError)

    def _getOnDisconnect(self):
        return self._OnDisconnect
    def _setOnDisconnect(self, event):
        if isinstance(event, Event):
            self._OnDisconnect = event
        else:
            raise NEventError, 'Event must subclass nevent.Event'
    OnDisconnect = property(
        _getOnDisconnect, _setOnDisconnect)


    def _Connection_OnConnectRequestRejected(self, sender, event_args):
        self._state = self.ERRORED
        self._shutdownSocket()
        self.OnConnectRequestRejected(self, event_args)

    def _Connection_OnMessage(self, sender, message):
        self.OnMessage(self, message)

    def _Connection_OnConnectRequestAccepted(self, sender, event_args):
        self._state = self.CONNECTED
        self.OnConnectRequestAccepted(self, event_args)

    def _Connection_OnError(self, sender, error_string):
        self._state = self.ERRORED
        self._shutdownSocket()
        self.OnError(self, error_string)

    def _Connection_OnDisconnect(self, sender, event_args):
        self._disconnect()

    def connect(self, address):
        '''
        Initiate a connection to the server at the specified address.

        This method will put the socket into the `CONNECTING` state. If a
        connection is already established a ClientError exception is raised.

        :Parameters:
            address : (host, port)
                Host address
        '''
        if self.isActive():
            raise ClientError(
                'Client cannot reconnect in a CONNECTING or CONNECTED state')
        if not netshared.isValidPort(address[1]):
            raise ClientError(
                '%s is not a valid port' % str(address[1]))
        self._socket = self.createSocket()
        self.connectSocket(address)
        self._address = address

        self._connection = connection.Connection(self)

        self._connection.OnConnectRequestAccepted += \
            self._Connection_OnConnectRequestAccepted
        self._connection.OnConnectRequestRejected += \
            self._Connection_OnConnectRequestRejected
        self._connection.OnError += self._Connection_OnError
        self._connection.OnDisconnect += self._Connection_OnDisconnect
        self._connection.OnMessage += self._Connection_OnMessage

        request_packet = packets.packets['ConnectRequest']()
        request_packet.protocol.value = netshared.PROTOCOL_VERSION
        self._sendReliablePacket(request_packet)
        self._state = self.CONNECTING

    def disconnect(self):
        '''
        Gracefully disconnect from the host. A disconnection packet is
        sent to the server upon calling the .update() method.
        '''
        self._connection.sendPacket(
            self.packetFactory.getByName('Disconnected')())
        self._disconnecting = True

    @property
    def connected(self):
        '''
        Returns True if this endpoint's state is `CONNECTED`.
        '''
        return self._state == self.CONNECTED

    @property
    def errored(self):
        '''
        Returns True if this endpoint's state is `ERRORED`.
        '''
        return self._state == self.ERRORED

    @property
    def disconnected(self):
        '''
        Returns True if this endpoint's state is `DISCONNECTED`.
        '''
        return self._state == self.DISCONNECTED

    def _sendPacket(self, packet):
        self._connection.sendPacket(packet)

    def _sendReliablePacket(self, packet):
        self._connection.sendReliablePacket(packet)

    def sendReliablePacket(self, packet):
        '''
        Send a packet to the server with guaranteed delivery.

        :Parameters:
            packet : `BasePacket`
                The packet to be sent
        '''
        if self._state == self.CONNECTED:
            self._sendReliablePacket(packet)
        else:
            raise ClientError, 'Cannot send packet - not connected'

    def sendPacket(self, packet):
        '''
        Send a packet to the server. The packet is added to the output buffer.
        To flush the output buffer call the .update() method.

        :Parameters:
            packet : `BasePacket`
                The packet to be sent
        '''
        if self._state == self.CONNECTED:
            self._sendPacket(packet)
        else:
            raise ClientError, 'Cannot send packet - not connected'

    def _disconnect(self, raise_event=True):
        self._state = self.DISCONNECTED
        self._shutdownSocket()
        self._disconnecting = False
        if raise_event:
            self.OnDisconnect(self, None)

    def update(self):
        '''
        This method should be called frequently to process incoming and
        outgoing data.
        '''
        if self._state in [self.CONNECTING, self.CONNECTED]:
            self._connection.update()

        if self._disconnecting and not self._connection.hasOutgoingPackets():
            self._disconnect(raise_event=False)
