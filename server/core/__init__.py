#
# File: server/core/__init__.py
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
    sys.path.insert(1, '../..')


grimm = None
grimm_ext = None
wxappid = None
wxsecret = None
socketio = None

# initialize grimm back-end service
if grimm is None:
    import json
    from flask import Flask
    from flask_cors import CORS
    from server.utils.misc import pardir
    from flask_socketio import SocketIO
    from server.core.globals import APP_SECURITY_PASSWORD_SALT, WX_CONFIG_FILE
    from server.core.globals import APP_CONFIG_FILE, APP_SECRET_KEY
    from server.core.globals import APP_TEMPLATE_PATH, APP_STATIC_PATH

    grimm = Flask('Grimm', static_folder=APP_STATIC_PATH, template_folder=APP_TEMPLATE_PATH)
    grimm_ext = CORS(grimm)
    # Flask app config
    grimm.config['SECRET_KEY'] = APP_SECRET_KEY # app secret key, default generated as random string
    grimm.config['SECURITY_PASSWORD_SALT'] = APP_SECURITY_PASSWORD_SALT # app security password salt
    grimm.config['JSON_AS_ASCII'] = False   # make return json object not limited as ascii
    grimm.config['JSON_SORT_KEYS'] = True   # sort return json object keys

    grimm.config.from_json(APP_CONFIG_FILE, silent=True)

    socketio = SocketIO(cors_allowed_origins='*', debug=True)
    socketio.init_app(grimm)

    with open(WX_CONFIG_FILE, mode='r') as fp:
        wxconfig = json.load(fp=fp, encoding='utf8')

    wxappid = wxconfig['appid']
    wxsecret = wxconfig['secret']

    del wxconfig, pardir
