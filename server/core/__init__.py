#
# File: core/__init__.py
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

if '../..' not in sys.path:
    sys.path.append('../..')

if '..' not in sys.path:
    sys.path.append('..')


grimm = None
grimm_ext = None
wxappid = None
wxsecret = None
socketio = None
api = None

# initialize grimm back-end service
if grimm is None:
    import os
    import uuid
    import json
    from flask import Flask
    from flask_cors import CORS
    from server.utils.misctools import get_pardir
    from flask_socketio import SocketIO
    from flask_restx import Api

    grimm = Flask('grimm')
    grimm_ext = CORS(grimm)

    grimm.config['SECRET_KEY']= os.urandom(24)
    grimm.config['SECURITY_PASSWORD_SALT'] = uuid.uuid4().hex

    socketio = SocketIO(cors_allowed_origins='*', debug=True)
    socketio.init_app(grimm)

    path = get_pardir(get_pardir(os.path.abspath(__file__)))
    with open(path + '/config/wxapp.config', mode='r') as fp:
        wxconfig = json.load(fp=fp, encoding='utf8')

    wxappid = wxconfig['appid']
    wxsecret = wxconfig['secret']

    del wxconfig, get_pardir, path
    api = Api(grimm)
