#
# File: server/deploy/wsgi.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: uwsgi application.
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

import sys

if '../..' not in sys.path:
    sys.path.insert(2, '../..')


import server
from server.core import grimm as app



if __name__ == '__main__':
    app.run()
