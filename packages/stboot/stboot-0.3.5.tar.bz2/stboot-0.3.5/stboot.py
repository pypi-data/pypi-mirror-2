#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 et:

import os
import sys
import logging
import stbootif as bootif
import opster
from opster import dispatch, command

try:
    import progressbar
    usebar = True
except:
    usebar = False


class VerifyFailed(Exception):
    pass


def getSTBoot(variant, tty, baudrate):
    if variant:
        return bootif.SK_STBoot(tty, baudrate)
    else:
        return bootif.STBoot(tty, baudrate)

def _verify(st, address, file_name, verbose=False):
    def checker(fb, db):
        if ord(fb) != db:
            raise VerifyFailed("Verify failed at page: 0x%08x"%address)

    if usebar and not verbose:
        bar = progressbar.ProgressBar(maxval=os.path.getsize(file_name),
                                      widgets=['Verifying: ',
                                               progressbar.Percentage(),
                                               ' ', progressbar.Bar(), ' ',
                                               progressbar.ETA()]).start()
        barpos = 0

    with open(file_name, 'rb') as fd:
        while True:
            fbuf = fd.read(256)
            if fbuf == '':
                break
            try:
                bl = len(fbuf)
                dbuf = st.read(address, bl)
                if usebar and not verbose:
                    barpos += bl
                    bar.update(barpos)
            except bootif.NAckError:
                opster.err("Bootloader error. Stoped at 0x%08x"%address)
                sys.exit(1)
            map(checker, fbuf, dbuf)
            address += 256

BR_DESC = ('b', bootif.BAUDRATE, 'Set baudrate')
SK_DESC = ('s', False, 'SK-MSTM32F107 compatible mode')
VERIFY_DESC = ('v', False, 'Verify data')
ERASE_DESC = ('e', False, 'Erase before program')
VERBOSE_DESC = ('V', False, 'Verbose output')

if int(opster.__version__.split('.')[2]) > 9:
    # Opster version before 0.9.10 don't support this:
    ADDR_DESC = ('a',
                 lambda x: bootif.FLASH_ADDR if x is None else int(x, 0),
                 'Start address')
    LENGTH_DESC = ('l',
                   lambda x: 256*1024 if x is None else int(x, 0),
                   'Byte length')
else:
    ADDR_DESC = ('a', bootif.FLASH_ADDR, 'Start address')
    LENGTH_DESC = ('l', 256*1024, 'Byte length')


@command(usage='[-b 115200] [-s] [-a 0x08000000] [-e] [-v] <tty> <bin-file>')
def program(tty,
           binfile,
           baudrate=BR_DESC,
           starterkit=SK_DESC,
           address=ADDR_DESC,
           verify=VERIFY_DESC,
           erase=ERASE_DESC,
           verbose=VERBOSE_DESC):
    """Program memory"""

    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)
    st = getSTBoot(starterkit, tty, baudrate)
    address_ = address

    if usebar and not verbose:
        barmax = os.path.getsize(binfile)
        bar = progressbar.ProgressBar(maxval=barmax,
                                      widgets=['Programming: ',
                                               progressbar.Percentage(),
                                               ' ', progressbar.Bar(), ' ',
                                               progressbar.ETA()]).start()
        barpos = 0

    if erase:
        print 'Erasing...'
        st.erase(glob=True)

    with open(binfile, 'rb') as fd:
        while True:
            buf = fd.read(256)
            if buf == '':
                break
            try:
                st.write(address, [ord(b) for b in buf])
                address += 256
                if usebar and not verbose:
                    bar.update(min(address-address_, barmax))
            except bootif.NAckError:
                opster.err("Bootloader error. Stoped at 0x%08x"%address)
                sys.exit(1)

    if verify:
        try:
            _verify(st, address_, binfile, verbose)
        except VerifyFailed as vf:
            opster.err(str(vf))
            opster.err('\n')
            sys.exit(2)

@command(usage='[-b 115200] [-s] [-a 0x08000000] <tty> <bin-file>')
def verify(tty,
           binfile,
           baudrate=BR_DESC,
           starterkit=SK_DESC,
           address=ADDR_DESC,
           verbose=VERBOSE_DESC):
    """Verify memory"""

    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)
    st = getSTBoot(starterkit, tty, baudrate)
    try:
        _verify(st, address, binfile, verbose)
    except VerifyFailed as vf:
        opster.err(str(vf))
        opster.err('\n')
        sys.exit(2)

@command(usage='[-b 115200] [-s] [-a 0x08000000] [-l 262144] <tty> <bin-file>')
def read(tty,
         binfile,
         baudrate=BR_DESC,
         starterkit=SK_DESC,
         address=ADDR_DESC,
         length=LENGTH_DESC,
         verbose=VERBOSE_DESC):
    """Read memory"""

    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)
    st = getSTBoot(starterkit, tty, baudrate)

    if usebar and not verbose:
        bar = progressbar.ProgressBar(maxval=length,
                                      widgets=['Reading: ',
                                               progressbar.Percentage(),
                                               ' ', progressbar.Bar(), ' ',
                                               progressbar.ETA()]).start()

    with open(binfile, 'wb') as fd:
        for block in range(address, address+length, 256):
            try:
                le = 256 if length > 256 else length
                buf = st.read(block, le)
                length -= 256
                fd.write(''.join([chr(b) for b in buf]))
                if usebar and not verbose:
                    bar.update(block-address+le)
            except bootif.NAckError:
                opster.err("Bootloader error. Stoped at 0x%08x"%block)
                sys.exit(1)

@command(usage='[-b 115200] [-s] <tty>')
def erase(tty,
          baudrate=BR_DESC,
          starterkit=SK_DESC,
          verbose=VERBOSE_DESC):
    """Flash global erase"""

    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)
    st = getSTBoot(starterkit, tty, baudrate)

    print 'Erasing...'
    st.erase(glob=True)

@command(usage='[-b 115200] [-s] <tty>')
def info(tty,
         baudrate=BR_DESC,
         starterkit=SK_DESC,
         verbose=VERBOSE_DESC):
    """Show device information"""

    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)
    st = getSTBoot(starterkit, tty, baudrate)

    print "Bootloader version: %s\n" \
          "Product ID: 0x%04x" % (st.version, st.product_id)

@command()
def version():
    """Show stboot version"""

    print 'STBoot version %s' % bootif.__version__


if __name__ == "__main__":
    dispatch()
