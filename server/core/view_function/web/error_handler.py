#
# File: server/core/view_function/error_page.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: render web error pages,
#
# To-Dos:
#   1. make other supplements if needed.
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#   1. 2019/09/19, Ming, create first revision.
#

from flask import render_template
from flask import url_for, redirect
from server.core import grimm as app


# 400 error
@app.errorhandler(400)
def Bad_Request(error):
    return render_template('http_error_page/HTTP400.html')


# 401 error
@app.errorhandler(401)
def Unauthorized(error):
    return render_template('http_error_page/HTTP401.html')


# 403 error
@app.errorhandler(403)
def Forbidden(error):
    return render_template('http_error_page/HTTP403.html')


# 404 error
@app.errorhandler(404)
def Not_Found(error):
    return render_template('http_error_page/HTTP404.html')


# 500 error
@app.errorhandler(500)
def Internal_Server_Error(error):
    return render_template('http_error_page/HTTP500.html')


# 501 error
@app.errorhandler(501)
def Not_Implemented(error):
    return render_template('http_error_page/HTTP501.html')


# 502 error
@app.errorhandler(502)
def Bad_Gateway(error):
    return render_template('http_error_page/HTTP502.html')


# 503 error
@app.errorhandler(503)
def Service_Unavailable_503(error):
    return render_template('http_error_page/HTTP503.html')

'''
# 521 error
@app.errorhandler(521)
def Service_Unavailable_521(error):
    return render_template('http_error_page/HTTP521.html')


# 520 error
@app.errorhandler(520)
def Unknown_Host(error):
    return render_template('http_error_page/HTTP520.html')


# 533 error
@app.errorhandler(533)
def Scheduled_Maintenance(error):
    return render_template('http_error_page/HTTP533.html')
'''
