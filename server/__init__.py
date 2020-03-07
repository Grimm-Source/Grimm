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


__all__ = ['GRIMM_VERSION', 'PY_VERSION', 'TOP_DIR']

# Grimm version string
GRIMM_VERSION = '1.0'
# Project top directory
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
if TOP_DIR not in sys.path:
    sys.path.insert(0, TOP_DIR)
# Grimm launcher
Launcher = sys.argv[0]
__all__.append('Launcher')
# Grimm required pkg list
Required_pkgs = ['json', 'flask', 'flask_cors', 'flask_socketio', 'uuid',
                 'signal', 'getpass', 'pymysql', 'logging', 'inspect',
                 'urllib3', 'platform', 'argparse', 'bcrypt', 'email',
                 'smtplib', 'ssl', 'dns.resolver', 'random', 'string',
                 'itsdangerous', 'werkzeug', 'socket', 'simplejson',
                 'atexit', 'hmac', 'shutil']
__all__.append('Required_pkgs')


# process launcher entries
import argparse
import server.core.globals
force_db_connect = False
__all__.append('force_db_connect')
# service is launched from start.py
if Launcher == 'start.py':
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
                        nargs='?', default=os.path.join(TOP_DIR, 'log/session.log'),
                        help='Specify a logfile when starting in daemon mode')
    parser.add_argument('-f', '--force', dest='force', action='store_true',
                        help='Force database connection when start')
    parser.add_argument('-D', '--daemon', dest='daemon', action='store_true',
                        help='Start in daemon mode')

    cmd_args = parser.parse_args()
    server.core.globals.HOST = cmd_args.host
    server.core.globals.PORT = cmd_args.port
    force_db_connect = cmd_args.force
    server.core.globals.DAEMON_LOAD = cmd_args.daemon
    server.core.globals.SESSION_LOG_FILE = cmd_args.logfile
    del parser, cmd_args
# service is launched from other entries
else:
    server.core.globals.HOST = '0.0.0.0'
    server.core.globals.PORT = 5000
    server.core.globals.SESSION_LOG_FILE = os.path.join(TOP_DIR, 'log/session.log')


# check python version
try:
    print('\nchecking python version...', end=' ')
except SyntaxError:
    print('\nchecking python version...', )
PY_MAJOR = sys.version_info.major
PY_MINOR = sys.version_info.minor
PY_MICRO = sys.version_info.micro
PY_VERSION = '.'.join([str(PY_MAJOR), str(PY_MINOR), str(PY_MICRO)])
if PY_VERSION < '3.6.5':
    print("Python %s is not supported, upgrade to 3.6.5 or later!" % (PY_VERSION))
    sys.exit(-1)
print('done!')


# check package dependency
print('checking required packages...', end=' ')
import importlib
for pkg in Required_pkgs:
    importlib.import_module(pkg)
del pkg, importlib
print('done!')


# get local os type
import platform
if server.core.globals.PLATFORM is None:
    server.core.globals.PLATFORM = platform.system()
PLATFORM = server.core.globals.PLATFORM
__all__.append('PLATFORM')
del platform


# print local host V4 ip
from server.utils.misc import get_host_ip
if server.core.globals.PLATFORM != 'Windows' and server.core.globals.HOST_IP == '0.0.0.0' or server.core.globals.HOST_IP is None:
    server.core.globals.HOST_IP = get_host_ip()
if Launcher == 'uwsgi':
    print('\n>>> Request Access: ' + server.core.globals.HOST_IP + '\n')
else:
    print('\n>>> Request Access: ' + server.core.globals.HOST_IP + ':' + str(server.core.globals.PORT) + '\n')
del get_host_ip


# initialize loggers and extend namespace
import server.utils.logger
from server.utils.logger import *
__all__.extend(server.utils.logger.__all__)


# register view functions and print rules
import server.core.view_function as view_function
from server.core import grimm
print('\nRegistered URL Mapping:')
print(grimm.url_map)
__all__.append('view_function')
__all__.append('grimm')


# connect database
import server.core.db as database
__all__.append('database')
database.init_connection(force=force_db_connect)


# check update root admin password
from server.core.globals import ROOT_PASSWORD
from server.utils.password import update_password
if database.exist_row('admin', admin_id=0):
    if database.expr_query('admin', fields='password', admin_id=0)[0]['password'] == 'default':
        if update_password(ROOT_PASSWORD, tbl='admin', admin_id=0):
            print('configure root admin password ... done!\n')
        else:
            print('configure root admin password failed!')
            sys.exit(-1)
else:
    print('Error: root admin isn\'t created by default, check your database!')
    sys.exit(-1)
del ROOT_PASSWORD, update_password


# register exit handler
import signal
from server.core.exit import exit_grimm
signal.signal(signal.SIGINT, exit_grimm)
# signal.signal(signal.SIGQUIT, exit_grimm)
signal.signal(signal.SIGTERM, exit_grimm)
del exit_grimm
