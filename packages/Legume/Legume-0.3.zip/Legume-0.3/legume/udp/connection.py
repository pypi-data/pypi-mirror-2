# legume. Copyright 2009 Dale Reidy. All rights reserved.
# See LICENSE for details.

__docformat__ = 'restructuredtext'

import time
import buffer
import logging
import netshared
from legume.nevent import Event
from legume.pingsampler import PingSampler
import random

PING_REQUEST_FREQUENCY = 2.0

class Connection(object):

    _log = logging.getLogger('legume.Connection')

    def __init__(self, parent):

        self.parent = parent
        self._buffer = buffer.EndpointBuffer(parent.message_factory)
        self._last_receive_timestamp = time.time()
        self._last_send_timestamp = time.time()
        self._keep_alive_send_timestamp = time.time()
        self._keep_alive_message_id = 0
        self._ping_id = 0
        self._ping_send_timestamp = time.time()
        self._ping_meter = PingSampler()

        self.OnConnectRequestAccepted = Event()
        self.OnConnectRequestRejected = Event()
        self.OnConnectRequest = Event()
        self.OnError = Event()
        self.OnMessage = Event()
        self.OnDisconnect = Event()

    @property
    def latency(self):
        return self._ping_meter.get_ping()


    # ------------- Public Methods -------------

    def hasOutgoingPackets(self):
        return self._buffer.hasOutgoingPackets()


    def processInboundPacket(self, data):
        '''Processes a raw data packet. This method is normally called
        from

        '''
        self._buffer.processInboundPacket(data)


    def sendMessage(self, message):
        self._buffer.sendMessage(message)
        self._last_send_timestamp = time.time()


    def sendReliableMessage(self, message):
        self._buffer.sendReliableMessage(message)
        self._last_send_timestamp = time.time()


    def update(self):
        '''
        This method sends any packets that are in the output buffer and
        reads any packets that have been recieved.
        '''
        try:
            self.parent.doRead(self._onSocketData)
        except netshared.NetworkEndpointError, e:
            self.raiseOnError('Connection reset by peer')
            return

        if self._ping_meter.has_estimate():
            self._buffer.setLatency(self._ping_meter.get_ping())

        self._log.debug('buffer update for %s' % self.parent)
        read_messages = self._buffer.update(
                        self.parent._socket, self.parent._address)

        if len(read_messages) != 0:
            self._last_receive_timestamp = time.time()

        for message in read_messages:

            if self.parent.message_factory.isA(message,
                                               'ConnectRequestAccepted'):
                self.OnConnectRequestAccepted(self, None)

            elif self.parent.message_factory.isA(message,
                                                 'ConnectRequestRejected'):
                self.OnConnectRequestRejected(self, None)

            elif self.parent.message_factory.isA(message, 'KeepAliveResponse'):

                if (message.id.value == self._keep_alive_message_id):
                    self._ping_meter.add_sample(
                        (time.time()-self._keep_alive_send_timestamp)*1000)
                else:
                    self._log.warning('Received old keep-alive, discarding')

            elif self.parent.message_factory.isA(message, 'KeepAliveRequest'):
                response = \
                    self.parent.message_factory.getByName('KeepAliveResponse')()
                response.id.value = message.id.value
                self.sendMessage(response)

            elif self.parent.message_factory.isA(message, 'Pong'):
                if (message.id.value == self._ping_id):
                    self._ping_meter.add_sample(
                      (time.time()-self._ping_send_timestamp)*1000)
                else:
                    self._log.warning('Received old Pong, discarding')

            elif self.parent.message_factory.isA(message, 'Ping'):
                self._sendPong(message.id.value)

            elif self.parent.message_factory.isA(message, 'Disconnected'):
                self._log.debug('Received `Disconnected` message')
                self.OnDisconnect(self, None)

            elif self.parent.message_factory.isA(message, 'MessageAck'):
                self._buffer.processMessageAck(message.message_to_ack.value)

            elif self.parent.message_factory.isA(message, 'ConnectRequest'):
                # Unless the connection request is explicitly denied then
                # a connection is made - OnConnectRequest may return None
                # if no event handlers are bound.
                accept = True

                if (message.protocol.value != netshared.PROTOCOL_VERSION):
                    self._log.warning('Invalid protocol version for client')
                    accept = False
                if self.OnConnectRequest(self.parent, message) is False:
                    accept = False

                if accept:
                    response = self.parent.message_factory.getByName(
                                'ConnectRequestAccepted')
                    self.sendReliableMessage(response())
                else:
                    response = self.parent.message_factory.getByName(
                                'ConnectRequestRejected')
                    self.sendReliableMessage(response())
                    self.pendingDisconnect = True
            else:
                self.OnMessage(self, message)


        if (time.time() > self._ping_send_timestamp + PING_REQUEST_FREQUENCY):
            if self.parent.is_server:
                self._keep_alive_send_timestamp = time.time()
            self._sendPing()


        if self.parent.is_server:
            # Server sends keep alive requests...
            if ((time.time()-self._keep_alive_send_timestamp)>
               (self.parent.timeout/2)):
                self._sendKeepAlive()
            # though it will eventually give up...
            if (time.time()-self._last_receive_timestamp)>(self.parent.timeout):
                self.OnError(self, 'Connection timed out')
        else:
            # ...Client waits for the connection to timeout
            if (time.time()-self._last_receive_timestamp)>(self.parent.timeout):
                self._log.info('Connection has timed out')
                self.OnError(self, 'Connection timed out')


    # ------------- Private Methods -------------


    def _onSocketData(self, data, addr):
        self._buffer.processInboundPacket(data)


    def _sendKeepAlive(self):
        self._keep_alive_message_id += 1
        if (self._keep_alive_message_id > netshared.USHRT_MAX):
            self._keep_alive_message_id = 0

        message = self.parent.message_factory.getByName('KeepAliveRequest')()
        message.id.value = self._keep_alive_message_id

        self.sendMessage(message)
        self._keep_alive_send_timestamp = time.time()


    def _sendPing(self):
        self._ping_id += 1
        if (self._ping_id > netshared.USHRT_MAX):
            self._ping_id = 0

        ping = self.parent.message_factory.getByName('Ping')()
        ping.id.value = self._ping_id
        self.sendMessage(ping)
        self._ping_send_timestamp = time.time()


    def _sendPong(self, pingID):
        pong = self.parent.message_factory.getByName('Pong')()
        pong.id.value = pingID
        self.sendMessage(pong)

