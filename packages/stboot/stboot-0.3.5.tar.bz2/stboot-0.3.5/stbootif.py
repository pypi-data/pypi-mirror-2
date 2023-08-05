# -*- coding: utf-8 -*-
# (c) Vladimir Ermakov, 2010, under terms of the new BSD License
# vim:set ts=4 sw=4 et:
"""
STM32F10x UART booltoader interface.
AN2662.
"""

__all__ = [
    'STBoot',
    'SK_STBoot',
    'ConnError',
    'AckError',
    'NAckError',
    'CmdNotSupported',
    'BAUDRATE',
    'RAM_ADDR',
    'FLASH_ADDR',
    'OPTION_ADDR',
]
__version__ = '0.3.5'
__author__ = 'Vladimir Ermakov'
__email__ = 'vooon341@gmail.com'

import time
import logging

import serial

log = logging.getLogger('stboot')
#log.setLevel(logging.INFO)

# default baudrate
BAUDRATE = 115200

# Memory map
RAM_ADDR    = 0x20001000
FLASH_ADDR  = 0x08000000
OPTION_ADDR = 0x1FFFF800

# Answers
ACK = 0x79
NACK = 0x1F

# Table 3. Bootloader commands
CMD_GET               = 0x00
CMD_GET_VERSION       = 0x01
CMD_GET_ID            = 0x02
CMD_READ              = 0x11
CMD_GO                = 0x21
CMD_WRITE             = 0x31
CMD_ERASE             = 0x43
CMD_WRITE_PROTECT     = 0x63
CMD_WRITE_UNPROTECT   = 0x73
CMD_READOUT_PROTECT   = 0x82
CMD_READOUT_UNPROTECT = 0x92


class ConnError(Exception):
    pass

class AckError(Exception):
    pass

class NAckError(Exception):
    pass

class CmdNotSupported(Exception):
    pass


def checkConnected(func):
    def inner(self, *args, **kwargs):
        if not self._connected:
            self.connect()
        return func(self, *args, **kwargs)
    return inner

def checkSupported(cmd):
    def deco(func):
        def inner(self, *args, **kwargs):
            if not self._geted:
                self.get()
            if not cmd in self._cmds:
                raise CmdNotSupported("Command 0x%02X not supported!"%cmd)
            return func(self, *args, **kwargs)
        return inner
    return deco

def checkGeted(func):
    def inner(self, *args, **kwargs):
        if not self._geted:
            self.get()
        return func(self, *args, **kwargs)
    return inner

def checkIDGeted(func):
    def inner(self, *args, **kwargs):
        if not self._id_geted:
            self.getID()
        return func(self, *args, **kwargs)
    return inner

def addsum(dlst):
    sum = 0
    for item in dlst:
        sum ^= item
    return dlst+[sum]


class STBoot(object):
    _pid = 0
    _cmds = [0]
    _version = 0x10
    _connected = False
    _geted = False
    _id_geted = False
    _protection_enabled = 0
    _protection_disabled = 0

    def __init__(self, port, baudrate=BAUDRATE):
        log.info("Opening port: '%s' %d,E,1" % (port, baudrate))
        self.com = serial.Serial(port, baudrate,
                                 8, serial.PARITY_EVEN, timeout=2)
        self.com.flush()
        self.com.flushInput()
        self.com.flushOutput()

    def __del__(self):
        self.close()

    def close(self):
        self.com.close()

    @property
    @checkGeted
    def version(self):
        return '%d.%d' % ((self._version>>4), (self._version & 0xf))

    @property
    @checkIDGeted
    def product_id(self):
        return self._pid

    def _send(self, dlst):
        if isinstance(dlst, int):
            dat = [dlst, 0xff^dlst]
        else:
            dat = addsum(dlst)
        log.debug("Send: "+' '.join((hex(i) for i in dat)))
        self.com.write(''.join((chr(i) for i in dat)))

    def _recv1(self):
        d = ord(self.com.read(1))
        log.debug("Recv: 0x%02X"%d)
        return d

    def _recv(self, len):
        d = [ord(i) for i in self.com.read(len)]
        log.debug("Recv: "+' '.join((hex(i) for i in d)))
        return d

    def _checkAck(self):
        c = self._recv1()
        if c == NACK:
            raise NAckError
        if c != ACK:
            raise AckError("c = 0x%02X"%c)

    def connect(self):
        """Connect"""
        log.info("connect()")
        self.com.write(chr(0x7F))
        c = self._recv1()
        if c == ACK:
            self._connected = True
            log.info("Connected")
            return True
        else:
            self._connected = False
            raise ConnError("NACK (0x%02X)" % c)

    @checkConnected
    def get(self):
        """
        GET command
        AN2662 2.6
        """
        log.info("get()")

        self._send(CMD_GET)
        self._checkAck()
        l = self._recv1()
        self._version = self._recv1()
        self._cmds = self._recv(l)
        self._checkAck()
        self._geted = True

        return {'version': self._version,
                'cmds': self._cmds}

    @checkConnected
    @checkSupported(CMD_GET_VERSION)
    def getVersion(self):
        """
        GET Version command
        AN2662 2.7
        """
        log.info("getVersion()")

        self._send(CMD_GET_VERSION)
        self._checkAck()
        self._version = self._recv1()
        self._protection_disabled = self._recv1()
        self._protection_enabled = self._recv1()
        self._checkAck()

        return self._version

    @checkConnected
    @checkSupported(CMD_GET_ID)
    def getID(self):
        """
        GET product ID
        AN2662 2.8
        """
        log.info("getID()")
        self._send(CMD_GET_ID)
        self._checkAck()
        l = self._recv1()
        self._pid = (self._recv1()<<8)|(self._recv1())
        self._checkAck()
        self._id_geted = True

        return self._pid

    @checkConnected
    @checkSupported(CMD_READ)
    def read(self, address, len):
        """
        Read memory
        AN2662 2.9
        """
        log.info("read(0x%08X, %i)"%(address, len))
        if len > 256:
            raise ValueError("Byte owerflow")

        self._send(CMD_READ)
        self._checkAck()
        self._send([
            (address>>24) & 0xff,
            (address>>16) & 0xff,
            (address>> 8) & 0xff,
            (address    ) & 0xff,
        ])
        self._checkAck()
        self._send(len-1)
        self._checkAck()
        data = self._recv(len)

        return data

    @checkConnected
    @checkSupported(CMD_GO)
    def go(self, address):
        """
        GO
        AN2662 2.10
        """
        log.info("go(0x%08X)"%address)
        self._send(CMD_GO)
        self._checkAck()
        self._send([
            (address>>24) & 0xff,
            (address>>16) & 0xff,
            (address>> 8) & 0xff,
            (address    ) & 0xff
        ])
        self._checkAck()

    @checkConnected
    @checkSupported(CMD_WRITE)
    def write(self, address, data):
        """
        Write memory
        AN2662 2.11
        """
        log.info("write(0x%08X, data len %i)"%(address, len(data)))
        if len(data) > 256:
            raise ValueError("Byte owerflow")

        self._send(CMD_WRITE)
        self._checkAck()
        self._send([
            (address>>24) & 0xff,
            (address>>16) & 0xff,
            (address>> 8) & 0xff,
            (address    ) & 0xff
        ])
        self._checkAck()
        self._send([len(data)-1]+data)
        self._checkAck()

        if address == OPTION_ADDR:
            # bootloader generates a system Reset
            self._connected = False

    @checkConnected
    @checkSupported(CMD_ERASE)
    def erase(self, pages=None, glob=False):
        """
        Erase pages or global erase
        AN2662 2.12
        """
        if glob == False and pages is None:
            raise ValueError("No pages specified")
        if pages is not None and len(pages) > 254:
            raise ValueError("0xff — global erase")

        if glob:
            log.info("erase(GLOBAL)")
        else:
            log.info("erase(%s)"%pages)

        self._send(CMD_ERASE)
        self._checkAck()
        if glob:
            self._send(0xff)
        else:
            self._send([len(pages)-1]+pages) # XXX: NOT TESTED!
        self._checkAck()

    @checkConnected
    @checkSupported(CMD_WRITE_PROTECT)
    def writeProtect(self, pages):
        """
        Write protect pages
        AN2662 2.13
        """
        log.info("writeProtect(%s)"%pages)
        self._send(CMD_WRITE_PROTECT)
        self._checkAck()
        self._send([len(pages)-1]+pages)
        self._checkAck()

    def _op_ack_ack_reboot(self, op):
        self._send(op)
        self._checkAck()
        self._checkAck()
        self._connected = False # bootloader generates a system Reset

    @checkConnected
    @checkSupported(CMD_WRITE_UNPROTECT)
    def writeUnProtect(self):
        """
        Unprotect all
        AN2662 2.14
        """
        log.info("writeUnProtect()")
        self._op_ack_ack_reboot(CMD_WRITE_UNPROTECT)

    @checkConnected
    @checkSupported(CMD_READOUT_PROTECT)
    def readoutProtect(self):
        """
        Readout protect
        AN2662 2.15
        """
        log.info("readoutProtect()")
        self._op_ack_ack_reboot(CMD_READOUT_PROTECT)

    @checkConnected
    @checkSupported(CMD_READOUT_UNPROTECT)
    def readoutUnProtect(self):
        """
        Readout unprotect
        AN2662 2.16
        """
        log.info("readoutUnProtect()")
        self._op_ack_ack_reboot(CMD_READOUT_UNPROTECT)


class SK_STBoot(STBoot):
    """SK-MSTM32F107"""
    def __init__(self, port, baudrate=BAUDRATE):
        STBoot.__init__(self, port, baudrate)

        # enter into bootloader
        self.setBoot0(True)
        self.setReset(True)
        time.sleep(0.1) # 100 ms
        self.setReset(False)
        time.sleep(0.5) # 500 ms
        self.setBoot0(False)

    def setReset(self, state):
        """DTR controls reset"""
        log.info("DTR: %s"%state)
        self.com.setDTR(state)

    def setBoot0(self, state):
        """RTS controls BOOT0"""
        log.info("RTS: %s"%state)
        self.com.setRTS(state)

    # hooks
    def _op_ack_ack_reboot(self, op):
        self.setBoot0(True)
        STBoot._op_ack_ack_reboot(self, op)

    def connect(self):
        STBoot.connect(self)
        self.setBoot0(False)

    def write(self, address, data):
        if address == OPTION_ADDR:
            self.setBoot0(True)
        STBoot.write(self, address, data)

