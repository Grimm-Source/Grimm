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
from server.utils.misctools import get_pardir


if '..' not in sys.path:
    sys.path.append('..')

if '../..' not in sys.path:
    sys.path.append('../..')

VERSION = '1.0'

# parse user command argument, host/port
import argparse
parser = argparse.ArgumentParser(prog='Grimm-backend',
                                 description='Load Grimm back-end service',
                                 add_help=False)
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s ' + VERSION,
                    help='Show %(prog)s version string and exit.')
parser.add_argument('-?', '--help', action='help',
                    help='Show this help message and exit.')
parser.add_argument('-h', '--host', metavar='Host IP', nargs='?',
                    default='0.0.0.0', dest='host',
                    help='Customize server host address.')
parser.add_argument('-p', '--port', metavar='Port Num', nargs='?',
                    default=5000, type=int, dest='port',
                    help='Customize service\'s listening port.')
parser.add_argument('-f', '--force', dest='force', action='store_true',
                    help='Force database connection when start')

CMDARGS = parser.parse_args()
HOST = CMDARGS.host
PORT = CMDARGS.port
FORCE = CMDARGS.force

del parser, argparse

# check python version
print('checking python version...')
from server.core.exceptions import PyVersionNotSupported
PY_MAJOR = sys.version_info.major
PY_MINOR = sys.version_info.minor
PY_MICRO = sys.version_info.micro
PY_VERSION = '.'.join([str(PY_MAJOR), str(PY_MINOR), str(PY_MICRO)])

if PY_VERSION < '3.6.5':
    raise PyVersionNotSupported(PY_VERSION)

del PyVersionNotSupported
print('check python version successfully !')


# check package dependency
print('checking package dependency...')
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
print('check package dependency successfully !')


# initialize system logger
print('initializing system logger...')
sys_logger = None
if sys_logger is None:
    sys_logger = logging.getLogger('sys-logger')
    sys_logger.setLevel(logging.DEBUG)
    log_dir = get_pardir(os.path.abspath(__file__)) + '/log'
    sys_log_path = log_dir + '/sys.log'
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    fh = logging.FileHandler(sys_log_path, mode='a', encoding='utf8')
    fmt = '%(asctime)s %(name)s %(levelname)1s %(message)s'
    fmtter = logging.Formatter(fmt)
    fh.setFormatter(fmtter)
    sys_logger.addHandler(fh)

    del fh, fmt, fmtter, sys_log_path, log_dir
print('system logger initialized successfully !')

# initialize admin logger
print('initializing admin logger...')
admin_logger = None
if admin_logger is None:
    admin_logger = logging.getLogger('admin-logger')
    admin_logger.setLevel(logging.DEBUG)
    log_dir = get_pardir(os.path.abspath(__file__)) + '/log'
    admin_log_path = log_dir + '/admin.log'
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    fh = logging.FileHandler(admin_log_path, mode='a', encoding='utf8')
    fmt = '%(asctime)s %(name)s %(levelname)1s %(message)s'
    fmtter = logging.Formatter(fmt)
    fh.setFormatter(fmtter)
    admin_logger.addHandler(fh)

    del fh, fmt, fmtter, admin_log_path, log_dir
print('admin logger initialized successfully !')

# initialize user logger
print('initializing user logger...')
user_logger = None
if user_logger is None:
    user_logger = logging.getLogger('user-logger')
    user_logger.setLevel(logging.DEBUG)
    log_dir = get_pardir(os.path.abspath(__file__)) + '/log'
    user_log_path = log_dir + '/user.log'
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    fh = logging.FileHandler(user_log_path, mode='a', encoding='utf8')
    fmt = '%(asctime)s %(name)s %(levelname)1s %(message)s'
    fmtter = logging.Formatter(fmt)
    fh.setFormatter(fmtter)
    user_logger.addHandler(fh)

    del fh, fmt, fmtter, user_log_path, log_dir
print('user logger initialized successfully !')
