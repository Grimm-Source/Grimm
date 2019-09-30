#
# File: misctool.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: contains misc tool functions.
#
# To-Dos:
#   1. make other supplements if needed.
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#   1. 2019/09/24, Ming, create first revision.
#


import os

# get parent directory
def get_pardir(_dir):
    '''truncate path to get parent directory path'''
    if _dir[-1] is os.path.sep:
        _dir = _dir.rstrip(os.path.sep)
    d = _dir.split(os.path.sep)
    d.pop()
    pd = os.path.sep.join(d)

    return pd



