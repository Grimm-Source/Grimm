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
import atexit
# jump out to upper directory, then `server` becomes a pure python package.
# must be placed ahead of other imports !!!
if '..' not in sys.path:
    sys.path.insert(1, '..')

# load services
import server

from server.core.globals import HOST, PORT, DAEMON_LOAD, SESSION_LOG_FILE
from server.core import grimm as app


# start Grimm back-end in daemon mode
def start_daemon(logfile=None, pid_file=None):
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
    if logfile is not None:
        with open('/dev/null') as null_read, open(logfile, mode='w+') as logger:
            os.dup2(null_read.fileno(), sys.stdin.fileno())
            os.dup2(logger.fileno(), sys.stdout.fileno())
            os.dup2(logger.fileno(), sys.stderr.fileno())

    # write pid file
    if pid_file is not None:
        with open(pid_file, 'w+') as fd:
            fd.write(str(os.getpid()))
        atexit.register(os.remove, pid_file)

    # start grimm back-end server
    app.run(host=HOST, port=PORT)


# Grimm back-end main entry
if __name__ == '__main__':
    # start grimm back-end server
    if DAEMON_LOAD:
        start_daemon(SESSION_LOG_FILE)
    else:
        app.run(host=HOST, port=PORT)
