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

# initialize system logger
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

    del fh, fmt, fmtter, get_pardir, sys_log_path, log_dir


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
from server.core.exceptions import PyVersionNotSupported
PY_MAJOR = sys.version_info.major
PY_MINOR = sys.version_info.minor
PY_MICRO = sys.version_info.micro
PY_VERSION = '.'.join([str(PY_MAJOR), str(PY_MINOR), str(PY_MICRO)])

if PY_VERSION < '3.6.5':
    e = PyVersionNotSupported(PY_VERSION)
    sys_logger.error('Unsupported Python: (%d, %s)', e.ecode, e.emsg)
    raise e

del PyVersionNotSupported


