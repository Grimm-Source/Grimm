#
# File: exit.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# ------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: define the completed procedure when trying to exit grimm.
#
# To-Dos:
#   1. make other supplements if needed.
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#   1. 2019/08/13, Ming, create first revision.
#

import sys
import time

if '../..' not in sys.path:
    sys.path.append('../..')

import server.core.db as db
import server
from server.core.db import destory_connection


def exit_grimm(signalnum=None, frame=None):
    '''procedures to be executed when trying to exit grimm'''
    # close db_logger
    print('\n\nclose db-logger...')
    if db.db_logger is not None:
        db.db_logger.disabled = True
        db.db_logger = None
    # print(db.db_logger)
    # close sys_logger
    print('close sys-logger...')
    if server.sys_logger is not None:
        server.sys_logger.disabled = True
        server.sys_logger = None
    # print(server.sys_logger)
    # close user_logger
    print('close user-logger...')
    if server.user_logger is not None:
        server.user_logger.disabled = True
        server.user_logger = None
    # print(server.user_logger)
    # exit grimm backend service
    time.sleep(1)
    print('\nquit grimm back-end service done !\n')
    sys.exit(0)
