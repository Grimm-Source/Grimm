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
import logging
import time
import server.core.db as db

from server import *


def exit_grimm(signalnum=None, frame=None):
    '''procedures to be executed when trying to exit grimm'''
    # close db_logger
    if db_logger is not None:
        print('\nclose db-logger...', end=' ')
        for handler in db_logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.close()
            db_logger.removeHandler(handler)
        db_logger.disabled = True
        print('done!')

    # close sys_logger
    if sys_logger is not None:
        print('close sys-logger...', end=' ')
        for handler in sys_logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.close()
            sys_logger.removeHandler(handler)
        sys_logger.disabled = True
        print('done!')

    # close user_logger
    if user_logger is not None:
        print('close user-logger...', end=' ')
        for handler in user_logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.close()
            user_logger.removeHandler(handler)
        user_logger.disabled = True
        print('done!')

    # close admin_logger
    if admin_logger is not None:
        print('close admin-logger...', end=' ')
        for handler in admin_logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.close()
            admin_logger.removeHandler(handler)
        admin_logger.disabled = True
        print('done!')

    # close app_logger
    if app_logger is not None:
        print('close app-logger...', end=' ')
        for handler in app_logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.close()
                app_logger.removeHandler(handler)
        app_logger.disabled = True
        print('done!')

    # close database connection
    print('close database connection...', end=' ')
    db.destroy_connection()
    print('done!')

    # exit grimm backend service
    time.sleep(1)
    print('\nquit grimm back-end service completely!')
    sys.exit(0)
