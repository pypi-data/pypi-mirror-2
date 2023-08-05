# legume. Copyright 2009 Dale Reidy. All rights reserved.
# See LICENSE for details.

__docformat__ = 'restructuredtext'

import socket
import errno

USHRT_MAX = 65535

DEFAULT_TIMEOUT = float(10) # default timeout in seconds
PROTOCOL_VERSION = 4

class LegumeError(Exception): pass
class NetworkEndpointError(LegumeError): pass
class PacketDataError(LegumeError): pass
class ServerError(LegumeError): pass
class MessageError(LegumeError): pass

def isValidPort(port):
    '''
    Returns True if the port parameter is within the
    range 1...65535.
    '''
    return port in xrange(1, 65535)

class NetworkEndpoint(object):
    DISCONNECTED = 100
    ERRORED = 101
    LISTENING = 102
    CONNECTING = 103
    CONNECTED = 104

    MTU = 1400

    def __init__(self, message_factory):
        self._state = self.DISCONNECTED
        self._socket = None
        self.message_factory = message_factory
        self._timeout = DEFAULT_TIMEOUT

    @property
    def timeout(self):
        return self._timeout

    def setTimeout(self, timeout):
        self._timeout = float(timeout)

    def getSocket(self):
        return self._socket
    socket = property(getSocket)

    def createSocket(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setblocking(0)
        return self.socket

    def _shutdownSocket(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()

    def connectSocket(self, addr):
        self._socket.connect(addr)

    def bindSocket(self, addr):
        self._socket.bind(addr)

    def isActive(self):
        return self._state in [
            self.LISTENING, self.CONNECTING, self.CONNECTED]

    def doRead(self, callback):
        if self._state in [self.LISTENING, self.CONNECTED, self.CONNECTING]:
            if self.socket:
                try:
                    while True:
                        data, addr = self.socket.recvfrom(self.MTU, 0)
                        callback(data, addr)
                except socket.error, e:
                    try:
                        errornum = e[0]
                        if errornum not in [errno.EWOULDBLOCK,errno.ECONNRESET]:
                            raise
                    except:
                        raise
            else:
                raise NetworkEndpointError, 'Endpoint is not active'

    def getState(self):
        return self._state
    state = property(getState)
