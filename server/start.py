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
import argparse
# jump out to upper directory, then `server` can be regarded as a pure python package
if '..' not in sys.path:
    sys.path.append('..')

import server
from server.core.wxapp import wxgrimm

parser = argparse.ArgumentParser(description='Load Grimm back-end service',
                                 add_help=False)
parser.add_argument('-h', '--host', metavar='Host IP', nargs='?',
                    default='0.0.0.0', dest='host')
parser.add_argument('-p', '--port', metavar='Port Num', nargs='?',
                    default=5000, type=int, dest='port')


if __name__ == '__main__':
    args = parser.parse_args()
    wxgrimm.run(host=args.host, port=args.port)
