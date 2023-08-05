#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 et:

from os.path import join, dirname
from setuptools import setup
import stboot

def readfile(filename):
    return open(join(dirname(__file__), filename)).read()

def desc():
    return readfile('README') + '\n\n' + readfile('ChangeLog.rst')

setup(
    name="stboot",
    description="""STM32F10x UART system bootloader interface.""",
    long_description=desc(),
    license="BSD",
    version = stboot.__version__,
    author = stboot.__author__,
    author_email = stboot.__email__,
    url = "http://vehq.ru/project/ST-Boot",
    download_url = 'http://hg.vehq.ru/st-boot/archive/%s.tar.bz2' % stboot.__version__,
    keywords = ['ARM Cortex-M3', 'bootloader', 'programmer'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    py_modules = ['stboot'],
    scripts = ['st-boot.py'],
    install_requires = ['pyserial', 'opster'],
    platforms = 'any',
)
