#
# File: server/core/view_function/__init__.py
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

import os
import importlib
from os.path import dirname


__all__ = []
# Dynamically import all view function modules recursively down
dir_triples = [x for x in os.walk(dirname(__file__), topdown=False)]
pkg_info = {item[0].replace('/', '.').lstrip('.') : \
            [f[:-3] for f in item[2] if f.endswith('.py') and f != '__init__.py'] \
            for item in dir_triples if '__pycache__' not in item[0]}


for package, modules in pkg_info.items():
    for module in modules:
        pkg = package + '.' + module
        mod = importlib.import_module(pkg)
        __all__.append(pkg)
        globals()[module] = mod # add to globals

view_function_package_info = pkg_info

del dirname, dir_triples, pkg_info, package, modules, module, mod, pkg
