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

# import view function interfaces
import server.core.route.web_admin
import server.core.route.wxapp

from server.core.const import ROOT_PASSWORD, HOST, PORT, FORCELOAD
from server.utils.password import update_password
from server.core.exit import exit_grimm
from server.core import grimm


if __name__ == '__main__':
    # register signal handler
    signal.signal(signal.SIGINT, exit_grimm)
    # signal.signal(signal.SIGQUIT, exit_grimm)
    signal.signal(signal.SIGTERM, exit_grimm)

    # initialize database connection
    db.init_connection(force=True if FORCELOAD is True else False)

    # update root admin password
    if db.exist_row('admin', admin_id=0):
        if db.expr_query('admin', fields='password', admin_id=0)[0]['password'] == 'default':
            if update_password(ROOT_PASSWORD, tbl='admin', admin_id=0):
                print('configure root admin password ... Done\n')
            else:
                print('configure root admin password failed')
                sys.exit(-1)
    else:
        print('Error: root admin isn\'t created by default, check your database!')
        sys.exit(-1)

    # start grimm back-end server
    grimm.run(host=HOST, port=PORT)
