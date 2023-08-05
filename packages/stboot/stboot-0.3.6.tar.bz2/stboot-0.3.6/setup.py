#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 et:

from os.path import join, dirname
from setuptools import setup
import stbootif

def readfile(filename):
    return open(join(dirname(__file__), filename)).read()

def desc():
    return readfile('README') + '\n\n' + readfile('ChangeLog.rst')

setup(
    name="stboot",
    description="""STM32F10x UART system bootloader interface.""",
    long_description=desc(),
    license="BSD",
    version = stbootif.__version__,
    author = stbootif.__author__,
    author_email = stbootif.__email__,
    url = "http://vehq.ru/project/STBoot",
    download_url = 'http://hg.vehq.ru/stboot/archive/%s.tar.bz2' % stbootif.__version__,
    keywords = ['ARM Cortex-M3', 'bootloader', 'programmer'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Environment :: Console',
        'Topic :: Software Development :: Embedded Systems',
    ],
    platforms = 'any',
    py_modules = ['stbootif'],
    scripts = ['stboot.py'],
    requires = ['pyserial', 'opster'],
    #install_requires = ['pyserial', 'opster'],
    extras_require = {'progress bar': ['progressbar']},
)
