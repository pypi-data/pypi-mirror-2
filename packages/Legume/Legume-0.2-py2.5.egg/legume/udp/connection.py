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

LOG = logging.getLogger('legume.connection')

PING_REQUEST_FREQUENCY = 2.0

class Connection(object):
    def __init__(self, parent):
        self.parent = parent
        self._buffer = buffer.EndpointBuffer(parent.packetFactory)
        self.lastDataRecvdAt = time.time()
        self.lastPacketSentAt = time.time()
        self._keepAliveSentAt = time.time()
        self._keepAlivePacketID = 0
        self._pingID = 0
        self._pingSentAt = time.time()
        self.pingMeter = PingSampler()

        self.OnConnectRequestAccepted = Event()
        self.OnConnectRequestRejected = Event()
        self.OnConnectRequest = Event()
        self.OnError = Event()
        self.OnMessage = Event()
        self.OnDisconnect = Event()

    @property
    def latency(self):
        return self.pingMeter.get_ping()

    def sendPacket(self, packet):
        self._buffer.send(packet)
        self.lastPacketSentAt = time.time()

    def sendReliablePacket(self, packet):
        self._buffer.sendReliable(packet)
        self.lastPacketSentAt = time.time()

    def _sendKeepAlive(self):
        self._keepAlivePacketID += 1
        if (self._keepAlivePacketID > netshared.USHRT_MAX):
            self._keepAlivePacketID = 0

        packet = self.parent.packetFactory.getByName('KeepAliveRequest')()
        packet.id.value = self._keepAlivePacketID

        self.sendPacket(packet)
        self._keepAliveSentAt = time.time()

    def _sendPing(self):
        self._pingID += 1
        if (self._pingID > netshared.USHRT_MAX):
            self._pingID = 0

        ping = self.parent.packetFactory.getByName('Ping')()
        ping.id.value = self._pingID
        self.sendPacket(ping)
        self._pingSentAt = time.time()

    def _sendPong(self, pingID):
        pong = self.parent.packetFactory.getByName('Pong')()
        pong.id.value = pingID
        self.sendPacket(pong)

    def insertRawUDPPacket(self, data):
        self._buffer.insertRawUDPPacket(data)

    def hasOutgoingPackets(self):
        return self._buffer.hasOutgoingPackets()

    def _onSocketData(self, data, addr):
        self.insertRawUDPPacket(data)

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

        if self.pingMeter.has_estimate():
            self._buffer.set_latency(self.pingMeter.get_ping())

        read_packets = self._buffer.update(
                        self.parent._socket, self.parent._address)

        if len(read_packets) != 0:
            self.lastDataRecvdAt = time.time()

        for packet in read_packets:

            if self.parent.packetFactory.isA(packet, 'ConnectRequestAccepted'):
                self.OnConnectRequestAccepted(self, None)

            elif self.parent.packetFactory.isA(packet,'ConnectRequestRejected'):
                self.OnConnectRequestRejected(self, None)

            elif self.parent.packetFactory.isA(packet, 'KeepAliveResponse'):

                if (packet.id.value == self._keepAlivePacketID):
                    self.pingMeter.add_sample(
                        (time.time()-self._keepAliveSentAt)*1000)
                else:
                    LOG.warning('Received old keep-alive, discarding')

            elif self.parent.packetFactory.isA(packet, 'KeepAliveRequest'):
                response = \
                    self.parent.packetFactory.getByName('KeepAliveResponse')()
                response.id.value = packet.id.value
                self.sendPacket(response)

            elif self.parent.packetFactory.isA(packet, 'Pong'):
                if (packet.id.value == self._pingID):
                    self.pingMeter.add_sample((time.time()-self._pingSentAt)*1000)
                else:
                    LOG.warning('Received old Pong, discarding')

            elif self.parent.packetFactory.isA(packet, 'Ping'):
                self._sendPong(packet.id.value)

            elif self.parent.packetFactory.isA(packet, 'Disconnected'):
                self.OnDisconnect(self, None)

            elif self.parent.packetFactory.isA(packet, 'PacketAck'):
                self._buffer.removePacketFromOutgoingList(
                    packet.packetToAck.value)

            elif self.parent.packetFactory.isA(packet, 'ConnectRequest'):
                # Unless the connection request is explicitly denied then
                # a connection is made - OnConnectRequest may return None
                # if no event handlers are bound.
                accept = True

                if (packet.protocol.value != netshared.PROTOCOL_VERSION):
                    LOG.warning('Invalid protocol version for client')
                    accept = False
                if self.OnConnectRequest(self.parent, packet) is False:
                    accept = False

                if accept:
                    response = self.parent.packetFactory.getByName(
                                'ConnectRequestAccepted')
                    self.sendReliablePacket(response())
                else:
                    response = self.parent.packetFactory.getByName(
                                'ConnectRequestRejected')
                    self.sendReliablePacket(response())
                    self.pendingDisconnect = True
            else:
                self.OnMessage(self, packet)


        if (time.time() > self._pingSentAt + PING_REQUEST_FREQUENCY):
            if self.parent.isserver:
                self._keepAliveSentAt = time.time()
            self._sendPing()


        if self.parent.isserver:
            # Server sends keep alive requests...
            if (time.time()-self._keepAliveSentAt)>(self.parent.timeout/2):
                self._sendKeepAlive()
            # though it will eventually give up...
            if (time.time()-self.lastDataRecvdAt)>(self.parent.timeout):
                self.OnError(self, 'Connection timed out')
        else:
            # ...Client waits for the connection to timeout
            if (time.time()-self.lastDataRecvdAt)>(self.parent.timeout):
                LOG.info('Connection has timed out')
                self.OnError(self, 'Connection timed out')
