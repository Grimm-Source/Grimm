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
from server.utils.misc import pardir


__all__ = []

# initialize flask app logger
print('initializing Flask app logger...', end=' ')
app_logger = None
__all__.append('app_logger')
if app_logger is None:
    app_logger = logging.getLogger('app-logger')
    app_logger.setLevel(logging.DEBUG)
    log_dir = pardir(pardir(os.path.abspath(__file__))) + '/log'
    app_log_path = log_dir + '/app.log'
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    fh = logging.FileHandler(app_log_path, mode='a', encoding='utf8')
    app_logger.addHandler(fh)
print('done!')


# initialize system logger
print('initializing system logger...', end=' ')
sys_logger = None
__all__.append('sys_logger')
if sys_logger is None:
    sys_logger = logging.getLogger('sys-logger')
    sys_logger.setLevel(logging.DEBUG)
    log_dir = pardir(pardir(os.path.abspath(__file__))) + '/log'
    sys_log_path = log_dir + '/sys.log'
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    fh = logging.FileHandler(sys_log_path, mode='a', encoding='utf8')
    fmt = '%(asctime)s %(name)s %(levelname)1s %(message)s'
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
    admin_logger.setLevel(logging.DEBUG)
    log_dir = pardir(pardir(os.path.abspath(__file__))) + '/log'
    admin_log_path = log_dir + '/admin.log'
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    fh = logging.FileHandler(admin_log_path, mode='a', encoding='utf8')
    fmt = '%(asctime)s %(name)s %(levelname)1s %(message)s'
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
    user_logger.setLevel(logging.DEBUG)
    log_dir = pardir(pardir(os.path.abspath(__file__))) + '/log'
    user_log_path = log_dir + '/user.log'
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    fh = logging.FileHandler(user_log_path, mode='a', encoding='utf8')
    fmt = '%(asctime)s %(name)s %(levelname)1s %(message)s'
    fmtter = logging.Formatter(fmt)
    fh.setFormatter(fmtter)
    user_logger.addHandler(fh)
print('done!')
