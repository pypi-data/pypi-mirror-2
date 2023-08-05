# legume. Copyright 2009 Dale Reidy. All rights reserved.
# See LICENSE for details.

__docformat__ = 'restructuredtext'

'''

A message packet class is a subclass of legume.udp.packets.BasePacket with two
class attributes defined:

    * PacketTypeID - An integer uniquely identifying the packet type. The
        allowed range for application packets is 1 to BASE_PACKETID_SYSTEM-1.
    * PacketValues - A dictionary of the values stored within the packet where
        the key is the name of the packet value, and the value is the type.

Type names available for PacketValues:
    * 'int' - An integer
    * 'string n' - A string where n is the maximum string length, eg 'string 18'
    * 'float' - A double precision floating point.
    * 'bool' - A boolean (a 1 byte short)

An example packet definition::

    class ChatMessage(legume.udp.packets.BasePacket):
        PacketTypeID = 1
        PacketValues = {
            'sender_name':'string 24',
            'message':'string 256',
            'channel':'string 24'
            }

    # Adding a packet to a new packet_factory
    packet_factory = legume.udp.packets.PacketFactory()
    packet_factory.add(ChatMessage)

    # and/or add it to the global packet factory
    legume.udp.packets.packetFactory.add(ChatMessage)

How to use this packet definition::

    # Note how this client uses the packet_factory the
    # ChatMessage packet was added to.
    client = legume.udp.Client(packet_factory)

    # ..snip..

    # Create the packet
    cm = ChatMessage()
    cm.sender_name.value = 'JoeUser'
    cm.message.value = 'This is a test message.'
    cm.channel.value = 'newbies'

    # send the packet to the server
    client.sendPacket(cm)

'''

import sys
import struct
import string
from legume.udp.netshared import PROTOCOL_VERSION

class PacketError(Exception): pass

BASE_PACKETID_SYSTEM = 1
BASE_PACKETID_USER = 20

def isValidIdentifier(identifier):
    return not (' ' in identifier or identifier[0] not in string.ascii_letters)

class PacketValue(object):
    VALID_TYPE_NAMES = ['int', 'string', 'float', 'bool',
                        'uchar', 'char', 'short']

    def __init__(self, name, typename, value=None, maxLength=None, packet=None):
        '''
        Create a new packet type.

        The name parameter must be a valid python class attribute identifier.
        Typename can be one of 'int', 'string', 'float' or 'bool'.
        Value must be of the specified type.
        maxLength is only required for string values.

        '''

        if not isValidIdentifier(name):
            raise PacketError, '%s is not a valid name' % name

        self.name = name
        self.typename = typename
        self._value = value
        self.maxLength = maxLength # only required for string

        if self.maxLength is not None:
            self.maxLength = int(self.maxLength)

        if self.typename == 'string' and self.maxLength is None:
            raise PacketError, 'String value requires a maxLength attribute'
        elif self.maxLength is not None and self.maxLength < 1:
            raise PacketError, 'Max length must be None or > 0'
        elif self.typename not in self.VALID_TYPE_NAMES:
            raise PacketError, '%s is not a valid type name' % self.typename
        elif self.name == '':
            raise PacketError('A value name is required')

        if packet is not None and packet.UseDefaultValues:
            self.setDefaultValue()


    def setDefaultValue(self):
        if self.typename == 'int':
            self._value =0
        elif self.typename == 'short':
            self._value = 0
        elif self.typename == 'string':
            self._value = ""
        elif self.typename == 'float':
            self._value = 0.0
        elif self.typename == 'bool':
            self._value = False
        elif self.typename == 'uchar':
            self._value = ""
        else:
            raise PacketError, ('Cant set default value for type "%s"' %
                self.typename)

    def getValue(self):
        return self._value

    def setValue(self, value):
        if self.typename == 'string':
            if len(value) > self.maxLength:
                raise PacketError, 'String value is too long.'
            self._value = value.replace('\0', '')
        else:
            self._value = value

    value = property(getValue, setValue)

    def getFormatString(self):
        '''
        Returns the string necessary for encoding this value using struct.
        '''

        if self.typename == 'int':
            return 'i'
        elif self.typename == 'short':
            return 'H'
        elif self.typename == 'string':
            return str(self.maxLength) + 's'
        elif self.typename == 'float':
            return 'd'
        elif self.typename == 'bool':
            return 'b'
        elif self.typename == 'uchar':
            return 'B'
        else:
            raise PacketError, ('Cant get format string for type "%s"' %
                self.typename)

class BasePacket(object):
    '''
    Data packets must inherit from this base class. A subclass must have a
    static property called PacketTypeID set to a integer value to uniquely
    identify the packet within a single PacketFactory.
    '''

    HEADER_FORMAT = 'B'
    PacketTypeID = None
    PacketValues = None
    UseDefaultValues = True

    def __init__(self, *values):
        self._packet_type_id = self.PacketTypeID
        if self.PacketTypeID is None:
            raise PacketError('%s does not have a PacketTypeID' %
                self.__class__.__name__)

        self.valueNames = []

        if len(values) > 0:
            for value in values:
                self._addValue(value)
        elif self.PacketValues is not None:
            for pvname, pvtype in self.PacketValues.iteritems():
                if pvtype[:6] == 'string':
                    valuetype, param = pvtype.split(' ')
                else:
                    valuetype = pvtype
                    param = None
                new_value = PacketValue(pvname, valuetype, None, param, self)
                self._addValue(new_value)

        self.loadDefaultValues()

    def _addValue(self, value):
        self.valueNames.append(value.name)
        self.__dict__[value.name] = value

    def getHeaderFormat(self):
        '''
        Returns the header format as a struct compatible string.
        '''
        return self.HEADER_FORMAT

    def getHeaderValues(self):
        '''
        Returns a list containing the values used to construct
        the packet header.
        '''
        return [self._packet_type_id]

    def getDataFormat(self):
        '''
        Returns a struct compatible format string of the packet data
        '''
        format = []
        for valuename in self.valueNames:
            value = self.__dict__[valuename]
            if not isinstance(value, PacketValue):
                raise PacketError(
                    'Overwritten message value! Use msgval.value = xyz')
            format.append(value.getFormatString())
        return ''.join(format)

    def getPacketValues(self):
        '''
        Returns a list containing the header+packet values used
        to construct the packet
        '''
        values = self.getHeaderValues()
        for name in self.valueNames:
            values.append(self.__dict__[name].value)
        return values

    def getPacketFormat(self):
        '''
        Returns a struct compatible format string of the packet
        header and data
        '''
        return self.getHeaderFormat() + self.getDataFormat()

    def getPacketString(self):
        '''
        Returns a string containing the packet header and data. This
        string can be passed to .loadFromString(...).
        '''
        return struct.pack(
            self.getPacketFormat(),
            *self.getPacketValues())

    @staticmethod
    def readHeaderFromByteBuffer(byteBuffer):
        '''
        Read a packet header from an instance of ByteBuffer. This
        method will return a tuple containing the header
        values.
        '''
        return byteBuffer.peekStruct(BasePacket.HEADER_FORMAT)

    def loadDefaultValues(self):
        '''
        Override this method to assign default values.
        '''
        pass

    def loadFromString(self, packetString):
        '''
        Reconstitute the packet values from the packetString argument.
        '''
        unpackedValues = struct.unpack(
            self.getPacketFormat(),
            packetString)

        headerValueCount = len(self.getHeaderValues())

        for i, name in enumerate(self.valueNames):
            self.__dict__[name].value = unpackedValues[i+headerValueCount]

    def loadFromByteBuffer(self, byteBuffer):
        '''
        Reconstitute the packet from a ByteBuffer instance
        '''
        packetString = byteBuffer.readBytes(
            struct.calcsize(self.getPacketFormat()))
        self.loadFromString(packetString)


class ConnectRequest(BasePacket):
    '''
    A connection request packet - sent by a client to the server.
    '''
    PacketTypeID = BASE_PACKETID_SYSTEM+1
    PacketValues = {
        'protocol':'uchar'
    }

    def loadDefaultValues(self):
        self.protocol.value = PROTOCOL_VERSION


class ConnectRequestRejected(BasePacket):
    '''
    A connection request rejection packet - sent by the server back to
    a client.
    '''
    PacketTypeID = BASE_PACKETID_SYSTEM+2

class ConnectRequestAccepted(BasePacket):
    '''
    A connection request accepted packet - sent by the server back to
    a client.
    '''
    PacketTypeID = BASE_PACKETID_SYSTEM+3

class KeepAliveRequest(BasePacket):
    '''
    This is sent by the server to keep the connection alive.
    '''
    PacketTypeID = BASE_PACKETID_SYSTEM+4
    PacketValues = {
        'id':'short'
    }

class KeepAliveResponse(BasePacket):
    '''
    A clients response to the receipt of a KeepAliveRequest packet.
    '''
    PacketTypeID = BASE_PACKETID_SYSTEM+5
    PacketValues = {
        'id':'short'
    }

class Disconnected(BasePacket):
    '''
    This packet is sent by either the client or server to indicate to the
    other end of the connection that the link is closed. In cases where
    the connection is severed due to software crash, this packet will
    not be sent, and the socket will eventually disconnect due to a timeout.
    '''
    PacketTypeID = BASE_PACKETID_SYSTEM+6

class PacketAck(BasePacket):
    '''
    Sent by either a client or server to acknowledge receipt of an
    in-order or reliable packet.
    '''
    PacketTypeID = BASE_PACKETID_SYSTEM+7
    PacketValues = {
        'packetToAck':'int'
    }

class Ping(BasePacket):
    PacketTypeID = BASE_PACKETID_SYSTEM+8
    PacketValues = {
        'id':'short'
    }

class Pong(BasePacket):
    PacketTypeID = BASE_PACKETID_SYSTEM+9
    PacketValues = {
        'id':'short'
    }

class PacketFactoryItem(object):
    def __init__(self, packet_name, packet_type_id, packet_factory):
        self.packet_name = packet_name
        self.packet_type_id = packet_type_id
        self.packet_factory = packet_factory

class PacketFactory(object):
    def __init__(self):
        self.factories = []
        self.factoriesByName = {}
        self.factoriesById = {}

        self.add(*packets.values())

    def add(self, *packet_classes):
        '''
        Add packet class(es) to the packet factory.
        The parameters to this method must be subclasses of BasePacket.

        A PacketError will be raised if a packet already exists in
        this factory with an identical name or PacketTypeID.
        '''
        for packet_class in packet_classes:
            if packet_class.__name__ in self.factoriesByName:
                raise PacketError, 'Packet already in factory'
            if packet_class.PacketTypeID in self.factoriesById:
                raise PacketError, 'Packet %s has same Id as Packet %s' % (
                    packet_class.__name__,
                    self.factoriesById[packet_class.PacketTypeID].packet_name)
            newFactory = PacketFactoryItem(
                packet_class.__name__,
                packet_class.PacketTypeID,
                packet_class)
            self.factoriesByName[packet_class.__name__] = newFactory
            self.factoriesById[packet_class.PacketTypeID] = newFactory

    def getById(self, id):
        '''
        Obtain a packet class by specifying the packets PacketTypeID.
        If the packet cannot be found a PacketError exception is raised.
        '''
        try:
            return self.factoriesById[id].packet_factory
        except:
            raise PacketError, 'No packet exists with ID %s' % str(id)

    def getByName(self, name):
        '''
        Obtain a packet class by specifying the packets name.
        If the packet cannot be found a PacketError exception is raised.
        '''
        try:
            return self.factoriesByName[name].packet_factory
        except:
            raise PacketError, 'No packet exists with name %s' % str(name)

    def isA(self, packetInstance, packetName):
        '''
        Determine if packetInstance is an instance of the named packet class.

        Example:
        >>> tp = TestPacket1()
        >>> packetFactory.isA(tp, 'TestPacket1')
        True
        '''
        return isinstance(packetInstance, self.getByName(packetName))


packets = {
    'ConnectRequest':ConnectRequest,
    'ConnectRequestRejected':ConnectRequestRejected,
    'ConnectRequestAccepted':ConnectRequestAccepted,
    'KeepAliveRequest':KeepAliveRequest,
    'KeepAliveResponse':KeepAliveResponse,
    'Disconnected':Disconnected,
    'PacketAck':PacketAck,
    'Pong':Pong,
    'Ping':Ping
}

# The default global packet factory.
packetFactory = PacketFactory()