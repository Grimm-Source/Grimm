#
# File: server/utils/__init__.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: form python package layers.
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
import os

__all__ = []

DYSMS_PKG_DIR = os.path.dirname(os.path.abspath(__file__))
if DYSMS_PKG_DIR not in sys.path:
    sys.path.insert(1, DYSMS_PKG_DIR)
__all__.append(DYSMS_PKG_DIR)
