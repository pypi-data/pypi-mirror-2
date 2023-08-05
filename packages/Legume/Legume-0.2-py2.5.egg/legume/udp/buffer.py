# legume. Copyright 2009 Dale Reidy. All rights reserved.
# See LICENSE for details.

__docformat__ = 'restructuredtext'

'''
The job of the buffer is to manage the flow of messages in and out through
the socket.

It appends a message number to any packets due to be sent which is read
by the buffer instance at the other end of the connection for the purposes
of managing in-order and reliable packet tranmission and acknowledgement.
'''
import time
import struct
import logging
import random
from legume.bitfield import bitfield

from legume.udp import packets
from legume.udp.netshared import PacketDataError

# Simulated connection loss (%)
CONNECTION_LOSS = 0

LOG = logging.getLogger('legume.buffer')

class BufferError(Exception): pass

class BufferedOutgoingPacket(object):
    def __init__(self, packetId, packetString, requireAck):
        self.packetId = packetId
        self.packetString = packetString
        self.requireAck = requireAck

        '''
        If this packet requires an ack this timestamp will
        either be None (not yet sent), or a value obtained
        from time.time() indicating when the packet was last sent.
        The EndpointBuffer will not send a packet until 2xRTT ms
        has elapsed between send attempts.
        '''
        self.lastSendAttemptTimestamp = None

    def getLength(self):
        return len(self.packetString)
    length = property(getLength)


class ByteBuffer(object):
    '''
    Provides a simplified method of reading struct packed data from
    a string buffer.

    readBytes and readStruct remove the read data from the string buffer.
    '''
    def __init__(self, bytes):
        self.bytes = bytes

    def readBytes(self, numBytes):
        if numBytes > len(self.bytes):
            raise PacketDataError('Unable to read buffered data', e)
        result = self.bytes[:numBytes]
        self.bytes = self.bytes[numBytes:]
        return result

    def peekBytes(self, numBytes):
        if numBytes > len(self.bytes):
            raise PacketDataError('Unable to read buffered  data', e)
        return self.bytes[:numBytes]

    def pushBytes(self, bytes):
        self.bytes += bytes

    def readStruct(self, structFormat):
        structSize = struct.calcsize(structFormat)
        structBytes = self.readBytes(structSize)
        try:
            bytes = struct.unpack(structFormat, structBytes)
        except struct.error, e:
            raise PacketDataError('Unable to unpack data', e)
        return bytes

    def peekStruct(self, structFormat):
        structSize = struct.calcsize(structFormat)
        structBytes = self.peekBytes(structSize)
        try:
            bytes = struct.unpack(structFormat, structBytes)
        except struct.error, e:
            raise PacketDataError('Unable to unpack data', e)
        return bytes

    def isEmpty(self):
        return len(self.bytes) == 0


class EndpointBuffer(object):
    '''
    A two-way buffer for reading and writing UDP packets.

    An MTU of 1400 bytes is set for the maximum payload of a UDP packet
    that can be sent by the buffer. Currently a message cannot span over
    multiple UDP packets and a PacketError will be raised.
    '''

    MTU = 1400
    PACKETBUFFER_HEADER = 'HHB'
    MAX_RECENT_PACKET_LIST_SIZE = 1000

    def __init__(self, packetFactory):
        self.packetFactory = packetFactory

        # Packet instances to be processed go in here
        self.incomingPacketList = []

        # Packet strings to be sent go in here
        self.outgoing = []

        # In-order packet instances that have arrived early
        self.inOrderHeldPacketList = []

        self.incomingInOrderSequenceNumber = 0
        self.outgoingInOrderSequenceNumber = 1

        self.outgoingPacketID = 0

        self.recentPacketIDs = []

        '''
        Default transport latency is high - This prevents spamming
        of the network prior to obtaining a calculated latency.
        '''
        self._transport_latency = 0.3 # 0.1 = 100ms

    def set_latency(self, latency):
        assert latency >= 0
        self._transport_latency = latency

    def removePacketFromOutgoingList(self, packetId):
        for p in self.outgoing:
            if p.packetId == packetId:
                self.outgoing.remove(p)
                return

        LOG.warning('Got duplicate ACK for packet. packetid=%s' % (
            packetId))


    def truncateRecentPacketList(self):
        '''
        Ensures that the recent_packet_ids list length is kept below
        MAX_RECENT_PACKET_LIST_SIZE. This method is called as part of this class'
        update method.
        '''
        if len(self.recentPacketIDs) > self.MAX_RECENT_PACKET_LIST_SIZE:
            self.recentPacketIDs = \
                self.recentPacketIDs[-self.MAX_RECENT_PACKET_LIST_SIZE:]


    def _insertPacket(self, packet):
        self.incomingPacketList.append(packet)
        self.recentPacketIDs.append(packet.packetId)
        if packet.isInOrder:
            self.incomingInOrderSequenceNumber = packet.seqNum

    def _holdPacket(self, packet):
        self.inOrderHeldPacketList.append(packet)
        self.recentPacketIDs.append(packet.packetId)

    def insertRawUDPPacket(self, udpData):
        '''
        Pass raw udp packet data to this method.
        Returns the number of packets parsed and inserted into
        the .incoming list.
        '''
        packetsToRead = self.parseRawUDPPacket(udpData)

        for packet in packetsToRead:
            if not packet.packetId in self.recentPacketIDs:
                if packet.isInOrder:
                    if self._canReadInOrderPacket(seqNum):
                        self._insertPacket(packet)
                    else:
                        self._holdPacket(packet)
                else:
                    self._insertPacket(packet)

        return len(packetsToRead)

    def _canReadInOrderPacket(self, sequenceNumber):
        '''
        Can the in-order packet with the specified sequence number be
        insert into the .incoming list for processing?
        '''
        return self.incomingInOrderSequenceNumber == (sequenceNumber+1)

    def parseRawUDPPacket(self, udpData):
        '''
        Parse a raw udp packet and return a list of packetStrings
        that were parsed.
        '''

        udpDataBB = ByteBuffer(udpData)
        parsedPackets = []

        # While more udpData to read.
        while not udpDataBB.isEmpty():
            # - Read packet ID bytes.
            # - Read reliable transfer byte.
            # - Read in-order sequence number bytes.
            # - Read packet header bytes.

            packetFlags = bitfield()

            packetId, seqNum, packetFlags = \
                udpDataBB.readStruct(self.PACKETBUFFER_HEADER)

            packetFlagsBF = bitfield(packetFlags)

            # - Read packet type ID
            packetTypeID = packets.BasePacket.readHeaderFromByteBuffer(
                udpDataBB)[0]

            packetClass = self.packetFactory.getById(packetTypeID)

            packet = packetClass()
            # - Read packet data bytes.
            packet.loadFromByteBuffer(udpDataBB)

            # - These flags are for consumption by .update()
            packet.isReliable = packetFlagsBF[1]
            packet.isInOrder = packetFlagsBF[0]
            packet.seqNum = seqNum
            packet.packetId = packetId

            parsedPackets.append(packet)

        return parsedPackets

    def update(self, sock, address):
        '''
        Update this buffer by sending any packets in the output lists
        and read any packets which have been insert into the inputBuffer
        via the insertRawUDPPacket call.

        Returns a list of packet instances of packets that were read.
        '''
        read_packets = self._doRead()
        self.truncateRecentPacketList()
        self._doWrite(sock, address)

        return read_packets


    def _doRead(self):
        unhold = []
        for heldpacket in self.inOrderHeldPacketList:
            if self._canReadInOrderPacket(heldpacket.seqNum):
                unhold.append(heldpacket)
                self.incomingInOrderSequenceNumber = packet.seqNum
                self.incomingPacketList.append(heldpacket)
        for unheldpacket in unhold:
            self.inOrderHeldPacketList.remove(unheldpacket)

        for packet in self.incomingPacketList:
            if packet.isInOrder or packet.isReliable:
                ack_packet = packets.PacketAck()
                ack_packet.packetToAck.value = packet.packetId
                self.send(ack_packet)
                LOG.info('Informing of reciept of packet %d' % packet.packetId)


        readPackets = self.incomingPacketList
        self.incomingPacketList = []

        return readPackets


    def _doWrite(self, sock, address):
        udpPacket = self._createOutgoingUDPDatagram()
        if udpPacket != "":
            if CONNECTION_LOSS > 0:
                if random.randint(1, 100) > CONNECTION_LOSS:
                    bytes_sent = sock.sendto(udpPacket, 0, address)
                else:
                    LOG.info('CONNECTION_LOSS override')
            else:
                bytes_sent = sock.sendto(udpPacket, 0, address)

            LOG.info('Sent UDP packet %d bytes in length' % len(udpPacket))


    def _createOutgoingUDPDatagram(self):
        udpPacketSize = 0
        udpPacketString = ""

        sent_packets = []

        for packet in self.outgoing:

            if packet.requireAck:
                if packet.lastSendAttemptTimestamp is not None:
                    if ((packet.lastSendAttemptTimestamp +
                      self._transport_latency) > time.time()):
                        break

            if udpPacketSize + packet.length <= self.MTU:
                LOG.debug('Added data packet into UDP packet')
                udpPacketSize += packet.length
                udpPacketString += packet.packetString
                packet.lastSendAttemptTimestamp = time.time()
                sent_packets.append(packet)
            else:
                LOG.debug(
                    'Data packet too fat, maybe he\'ll get on the next bus')

        for sent_packet in sent_packets:
            # Packets that require an ack are only removed
            # from the outgoing list if an ack is received.
            if not sent_packet.requireAck:
                LOG.info('Packet %d doesnt require ack - removing' %
                    sent_packet.packetId)
                self.outgoing.remove(sent_packet)
            else:
                LOG.info(
                    'Packet %d requires ack - waiting for response' %
                    sent_packet.packetId)

        return udpPacketString


    def _getNewOutgoingPacketNumber(self):
        '''
        Returns a packet ID for the next outgoing packet. The
        outgoing_packet_id attribute contains the ID returned
        by the last call to this method.
        '''
        self.outgoingPacketID += 1
        return self.outgoingPacketID


    def _getNewOutgoingInOrderSequenceNumber(self):
        self.outgoingInOrderSequenceNumber += 1
        return self.outgoingInOrderSequenceNumber


    def _getNewPacketBufferHeader(
        self, packetId, seqNum, packetFlags):
        return struct.pack(
            self.PACKETBUFFER_HEADER,
            packetId, seqNum, packetFlags)


    def _addPacketStringToOutputList(self, packetId, packetString, requireAck=False):
        if len(packetString) > self.MTU:
            raise BufferError, 'Packet is too large. size=%s, mtu=%s' % (
                len(packetString), self.MTU)
        else:
            self.outgoing.append(
                BufferedOutgoingPacket(packetId, packetString, requireAck))


    def send(self, packet, inOrder=False, reliable=False):
        '''
        Send a packet and specify any options for the send method used.
        A packet sent inOrder is implicitly sent as reliable.
        packet is an instance of a subclass of packets.BasePacket.
        '''
        packetId = self._getNewOutgoingPacketNumber()
        if inOrder:
            inOrderSequenceNumber = self._getNewOutgoingInOrderSequenceNumber()
        else:
            inOrderSequenceNumber = 0

        packetFlags = bitfield()
        packetFlags[0] = int(inOrder)
        packetFlags[1] = int(reliable)

        packetBufferHeader = self._getNewPacketBufferHeader(
            packetId, inOrderSequenceNumber, packetFlags)

        packetString = packet.getPacketString()

        self._addPacketStringToOutputList(
            packetId,
            packetBufferHeader+packetString,
            inOrder or reliable)

        LOG.debug('Added %d byte packet in outgoing buffer' %
            (len(packetBufferHeader)+len(packetString)))


    def sendNormal(self, packet):
        '''
        Send a packet that may arrive out of order or be lost.
        packet is an instance of a subclass of packets.BasePacket
        '''
        self.send(packet)

    def sendReliable(self, packet):
        '''
        Send a packet that is guaranteed to be delivered.
        packet is an instance of a subclass of packets.BasePacket
        '''
        self.send(packet, False, True)

    def sendInOrder(self, packet):
        '''
        Send a packet in the in-order channel. Any packets sent in-order will
        arrive in the order they were sent.
        packet is an instance of a subclass of packets.BasePacket
        '''
        self.send(packet, True)

    def hasOutgoingPackets(self):
        '''
        Returns whether this buffer has any packets waiting to be sent.
        '''
        return len(self.outgoing) > 0
