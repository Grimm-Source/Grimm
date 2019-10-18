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
import signal
# jump out to upper directory, then `server` becomes a pure python package.
# must be placed ahead of other imports !!!
if '..' not in sys.path:
    sys.path.append('..')

# load services
import server
import server.core.db as db
from server import HOST, PORT
from server.core import grimm
from server.core.exit import exit_grimm

# import view function interfaces
import server.core.route.web_admin
import server.core.route.wxapp

# update root user info
from server.core.route.web_admin import ROOT_PASSWORD
from server.utils.password import update_password

if db.exist_row('admin', admin_id=0):
    if db.expr_query('admin', fields='password', admin_id=0)[0]['password'] == 'default':
        if update_password(ROOT_PASSWORD, tbl='admin', admin_id=0):
            print('configure root password ... Done\n')
        else:
            print('configure root password failed')
            sys.exit(-1)
else:
    print('root user is not registerd by default, check you database!')
    sys.exit(-1)


if __name__ == '__main__':
    # register signal handler
    signal.signal(signal.SIGINT, exit_grimm)
    signal.signal(signal.SIGQUIT, exit_grimm)
    signal.signal(signal.SIGTERM, exit_grimm)
    # start grimm back-end
    grimm.run(host=HOST, port=PORT)
