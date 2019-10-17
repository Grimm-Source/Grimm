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

import server
from server import HOST, PORT
from server.core import grimm
from server.core.exit import exit_grimm
# import view function interfaces
import server.core.route.web_admin
import server.core.route.wxapp


if __name__ == '__main__':
    # register signal handler
    signal.signal(signal.SIGINT, exit_grimm)
    signal.signal(signal.SIGQUIT, exit_grimm)
    signal.signal(signal.SIGTERM, exit_grimm)
    # start grimm back-end
    grimm.run(host=HOST, port=PORT)
