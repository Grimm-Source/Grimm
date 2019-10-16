#
# File: utils/template.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: some template webpages.
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


from flask import render_template
from server.core import grimm as app


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404  # ???
