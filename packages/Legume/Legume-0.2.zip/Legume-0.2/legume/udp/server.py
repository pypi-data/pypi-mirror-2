# legume. Copyright 2009 Dale Reidy. All rights reserved.
# See LICENSE for details.

__docformat__ = 'restructuredtext'

import logging
import netshared
import packets
import serverpeer
import time
from legume.nevent import Event

LOG = logging.getLogger('legume.server')

class Server(netshared.NetworkEndpoint):
    '''
    A server. To allow network clients to communicate with this class
    call listen() with a network address then periodically call update()
    to ensure data is kept flowing and connects/disconnects are handled.
    '''

    def __init__(self, packetFactory=packets.packetFactory):
        '''
        Create an instance of a new Server endpoint. Use the packetFactory
        parameter to specify an alternative to the global packets.packetFactory
        instance::

            pf = legume.udp.packets.PacketFactory()
            server = legume.udp.Server(packetFactory=pf)

        '''
        netshared.NetworkEndpoint.__init__(self, packetFactory)
        self._state = self.DISCONNECTED
        self._peers = {}
        self._dead_peers = [] # List of peers (by address) to be removed
        self._in_update = False

        self.OnConnectRequest = Event()
        self.OnDisconnect = Event()
        self.OnError = Event()
        self.OnMessage = Event()

    def listen(self, address):
        '''
        Begin listening for incoming connections.
        address is a tuple of the format (hostname, port)
        This method change the class state to LISTENING::

            # Begin listening on port 4000 on all IP interfaces
            server = legume.udp.Server()
            server.listen(('', 4000))
        '''
        if self.isActive():
            raise netshared.ServerError(
                'Server cannot listen whilst in a LISTENING state')
        self.createSocket()
        self.bindSocket(address)
        self._address = address
        self._state = self.LISTENING

    def _onSocketData(self, data, addr):
        LOG.debug(
            'Got data %s bytes in length from %s' %
            (str(len(data)), str(addr)))

        if not addr in self._peers:
            new_peer = serverpeer.Peer(self, addr, self.packetFactory)
            self._peers[addr] = new_peer

            new_peer.OnDisconnect += self._Peer_OnDisconnect
            new_peer.OnError += self._Peer_OnError
            new_peer.OnMessage += self._Peer_OnMessage
            new_peer.OnConnectRequest += self._Peer_OnConnectRequest

        self._peers[addr].insertRawUDPPacket(data)

    def _Peer_OnConnectRequest(self, peer, event_args):
        return self.OnConnectRequest(peer, event_args)

    def _Peer_OnError(self, peer, error_string):
        self._dead_peers.append(peer)
        self.OnError(peer, error_string)

    def _Peer_OnMessage(self, peer, message_packet):
        self.OnMessage(peer, message_packet)

    def _Peer_OnDisconnect(self, peer, event_args):
        self.OnDisconnect(peer, None)

    def update(self):
        '''
        Pumps buffers and dispatches events. Call regularly to ensure
        buffers do not overfill or connections time-out::

            server = legume.udp.Server()
            server.listen(('', 4000))

            while True:
                server.update()
                # Other update tasks here..
                time.sleep(0.001)

        '''

        self.doRead(self._onSocketData)

        for peer in self._peers.itervalues():
            peer.update()

            if peer.pendingDisconnect and not peer.hasPacketsToSend():
                self._dead_peers.append(peer)

        self._removePeers()


    def _removePeers(self):
        for dead_peer in self._dead_peers:
            del self._peers[dead_peer.address]
        self._dead_peers = []


    def getPeerByAddress(self, peer_address):
        '''
        Obtain a ServerPeer instance by specifying the peer's address
        '''
        return self._peers[peer_address]

    @property
    def peercount(self):
        '''
        Get count of connected peers
        '''
        return sum(
            1 for peer in self._peers.itervalues()
            if peer.connectionEstablished)

    @property
    def peers(self):
        '''
        Returns a list of peers
        '''
        return [
            peer for peer in self._peers.itervalues()
            if peer.connectionEstablished]


    def disconnect(self, peer_address):
        '''
        Disconnect a peer by specifying their address.
        Equivalent to::

            server.getPeerByAddress(peer_address).disconnect()

        '''
        self.getPeerByAddress(peer_address).disconnect()


    def disconnectAll(self):
        '''
        Disconnect all connected clients
        '''
        for peer in self._peers.itervalues():
            peer.disconnect()


    def sendPacketToAll(self, packet):
        '''
        Send a non-reliable packet to all connected peers.
        packet is an instance of a legume.packets.BasePacket subclass::

            msg_packet = ExamplePacket()
            msg_packet.chat_message.value = "Hello!"
            msg_packet.sender.value = "@X3"
            server.sendPacketToAll(msg_packet)

        '''
        for peer in self._peers.itervalues():
            peer.sendPacket(packet)


    def sendReliablePacketToAll(self, packet):
        '''
        Send a reliable packet to all connected peers. packet is an
        instance of a legume.udp.packets.BasePacket subclass.

        '''
        for peer in self._peers.itervalues():
            peer.sendReliablePacket(packet)
