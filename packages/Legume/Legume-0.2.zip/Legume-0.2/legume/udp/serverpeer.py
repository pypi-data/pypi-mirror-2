# legume. Copyright 2009 Dale Reidy. All rights reserved.
# See LICENSE for details.

__docformat__ = 'restructuredtext'

import buffer
import logging
import time
import netshared
import connection
from legume.nevent import Event

LOG = logging.getLogger('legume.peer')

class Peer(object):
    '''
    A connection to the server. Each Client connection to the
    server has a separate instance.
    '''
    def __init__(self, parent, address, packetFactory):
        self.connectionEstablished = False
        self.parent = parent
        self._socket = parent.socket
        self._address = address
        self.packetFactory = packetFactory
        self.lastDataRecvdAt = time.time()
        self.pendingDisconnect = False

        self.OnConnectRequest = Event()
        self.OnDisconnect = Event()
        self.OnError = Event()
        self.OnMessage = Event()

        self._connection = connection.Connection(self)
        self._connection.OnMessage += self._Connection_OnMessage
        self._connection.OnDisconnect += self._Connection_OnDisconnect
        self._connection.OnError += self._Connection_OnError
        self._connection.OnConnectRequest += self._Connection_OnConnectRequest

    @property
    def isserver(self):
        return True

    def _Connection_OnMessage(self, sender, event_args):
        if not self.connectionEstablished:
            self.pendingDisconnect = True
        else:
            self.OnMessage(self, event_args)

    def _Connection_OnConnectRequest(self, sender, event_args):
        self.connectionEstablished = self.OnConnectRequest(self, event_args)
        if self.connectionEstablished is None:
            # No event handler bound, default action is to accept connection.
            self.connectionEstablished = True
        return self.connectionEstablished

    def _Connection_OnError(self, sender, error_string):
        self.OnError(self, error_string)

    def _Connection_OnDisconnect(self, sender, event_args):
        self.OnDisconnect(self, sender)

    def getLastPacketSentAt(self):
        return self._connection.lastPacketSentAt
    lastPacketSentAt = property(getLastPacketSentAt)

    @property
    def latency(self):
        return self._connection.latency

    def getAddress(self):
        return self._address
    address = property(getAddress)

    def getTimeout(self):
        return self.parent.timeout
    timeout = property(getTimeout)

    def doRead(self, callback):
        self.parent.doRead(callback)

    def insertRawUDPPacket(self, rawData):
        self._connection.insertRawUDPPacket(rawData)

    def hasPacketsToSend(self):
        return self._connection.hasOutgoingPackets()

    def sendPacket(self, packet):
        '''
        Adds a packet to the outgoing buffer to be sent to the client.
        This does not set the in-order or reliable flags.

        packet is an instance of BasePacket.
        '''
        if self.pendingDisconnect:
            raise netshared.ServerError, \
                'Cannot sendPacket to a disconnecting peer'
        self._connection.sendPacket(packet)

    def sendReliablePacket(self, packet):
        if self.pendingDisconnect:
            raise netshared.ServerError, \
                'Cannot sendReliablePacket to a disconnecting peer'
        self._connection.sendReliablePacket(packet)

    def disconnect(self):
        '''
        Disconnect this peer. A Disconnected packet will be sent to the client
        and this peer object will be deleted once the outgoing buffer for
        this connection has emptied.
        '''
        LOG.info('Sent Disconnected packet to client')
        self._connection.sendPacket(
            self.packetFactory.getByName('Disconnected')())
        self.pendingDisconnect = True

    def update(self):
        self._connection.update()
