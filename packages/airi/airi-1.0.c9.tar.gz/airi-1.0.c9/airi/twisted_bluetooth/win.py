# -*- coding: utf-8 -*-
# Copyright (c) 2011 Naranjo Manuel Francisco <manuel@aircable.net>
# Copyright (c) 2001-2009 Twisted Matrix Laboratories.
# See Twisted LICENSE for details.

"""
Various Bluetooth Socket classes
"""

# System Imports
import os
import types
import socket
import sys
import operator
import bluetooth

from twisted.internet import tcp
from twisted.internet.tcp import *

from twisted.python import log

from bluetooth import *

L2CAP_SUPPORTED=False
SCO_SUPPORTED=False
PAIR_SUPPORTED=False

def isPairingSupported():
    return False

def shutdown(self, how):
    return self.close()

bluetooth.BluetoothSocket.shutdown = shutdown

class BluetoothConnection(tcp.Connection):
    """
    Superclass of all Bluetooth-socket-based Descriptors

    This is an abstract superclass of all objects which represent a Bluetooth
    connection based socket.

    @ivar logstr: prefix used when logging events related to this connection.
    @type logstr: C{str}

    """

class BluetoothBaseClient(tcp.Connection):
    """A base class for client Bluetooth (and similiar) sockets.
    """
    addressFamily = 31 # AF_BLUETOOTH
    proto = None

    def createInternetSocket(self):
        """(internal) Create a non-blocking socket using
        self.addressFamily, self.socketType.
        """
        if self.proto not in [ None, bluetooth.RFCOMM, bluetooth.L2CAP ]:
            raise RuntimeException("I only handle bluetooth sockets")
        
        print self.proto, type(self.proto)
        s = bluetooth.BluetoothSocket(self.proto)
        s.setblocking(0)
        tcp.fdesc._setCloseOnExec(s.fileno())
        return s

    def resolveAddress(self):
        self.realAddress = self.addr
        print "resolveAddress", self.realAddress
        self.doConnect()

    def doConnect(self):
        """I connect the socket.

        Then, call the protocol's makeConnection, and start waiting for data.
        """
        if not hasattr(self, "connector"):
            # this happens when connection failed but doConnect
            # was scheduled via a callLater in self._finishInit
            return

        try:
            self.socket.setblocking(True)
            connectResult = self.socket.connect(self.realAddress)
            self.socket.setblocking(False)
        except socket.error, se:
            connectResult = se.args[0]
            print "connectResult", connectResult
            if connectResult:
                if connectResult == EISCONN:
                    pass
                # on Windows EINVAL means sometimes that we should keep trying:
                # http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winsock/winsock/connect_2.asp
                elif ((connectResult in (EWOULDBLOCK, EINPROGRESS, EALREADY)) or
                      (connectResult == EINVAL and platformType == "win32")):
                    self.startReading()
                    self.startWriting()
                    return
                else:
                    self.failIfNotConnected(error.getConnectError((connectResult, strerror(connectResult))))
                    return

        # If I have reached this point without raising or returning, that means
        # that the socket is connected.
        del self.doWrite
        del self.doRead
        # we first stop and then start, to reset any references to the old doRead
        self.stopReading()
        self.stopWriting()
        self._connectDone()

    def doRead(self):
        """Calls self.protocol.dataReceived with all available data.

        This reads up to self.bufferSize bytes of data from its socket, then
        calls self.dataReceived(data) to process it.  If the connection is not
        lost through an error in the physical recv(), this function will return
        the result of the dataReceived call.
        """
        try:
            data = self.socket.recv(self.bufferSize)
        except (bluetooth.btcommon.BluetoothError, socket.error), se:
            if se.args[0] == EWOULDBLOCK:
                return
            else:
                return main.CONNECTION_LOST
        if not data:
            return main.CONNECTION_DONE
        return self.protocol.dataReceived(data)



class Client(BluetoothBaseClient, tcp.Client):
    """A Bluetooth client."""

    def __init__(self, proto, *args, **kwargs):
        if proto not in [ None, bluetooth.RFCOMM, bluetooth.L2CAP ]:
            raise RuntimeException("I only handle bluetooth sockets")
        self.proto = proto
        super(Client, self).__init__(*args, **kwargs)

    def getHost(self):
        """Returns a Bluetooth address.

        This indicates the address from which I am connecting.
        """
        return self.socket.getsockname()

    def getPeer(self):
        """Returns a Bluetooth address.

        This indicates the address that I am connected to.
        """
        return self.realAddress

class Server(BluetoothBaseClient, tcp.Connection):
    """
    Serverside bluetooth socket-stream connection class.

    This is a serverside network connection transport; a socket which came from
    an accept() on a server.
    """

    def startTLS(self, ctx, server=1):
        raise RuntimeException("not valid method")

    def getHost(self):
        """Returns a Bluetooth address.

        This indicates the server's address.
        """
        return self.socket.getsockname()

    def getPeer(self):
        """Returns a Bluetooth address.

        This indicates the client's address.
        """
        return self.client

class Port(tcp.Port):
    """
    A Bluetooth server port, listening for connections.

    L{twisted.internet.tcp.Port}
    """
    addressFamily = 31 # socket.AF_BLUETOOTH
    proto = None

    def __init__(self, proto, port, factory, backlog=50, interface='', reactor=None):
        """Initialize with a numeric port to listen on.
        """
        tcp.Port.__init__(self, port, factory, backlog, interface, reactor)
        if proto not in [ None, bluetooth.RFCOMM, bluetooth.L2CAP ]:
            raise RuntimeException("I only do Bluetooth")
        self.proto = proto

    def createInternetSocket(self):
        s = bluetooth.BluetoothSocket(self.proto)
        if platformType == "posix" and sys.platform != "cygwin":
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s

    def _buildAddr(self, (host, port)):
        return (host, port)

    def getHost(self):
        """Returns a Bluetooth Address

        This indicates the server's address.
        """
        return self.socket.getsockname()

class Connector(tcp.Connector):
    def __init__(self, proto, host, port, *a, **kw):
        tcp.Connector.__init__(self, host, int(port), *a, **kw)
        self.proto = proto

    def _makeTransport(self):
        return Client(self.proto, self.host, self.port, self.bindAddress, self, self.reactor)

    def getDestination(self):
        return (self.host, self.port)

def __connectGeneric(reactor, proto, host, port, factory, timeout=30, bindAddress=None):
    c = Connector(proto, host, port, factory, timeout, bindAddress, reactor)
    c.connect()
    return c

def connectRFCOMM(reactor, *a, **kw):
    return __connectGeneric(reactor, bluetooth.RFCOMM, *a, **kw)

def connectL2CAP(reactor, *a, **kw):
    return __connectGeneric(reactor, bluetooth.L2CAP, *a, **kw)

def resolve_name(address):
    try:
        return bluetooth.lookup_name(address)
    except:
        pass
    return None

