#
# File: start.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# ------------------------------------------------------------------------- #
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: start whole back-end service.
#
# To-Dos:
#   1. make other supplements if needed.
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#   1. 2019/08/27, Ming, create first revision.
#

import sys
import os
import signal
import atexit
# handle user command arguments
import argparse
# jump out to upper directory, then `server` becomes a pure python package.
# must be placed ahead of other imports !!!
if '..' not in sys.path:
    sys.path.append('..')

# load services
import server
import server.core.db as db
import server.core.const as const

# import view function interfaces
import server.core.route.web_admin
import server.core.route.wxapp
import server.core.route.devapis

from server.utils.password import update_password
from server.core.exit import exit_grimm
from server.core import grimm

GRIMM_VERSION = '1.0'

def initialize():
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
    const.HOST = cmdargs.host
    const.PORT = cmdargs.port
    const.FORCE_LOAD = cmdargs.force
    const.DAEMON_LOAD = cmdargs.daemon
    const.SESSION_LOG = cmdargs.logfile

    # print local host V4 ip
    from server.utils.misctools import get_host_ip
    if const.PLATFORM != 'Windows' and const.HOST_IP == '0.0.0.0' or const.HOST_IP is None:
        const.HOST_IP = get_host_ip()
    print('\n>>> IPv4 Access Info: ' + const.HOST_IP + ':' + str(const.PORT) + '\n')
    del get_host_ip

# start Grimm back-end in daemon mode
def start_daemon(logfile, pid_file=None):
    '''start Grimm back-end in daemon mode'''
    son_pid = os.fork()
    # exit father
    if son_pid:
        sys.exit(0)

    # fork grandson and exit son
    os.umask(0)
    os.setsid()

    grandson_pid = os.fork()
    if grandson_pid:
        sys.exit(0)

    # flush stdin/stdout
    sys.stdout.flush()
    sys.stderr.flush()

    # disregard stdin, and redirect stdout/stderr to session logfile
    with open('/dev/null') as null_read, open(logfile, mode='w') as logger:
        os.dup2(null_read.fileno(), sys.stdin.fileno())
        os.dup2(logger.fileno(), sys.stdout.fileno())
        os.dup2(logger.fileno(), sys.stderr.fileno())

    # write pid file
    if pid_file:
        with open(pid_file, 'w+') as fd:
            fd.write(str(os.getpid()))

        atexit.register(os.remove, pid_file)

    # start grimm back-end server
    grimm.run(host=const.HOST, port=const.PORT)



# Grimm back-end main entry
if __name__ == '__main__':
    initialize()
    # register signal handler
    signal.signal(signal.SIGINT, exit_grimm)
    # signal.signal(signal.SIGQUIT, exit_grimm)
    signal.signal(signal.SIGTERM, exit_grimm)

    # initialize database connection
    db.init_connection(force=const.FORCE_LOAD)

    # update root admin password
    if db.exist_row('admin', id=0):
        if db.expr_query('admin', fields='password', id=0)[0]['password'] == 'default':
            if update_password(const.ROOT_PASSWORD, tbl='admin', id=0):
                print('configure root admin password ... Done\n')
            else:
                print('configure root admin password failed')
                sys.exit(-1)
    else:
        print('Error: root admin isn\'t created by default, check your database!')
        sys.exit(-1)

    # start grimm back-end server
    if const.DAEMON_LOAD:
        start_daemon(const.SESSION_LOG)
    else:
        grimm.run(host=const.HOST, port=const.PORT)
