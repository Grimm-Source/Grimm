#
# File: server/__init__.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# ------------------------------------------------------------------------- #
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: load necessary services, initialize environments.
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


# initialize system logger
sys_logger = logging.getLogger('sys-logger')
sys_logger.setLevel(logging.DEBUG)
if not os.path.isdir('../log'):
    os.mkdir('../log')
fh = logging.FileHandler('../log/sys.log', mode='a', encoding='utf8')
fmt = '%(asctime)s %(name)s %(levelname)1s %(message)s'
fmter = logging.Formatter(fmt)
fh.setFormatter(fmter)
sys_logger.addHandler(fh)

del fh, fmt, fmter


# check package dependency
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
except ImportError as e:
    sys_logger.error('Lack package dependency: %s', e.msg)
    raise e


# check python version
from core.exception import PyVersionNotSupported
PY_MAJOR = sys.version_info.major
PY_MINOR = sys.version_info.minor
PY_MICRO = sys.version_info.micro
PY_VERSION = '.'.join([str(PY_MAJOR), str(PY_MINOR), str(PY_MICRO)])

if PY_MAJOR < 3 or PY_MINOR < 6 or PY_MICRO < 5:
    e = PyVersionNotSupported(PY_VERSION)
    sys_logger.error('Unsupported Python: (%d, %s)', e.ecode, e.emsg)
    raise e

del PyVersionNotSupported


