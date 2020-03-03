#
# File: basic.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: wx api interface view functions,
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

import json
import urllib3
import server.core.db as db
from flask import request, url_for, jsonify
from server.core import grimm as app
from server import user_logger
from server.utils.misc import request_success, request_fail
from server.core import wxappid, wxsecret


@app.route('/jscode2session', methods=['GET'])
def wxjscode2session():
    '''view function for validating weixin user openid'''
    if request.method == 'GET':
        js_code = request.args.get("js_code")
        if js_code is None:
            return request_fail()
        prefix = 'https://api.weixin.qq.com/sns/jscode2session?appid='
        suffix = '&grant_type=authorization_code'
        url = prefix + wxappid + '&secret=' + wxsecret + '&js_code=' + js_code + suffix
        user_logger.info('user login, wxapp authorization: %s', url)
        retry = 3
        while retry > 0:
            http = urllib3.PoolManager()
            response = http.request('GET', url)
            feedback = json.loads(response.data)
            # authorization success
            if response.status == 200 and 'openid' in feedback:
                break
            retry -= 1

        if retry != 0:
            feedback['server_errcode'] = 0
            openid = feedback['openid']
            if 'session_key' in feedback:
                del feedback['session_key']
            # query user in database
            if db.exist_row('user', openid=openid):
                try:
                    userinfo = db.expr_query('user', openid=openid)[0]
                except:
                    return request_fail('未知错误')
                feedback['isRegistered'] = True
                if userinfo['audit_status'] == 0:
                    feedback['auditStatus'] = 'pending'
                elif userinfo['audit_status'] == 1:
                    feedback['auditStatus'] = 'approved'
                elif userinfo['audit_status'] == -1:
                    feedback['auditStatus'] = 'rejected'
            else:
                feedback['isRegistered'] = False
                feedback['auditStatus'] = 'pending'
            feedback['status'] = 'success'
            user_logger.info('%s: wxapp authorization success', openid)
        else:
            user_logger.error('%s: wxapp authorization failed', openid)
            feedback['status'] = 'failure'

        return jsonify(feedback)
