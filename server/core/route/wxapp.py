#
# File: wxapp.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: all view functions for wxapp,
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

import sys
import os
import json
import urllib3
from datetime import datetime
from flask import request, url_for

import server.core.db as db
import server.utils.sms_verify as sms_verify
from server.core import grimm as app
from server.core import wxappid, wxsecret
from server import user_logger
from server.utils.misctools import json_dump_http_response, json_load_http_request

from server.core.const import SMS_VRF_EXPIRY


SMS_VERIFIED_OPENID = {}


@app.route('/jscode2session', methods=['GET'])
def wxjscode2session():
    '''view function for validating weixin user openid'''
    if request.method == 'GET':
        js_code = request.args.get("js_code")
        if js_code is None:
            return json_dump_http_response({'status': 'failure'})
        prefix = 'https://api.weixin.qq.com/sns/jscode2session?appid='
        suffix = '&grant_type=authorization_code'
        url = prefix + wxappid + '&secret=' + wxsecret + '&js_code=' + js_code + suffix
        user_logger.info('user login, wxapp authorization: %s', url)
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        # authorization success
        if response.status == 200:
            feedback = json.loads(response.data)
            feedback['server_errcode'] = 0
            openid = feedback['openid']
            if 'session_key' in feedback:
                del feedback['session_key']
            # query user in database
            if db.exist_row('user', openid=openid):
                try:
                    userinfo = db.expr_query('user', openid=openid)[0]
                except:
                    return json_dump_http_response({'status': 'failure', 'message': '未知错误'})
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

        return json_dump_http_response(feedback)


@app.route('/register', methods=['POST'])
def register():
    '''view function for registering new user to database'''
    if request.method == 'POST':
        global SMS_VERIFIED_OPENID
        userinfo = {}
        info = json_load_http_request(request)  # get http POST data bytes format
        # fetch data from front end
        userinfo['openid'] = request.headers.get('Authorization')
        openid = userinfo['openid']
        if not db.exist_row('user', openid=openid):
            # confirm sms-code
            if not ('verification_code' in info or openid in SMS_VERIFIED_OPENID):
                user_logger.warning('%s: user registers before sms verification', openid)
                return json_dump_http_response({'status': 'failure', 'message': '未认证注册用户'})
            if 'verification_code' in info:
                vrfcode = info['verification_code']
                phone_number = info['tel']
                sms_token = sms_verify.fetch_token(phone_number)
                if sms_token is None:
                    user_logger.warning('%s: no such a sms token for number', phone_number)
                    return json_dump_http_response({'status': 'failure', 'message': '未向该用户发送验证短信'})
                if sms_token.expired:
                    user_logger.warning('%s, %s: try to validate user with expired token', phone_number, sms_token.vrfcode)
                    sms_verify.drop_token(phone_number)
                    return json_dump_http_response({'status': 'failure', 'message': '过期验证码'})
                if not sms_token.valid:
                    user_logger.warning('%s: try to validate user with invalid token', phone_number)
                    sms_verify.drop_token(phone_number)
                    return json_dump_http_response({'status': 'failure', 'message': '无效验证码'})

                result = sms_token.validate(phone_number=phone_number, vrfcode=vrfcode)
                if result is not True:
                    user_logger.warning('%s, %s: sms code validation failed, %s', phone_number, vrfcode, result)
                    return json_dump_http_response({'status': 'failure', 'message': result })
                user_logger.info('%s, %s: sms code validates successfully', phone_number, vrfcode)
                sms_verify.drop_token(phone_number)  # drop token from pool after validation
            else:
                del SMS_VERIFIED_OPENID[openid]
            # mock user info and do inserting
            userinfo['birth'] = info['birthdate']
            userinfo['remark'] = info['comment']
            userinfo['disabled_id'] = info['disabledID']
            userinfo['emergent_contact'] = info['emergencyPerson']
            userinfo['emergent_contact_phone'] = info['emergencyTel']
            userinfo['gender'] = info['gender']
            userinfo['idcard'] = info['idcard']
            userinfo['address'] = info['linkaddress']
            userinfo['contact'] = info['linktel']
            userinfo['name'] = info['name']
            userinfo['role'] = 0 if info['role'] == "志愿者" else 1
            userinfo['audit_status'] = 0
            userinfo['registration_date'] = datetime.now().strftime('%Y-%m-%d')
            userinfo['phone'] = info['tel']
            userinfo['phone_verified'] = 1
            try:
                if db.expr_insert('user', userinfo) != 1:
                    user_logger.error('%s: user registration failed', openid)
                    return json_dump_http_response({'status': 'failure', 'message': '录入用户失败，请重新注册'})
            except:
                user_logger.error('%s: user registration failed', openid)
                return json_dump_http_response({'status': 'failure', 'message': '未知错误，请重新注册'})

            user_logger.info('%s: complete user registration success', openid)
            return json_dump_http_response({'status': 'success'})

        user_logger.error('%s: user is registered already', openid)
        return json_dump_http_response({'status': 'failure', 'message': '用户已注册，请登录'})


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    '''view function for displaying or updating user profile'''
    feedback = {'status': 'success'}
    if request.method == 'GET':
        openid = request.headers.get('Authorization')
        if db.exist_row('user', openid=openid):
            try:
                userinfo = db.expr_query('user', openid=openid)[0]
            except:
                return json_dump_http_response({'status': 'failure', 'message': '未知错误'})
            feedback['openid'] = userinfo['openid']
            feedback['birthDate'] = userinfo['birth']
            feedback['usercomment'] = userinfo['remark']
            feedback['disabledID'] = userinfo['disabled_id']
            feedback['emergencyPerson'] = userinfo['emergent_contact']
            feedback['emergencyTel'] = userinfo['emergent_contact_phone']
            feedback['gender'] = userinfo['gender']
            feedback['idcard'] = userinfo['idcard']
            feedback['linkaddress'] = userinfo['address']
            feedback['linktel'] = userinfo['contact']
            feedback['name'] = userinfo['name']
            feedback['role'] = "志愿者" if userinfo['role'] == 0 else "视障人士"
            feedback['tel'] = userinfo['phone']
            feedback['registrationDate'] = userinfo['registration_date']
            user_logger.info('%s: user login successfully', userinfo['openid'])
            return json_dump_http_response(feedback)

        user_logger.warning('%s: user not registered', openid)
        return json_dump_http_response({'status': 'failure', 'message': '用户未注册'})

    if request.method == 'POST':
        newinfo = json_load_http_request(request)  # get request POST user data
        userinfo = {}
        userinfo['openid'] = request.headers.get('Authorization')
        userinfo['phone'] = newinfo['tel']
        userinfo['gender'] = newinfo['gender']
        userinfo['birth'] = newinfo['birthDate']
        userinfo['contact'] = newinfo['linktel']
        userinfo['address'] = newinfo['linkaddress']
        userinfo['emergent_contact'] = newinfo['emergencyPerson']
        userinfo['emergent_contact_phone'] = newinfo['emergencyTel']
        userinfo['remark'] = newinfo['usercomment']
        try:
            if db.expr_update('user', userinfo, openid=userinfo['openid']) != 1:
                user_logger.error('%s: user update info failed', userinfo['openid'])
                return json_dump_http_response({'status': 'failure', 'message': "更新失败，请重新输入"})
        except:
            return json_dump_http_response({'status': 'failure', 'message': '未知错误'})

        user_logger.info('%s: complete user profile updating successfully', userinfo['openid'])
        return json_dump_http_response({'status': 'success'})


@app.route('/smscode', methods=['GET', 'POST'])
def smscode():
    '''view function to send and verify sms verification code'''
    # send smscode
    if request.method == 'GET':
        phone_number = request.args.get('tel')
        if phone_number is None:
            user_logger.warning('invalid url parameter phone_number')
            return json_dump_http_response({'status': 'failure', 'message': '无效url参数'})
        try:
            sms_verify.drop_token(phone_number)  # drop old token if it exists
            sms_token = sms_verify.SMSVerifyToken(phone_number=phone_number,
                                                  expiry=SMS_VRF_EXPIRY,
                                                  template='REGISTER_USER')
            if not sms_token.send_sms():
                user_logger.warning('%s, unable to send sms to number', phone_number)
                return json_dump_http_response({'status': 'failure', 'message': '发送失败'})
        except Exception as err:
            return json_dump_http_response({'status': 'failure', 'message': f"{err.args}"})
        # append new token to pool
        sms_verify.append_token(sms_token)

        user_logger.info('%s, %s: send sms to number successfully', phone_number, sms_token.vrfcode)
        return json_dump_http_response({'status': 'success'})

    # verify smscode
    if request.method == 'POST':
        global SMS_VERIFIED_OPENID
        data = json_load_http_request(request)
        phone_number = data['tel']
        vrfcode = data['verification_code']
        openid = request.headers.get('Authorization')
        sms_token = sms_verify.fetch_token(phone_number)
        if sms_token is None:
            user_logger.warning('%s: no such a sms token for number', phone_number)
            return json_dump_http_response({'status': 'failure', 'message': '未向该用户发送验证短信'})
        result = sms_token.validate(phone_number=phone_number, vrfcode=vrfcode)
        if result is not True:
            user_logger.warning('%s, %s: sms code validation failed, %s', phone_number, vrfcode, result)
            return json_dump_http_response({'status': 'failure', 'message': result })
        sms_verify.drop_token(phone_number)  # drop token from pool if validated
        # try update database first, if no successful, append this openid.
        try:
            if db.expr_update('user', {'phone_verified': 1}, openid=openid) is False:
                SMS_VERIFIED_OPENID[openid] = phone_number
        except:
            user_logger.warning('%s: update user phone valid status failed', openid)
            return json_dump_http_response({'status': 'failure', 'message': '未知错误，请重新短信验证'})

        user_logger.info('%s, %s: sms code validates successfully', phone_number, vrfcode)
        return json_dump_http_response({'status': 'success'})
