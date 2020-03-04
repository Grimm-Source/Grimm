#
# File: server/__init__.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: load necessary services, check configs,
# form package layers and do initialization jobs.
#
# To-Dos:
#   1. make other supplements if needed.
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#   1. 2019/08/12, Ming, create first revision.
#

import sys
import os
import logging


__all__ = ['GRIMM_VERSION', 'PY_VERSION']
GRIMM_VERSION = '1.0'


if '..' not in sys.path:
    sys.path.insert(0, '..')


# get local os type
import platform
import server.core.globals
if server.core.globals.PLATFORM is None:
    server.core.globals.PLATFORM = platform.system()
del platform


# handle user command arguments
import argparse

parser = argparse.ArgumentParser(prog='Grimm-backend',
                                 description='Load Grimm back-end service',
                                 add_help=False)
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s ' + GRIMM_VERSION,
                    help='Show %(prog)s version string and exit.')
parser.add_argument('-?', '--help', action='help',
                    help='Show this help message and exit.')
parser.add_argument('-h', '--host', metavar='Host IP', nargs='?',
                    default='0.0.0.0', dest='host',
                    help='Customize server host address.')
parser.add_argument('-p', '--port', metavar='Port Num', nargs='?',
                    default=5000, type=int, dest='port',
                    help='Customize service\'s listening port.')
parser.add_argument('-l', '--logfile', dest='logfile', metavar='Log File',
                    nargs='?', default='./log/session.log',
                    help='Specify a logfile when starting in daemon mode')
parser.add_argument('-f', '--force', dest='force', action='store_true',
                    help='Force database connection when start')
parser.add_argument('-D', '--daemon', dest='daemon', action='store_true',
                    help='Start in daemon mode')

cmdargs = parser.parse_args()
server.core.globals.HOST = cmdargs.host
server.core.globals.PORT = cmdargs.port
server.core.globals.FORCE_LOAD = cmdargs.force
server.core.globals.DAEMON_LOAD = cmdargs.daemon
server.core.globals.SESSION_LOG = cmdargs.logfile

del parser, argparse, cmdargs


# check python version
try:
    print('checking python version...', end=' ')
except SyntaxError:
    print('checking python version...', )
PY_MAJOR = sys.version_info.major
PY_MINOR = sys.version_info.minor
PY_MICRO = sys.version_info.micro
PY_VERSION = '.'.join([str(PY_MAJOR), str(PY_MINOR), str(PY_MICRO)])

if PY_VERSION < '3.6.5':
    print("Python %s is not supported, upgrade to 3.6.5 or later!" % (PY_VERSION))
    sys.exit(-1)
print('done!')


# check package dependency
print('checking package dependency...', end=' ')
try:
    import re
    import json
    import pymysql
    import urllib3
    import bcrypt
    import email
    import getpass
    import inspect
    import flask
except ImportError as err:
    raise err
print('done!')


# print local host V4 ip
from server.utils.misc import get_host_ip
if server.core.globals.PLATFORM != 'Windows' and server.core.globals.HOST_IP == '0.0.0.0' or server.core.globals.HOST_IP is None:
    server.core.globals.HOST_IP = get_host_ip()
print('\n>>> Request Access: ' + server.core.globals.HOST_IP + ':' + str(server.core.globals.PORT) + '\n')
del get_host_ip


# load loggers and append namespace
import server.utils.logger
from server.utils.logger import *
__all__.extend(server.utils.logger.__all__)
