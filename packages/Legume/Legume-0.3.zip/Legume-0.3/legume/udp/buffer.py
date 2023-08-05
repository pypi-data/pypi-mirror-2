# legume. Copyright 2009 Dale Reidy. All rights reserved.
# See LICENSE for details.

__docformat__ = 'restructuredtext'

'''
The job of the buffer is to manage the flow of messages in and out through
the socket.

It appends a message number to any messages due to be sent which is read
by the buffer instance at the other end of the connection for the purposes
of managing in-order and reliable packet tranmission and acknowledgement.
'''
import time
import struct
import logging
import random

from legume.bitfield import bitfield
from legume.bytebuffer import ByteBuffer
from legume.udp import messages

# Simulated connection loss (%)
CONNECTION_LOSS = 0

class OutgoingMessage(object):
    def __init__(self, message_id, message_bytes, require_ack):
        self.message_id = message_id
        self.message_bytes = message_bytes
        self.require_ack = require_ack

        '''
        If this message requires an ack this timestamp will
        either be None (not yet sent), or a value obtained
        from time.time() indicating when the message was last sent.
        The EndpointBuffer will not send a packet until 2xRTT ms
        has elapsed between send attempts.
        '''
        self.last_send_attempt_timestamp = None

    @property
    def length(self):
        return len(self.message_bytes)


class EndpointBuffer(object):
    '''
    A two-way buffer.

    An MTU of 1400 bytes is set for the maximum payload of a UDP packet
    that can be sent by the buffer. Currently a message cannot span over
    multiple UDP packets and a MessageError will be raised.
    '''

    MTU = 1400
    MESSAGE_TRANSPORT_HEADER = 'HHB'
    RECENT_MESSAGE_LIST_SIZE = 1000

    _log = logging.getLogger('legume.EndpointBuffer')

    def __init__(self, message_factory):

        self.message_factory = message_factory

        # Packet instances to be processed go in here
        self._incoming_messages = []

        # Packet strings to be sent go in here
        self._outgoing = []

        # In-order packet instances that have arrived early
        self._incoming_out_of_sequence_messages = []

        self._incoming_ordered_sequence_number = 0
        self._outgoing_ordered_sequence_number = 1
        self._outgoing_message_id = 0
        self._recent_message_ids = []

        '''
        Default transport latency is high - This prevents spamming
        of the network prior to obtaining a calculated latency.
        '''
        self._transport_latency = 0.3 # 0.1 = 100ms


    # ------------- Public Methods -------------


    def setLatency(self, latency):
        assert latency >= 0
        self._transport_latency = latency


    def processMessageAck(self, message_id):
        for m in self._outgoing:
            if m.message_id == message_id:
                self._outgoing.remove(m)
                return

        self._log.warning('Got duplicate ACK for packet. message_id=%s' % (
            message_id))


    def parsePacket(self, packet_bytes):
        '''
        Parse a raw udp packet and return a list of parsed messages.
        '''

        byte_buffer = ByteBuffer(packet_bytes)
        parsed_messages = []

        while not byte_buffer.isEmpty():

            message_id, sequence_number, message_flags = \
                byte_buffer.readStruct(self.MESSAGE_TRANSPORT_HEADER)

            message_type_id = messages.BaseMessage.readHeaderFromByteBuffer(
                byte_buffer)[0]
            message = self.message_factory.getById(message_type_id)()
            message.readFromByteBuffer(byte_buffer)

            # - These flags are for consumption by .update()
            message_flags_bf = bitfield(message_flags)
            message.is_reliable = message_flags_bf[1]
            message.is_ordered = message_flags_bf[0]

            message.sequence_number = sequence_number
            message.message_id = message_id

            parsed_messages.append(message)

        return parsed_messages


    def processInboundPacket(self, packet_bytes):
        '''
        Pass raw udp packet data to this method.
        Returns the number of packets parsed and inserted into
        the .incoming list.
        '''
        self._log.debug('%d bytes of packet_bytes read' % len(packet_bytes))
        messages_to_read = self.parsePacket(packet_bytes)

        for message in messages_to_read:
            if not message.message_id in self._recent_message_ids:
                if message.is_ordered:
                    if self._canReadInOrderMessage(seqNum):
                        self._insertMessage(message)
                    else:
                        self._holdMessage(message)
                else:
                    self._insertMessage(message)

        return len(messages_to_read)


    def sendMessage(self, message, ordered=False, reliable=False):
        '''
        Send a message and specify any options for the send method used.
        A message sent inOrder is implicitly sent as reliable.
        message is an instance of a subclass of packets.BasePacket.
        '''
        message_id = self._getNewOutgoingMessageNumber()
        if ordered:
            inorder_sequence_number = self._getNewOutgoingInOrderSequenceNumber()
        else:
            inorder_sequence_number = 0

        packet_flags = bitfield()
        packet_flags[0] = int(ordered)
        packet_flags[1] = int(reliable)

        message_transport_header = self._getMessageTransportHeader(
            message_id, inorder_sequence_number, packet_flags)

        message_bytes = message.getPacketBytes()

        self._addMessageBytesToOutputList(
            message_id,
            message_transport_header+message_bytes,
            ordered or reliable)

        self._log.debug('Packet data length = %s' % len(message_bytes))
        self._log.debug('Header length = %s' % len(message_transport_header))
        self._log.debug('Added %d byte %s packet in outgoing buffer' %
            (len(message_transport_header)+
             len(message_bytes), message.__class__.__name__))


    def sendReliableMessage(self, message):
        '''
        Send a message that is guaranteed to be delivered.
        message is an instance of a subclass of packets.BasePacket
        '''
        self.sendMessage(message, False, True)


    def sendInOrderMessage(self, message):
        '''
        Send a message in the in-order channel. Any packets sent in-order will
        arrive in the order they were sent.
        message is an instance of a subclass of packets.BasePacket
        '''
        self.sendMessage(message, True)


    def hasOutgoingPackets(self):
        '''
        Returns whether this buffer has any packets waiting to be sent.
        '''
        return len(self._outgoing) > 0


    def update(self, sock, address):
        '''
        Update this buffer by sending any messages in the output lists
        and read any messages which have been insert into the inputBuffer
        via the processInboundPacket call.

        Returns a list of message instances of messages that were read.
        '''
        read_packets = self._doRead()
        self._truncateRecentMessageList()
        self._doWrite(sock, address)

        return read_packets


    # ------------- Private Methods -------------


    def _addMessageBytesToOutputList(self, message_id,
                                     message_bytes, require_ack=False):
        if len(message_bytes) > self.MTU:
            raise BufferError, 'Packet is too large. size=%s, mtu=%s' % (
                len(message_bytes), self.MTU)
        else:
            self._outgoing.append(
                OutgoingMessage(message_id, message_bytes, require_ack))


    def _canReadInOrderMessage(self, sequence_number):
        '''
        Can the in-order message with the specified sequence number be
        insert into the .incoming list for processing?
        '''
        return self._incoming_ordered_sequence_number == (sequence_number+1)


    def _createPacket(self):
        packet_size = 0
        packet_bytes = ""

        sent_messages = []

        self._log.debug('%d packets pending' % len(self._outgoing))

        for message in self._outgoing:

            if message.require_ack:
                if message.last_send_attempt_timestamp is not None:
                    if ((message.last_send_attempt_timestamp +
                      self._transport_latency) > time.time()):
                        self._log.debug('Requires ack cant send yet')
                        continue

            if packet_size + message.length <= self.MTU:
                self._log.debug('Added data message into UDP packet')
                packet_size += message.length
                packet_bytes += message.message_bytes
                message.last_send_attempt_timestamp = time.time()
                sent_messages.append(message)
            else:
                self._log.debug(
                    'Message too fat, maybe he\'ll get on the next bus')

        for sent_message in sent_messages:
            # Packets that require an ack are only removed
            # from the outgoing list if an ack is received.
            if not sent_message.require_ack:
                self._log.info('Message %d doesnt require ack - removing' %
                    sent_message.message_id)
                self._outgoing.remove(sent_message)
            else:
                self._log.info(
                    'Message %d requires ack - waiting for response' %
                    sent_message.message_id)

        return packet_bytes


    def _doRead(self):
        unheld_messages = []
        for held_message in self._incoming_out_of_sequence_messages:

            if self._canReadInOrderMessage(held_message.sequence_number):
                unheld_messages.append(held_message)

                self._incoming_inorder_sequence_number = message.sequence_number
                self._incoming_messages.append(held_message)

        for unheld_message in unheld_messages:
            self._incoming_out_of_sequence_messages.remove(unheld_message)

        for message in self._incoming_messages:
            self._log.debug('Incoming message:')
            self._log.debug('IsInOrder: %d' % message.is_ordered)
            self._log.debug('IsReliable:%d' % message.is_reliable)
            self._log.debug('MessageID :%d' % message.message_id)
            if message.is_ordered or message.is_reliable:
                ack_message = messages.MessageAck()
                ack_message.message_to_ack.value = message.message_id
                self.sendMessage(ack_message)
                self._log.info(
                  'Informing of reciept of message %d' % message.message_id)

        read_messages = self._incoming_messages
        self._incoming_messages = []

        return read_messages


    def _doWrite(self, sock, address):
        while True:
            packet = self._createPacket()
            if not packet:
                break

            if CONNECTION_LOSS > 0:
                if random.randint(1, 100) > CONNECTION_LOSS:
                    bytes_sent = sock.sendto(packet, 0, address)
                else:
                    self._log.info('CONNECTION_LOSS override')
            else:
                bytes_sent = sock.sendto(packet, 0, address)

            self._log.info('Sent UDP packet %d bytes in length' % len(packet))


    def _getMessageTransportHeader(self, message_id,
                                   sequence_number, message_flags):
        return struct.pack(
            '!'+self.MESSAGE_TRANSPORT_HEADER,
            message_id, sequence_number, int(message_flags))


    def _getNewOutgoingInOrderSequenceNumber(self):
        self._outgoing_ordered_sequence_number += 1
        return self._outgoing_ordered_sequence_number


    def _getNewOutgoingMessageNumber(self):
        '''
        Returns a message ID for the next outgoing message. The
        outgoingMessageID attribute contains the ID returned
        by the last call to this method.
        '''
        self._outgoing_message_id += 1
        return self._outgoing_message_id


    def _holdMessage(self, message):
        self._incoming_out_of_sequence_messages.append(message)
        self._recent_message_ids.append(message.message_id)


    def _insertMessage(self, message):
        self._incoming_messages.append(message)
        self._recent_message_ids.append(message.message_id)
        if message.is_ordered:
            self._incoming_ordered_sequence_number = message.sequence_number


    def _truncateRecentMessageList(self):
        '''
        Ensures that the recentMessageIDs list length is kept below
        MAX_RECENT_PACKET_LIST_SIZE. This method is called as part of this class'
        update method.
        '''
        if len(self._recent_message_ids) > self.RECENT_MESSAGE_LIST_SIZE:
            self._recent_message_ids = \
                self._recent_message_ids[-self.RECENT_MESSAGE_LIST_SIZE:]
