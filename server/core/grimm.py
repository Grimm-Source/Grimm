#
# File: grimm.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# ------------------------------------------------------------------------- #
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: the main mid-layer between grimm wxapp client and server.
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


from flask import Flask, request
import urllib3
import json
import db


wxapp = Flask(__name__)


with open('../config/wxapp.config', 'r') as fp:
    config = json.load(fp=fp, encoding='utf8')

wxapp.config['APP_ID'] = config['appid']
wxapp.config['APP_SECRTE'] = config['secret']
wxapp.config['SECURITY_PASSWORD_SALT'] = 3

print(wxapp.config['APP_ID'])
print(wxapp.config['APP_SECRTE'])
print(wxapp.config['SECURITY_PASSWORD_SALT'])

del config


def form_wx_url(appid, secret, js_code, grant_type='authorization_code'):
    url_head = f"https://api.weixin.qq.com/sns/jscode2session?"
    url_tail = f"appid={appid}&secret={secret}&\
                js_code={js_code}&grant_type={grant_type}"

    return url_head + url_tail


@wxapp.route('/jscode2session')
def wx_jscode2session():
    jscode = request.args.get('js_code')
    url = form_wx_url(wxappid, wxsecret, jscode)
    http = urllib3.PoolManager()
    response = http.request('GET', url)

    if response == 200:
        response_data = response.data

        data = json.loads(response_data)
        data['server_errcode'] = 0
        data['is_register'] = False
        new_data = json.dumps(data)
    else:
        data = {'server_errcode': -1}
        new_data = json.dumps(data)

    return new_data


