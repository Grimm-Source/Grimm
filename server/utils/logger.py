#
# File: server/utils/logger.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: start logger instances.
#
# To-Dos:
#   1. make other supplements if needed.
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#   1. 2019/08/19, Ming, create first revision.
#

import os
import logging
from flask.logging import default_handler
from server.utils.misc import pardir
from server.core import grimm as app
from server.core.globals import SYS_LOG_FILE, SYS_LOGGING_LEVEL
from server.core.globals import USER_LOG_FILE, USER_LOGGING_LEVEL
from server.core.globals import ADMIN_LOG_FILE, ADMIN_LOGGING_LEVEL
from server.core.globals import APP_LOG_FILE, APP_LOGGING_LEVEL
from server.core.globals import DB_LOG_FILE, DB_LOGGING_LEVEL


__all__ = []

# initialize database logger
print('initializing database logger...', end=' ')
db_logger = None
__all__.append('db_logger')
if db_logger is None:
    db_logger = logging.getLogger('db-transaction-logger')
    # set logging level as default DEBUG level.
    db_logger.setLevel(DB_LOGGING_LEVEL)
    log_dir = pardir(DB_LOG_FILE)
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    # create logging file handler.
    fh = logging.FileHandler(DB_LOG_FILE, mode='a', encoding='utf8')
    # format
    fmt = '[%(asctime)s] %(levelname)s: %(message)s'
    fmter = logging.Formatter(fmt)
    fh.setFormatter(fmter)
    # add file handler
    db_logger.addHandler(fh)
    print('done!')


# initialize flask app logger
print('initializing Flask app logger...', end=' ')
app_logger = app.logger
__all__.append('app_logger')
if app_logger is None:
    raise RuntimeError('Flask app logger not correctly initialized!')
else:
    app_logger.removeHandler(default_handler)
    app_logger.setLevel(APP_LOGGING_LEVEL)
    log_dir = pardir(APP_LOG_FILE)
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    fh = logging.FileHandler(APP_LOG_FILE, mode='a', encoding='utf8')
    fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    fmtter = logging.Formatter(fmt)
    fh.setFormatter(fmtter)
    app_logger.addHandler(fh)
    print('done!')


# initialize system logger
print('initializing system logger...', end=' ')
sys_logger = None
__all__.append('sys_logger')
if sys_logger is None:
    sys_logger = logging.getLogger('sys-logger')
    sys_logger.setLevel(SYS_LOGGING_LEVEL)
    log_dir = pardir(SYS_LOG_FILE)
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    fh = logging.FileHandler(SYS_LOG_FILE, mode='a', encoding='utf8')
    fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    fmtter = logging.Formatter(fmt)
    fh.setFormatter(fmtter)
    sys_logger.addHandler(fh)
    print('done!')


# initialize admin logger
print('initializing admin logger...', end=' ')
admin_logger = None
__all__.append('admin_logger')
if admin_logger is None:
    admin_logger = logging.getLogger('admin-logger')
    admin_logger.setLevel(ADMIN_LOGGING_LEVEL)
    log_dir = pardir(ADMIN_LOG_FILE)
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    fh = logging.FileHandler(ADMIN_LOG_FILE, mode='a', encoding='utf8')
    fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    fmtter = logging.Formatter(fmt)
    fh.setFormatter(fmtter)
    admin_logger.addHandler(fh)
    print('done!')


# initialize user logger
print('initializing user logger...', end=' ')
user_logger = None
__all__.append('user_logger')
if user_logger is None:
    user_logger = logging.getLogger('user-logger')
    user_logger.setLevel(USER_LOGGING_LEVEL)
    log_dir = pardir(USER_LOG_FILE)
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    fh = logging.FileHandler(USER_LOG_FILE, mode='a', encoding='utf8')
    fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    fmtter = logging.Formatter(fmt)
    fh.setFormatter(fmtter)
    user_logger.addHandler(fh)
    print('done!')
