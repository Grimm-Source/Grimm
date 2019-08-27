#
# File: user.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: server backend code template.
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


import os
import sys
import json
import db
from exceptions import *
from server.utils import password


class GrimmAdmin(object):
    '''
    class definition for Grimm Admin users.
    '''
    def __init__(self, json_obj)
