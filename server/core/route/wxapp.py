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
import pymysql
from datetime import datetime
from flask import request, url_for

import server.core.db as db
import server.utils.sms_verify as sms_verify
from server.core import grimm as app
from server.core import wxappid, wxsecret, socketio
from server import user_logger
from server.utils.misctools import json_dump_http_response, json_load_http_request, calc_duration

from server.core.const import SMS_VRF_EXPIRY
from server.core.const import CAROUSEL_LIST


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
            userinfo['role'] = 0 if info['role'] == "志愿者" else 1
            if userinfo['role'] == 1:
                userinfo['disabled_id'] = info['disabledID']
                userinfo['emergent_contact'] = info['emergencyPerson']
                userinfo['emergent_contact_phone'] = info['emergencyTel']
            userinfo['birth'] = info['birthdate']
            userinfo['remark'] = info['comment']
            userinfo['gender'] = info['gender']
            userinfo['idcard'] = info['idcard']
            userinfo['address'] = info['linkaddress']
            userinfo['contact'] = info['linktel']
            userinfo['name'] = info['name']
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

            socketio.emit('new-users', [userinfo])
            try:
                rc = db.expr_update(tbl = 'user', vals = {'push_status':1}, openid = userinfo['openid'])
            except Exception as e:
                user_logger.error('update push_status fail, %s', e)
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
        openid = request.headers.get('Authorization')
        if newinfo['role'] == '视障人士':
            userinfo['disabled_id'] = newinfo['disabledID']
            userinfo['emergent_contact'] = newinfo['emergencyPerson']
            userinfo['emergent_contact_phone'] = newinfo['emergencyTel']
        userinfo['phone'] = newinfo['tel']
        userinfo['gender'] = newinfo['gender']
        userinfo['birth'] = newinfo['birthDate']
        userinfo['contact'] = newinfo['linktel']
        userinfo['address'] = newinfo['linkaddress']
        userinfo['remark'] = newinfo['usercomment']
        userinfo['idcard'] = newinfo['idcard']
        userinfo['name'] = newinfo['name']
        try:
            status = db.expr_query('user', 'audit_status', openid=openid)[0]
            if status['audit_status'] == -1:
                userinfo['audit_status'] = 0
            if db.expr_update('user', userinfo, openid=openid) != 1:
                user_logger.error('%s: user update info failed', openid)
                return json_dump_http_response({'status': 'failure', 'message': "更新失败，请重新输入"})
        except:
            return json_dump_http_response({'status': 'failure', 'message': '未知错误'})

        user_logger.info('%s: complete user profile updating successfully', openid)
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

@app.route('/registeredActivities', methods = ['POST', 'GET', 'DELETE'])
def registeredActivities():
    # register an activity
    if request.method == 'POST':
        openid = request.headers.get('Authorization')
        info = json_load_http_request(request)[0]
        print(info)
        activity_id = info['activityId']
        registerAct = {}
        if 'needPickUp' in info.keys():
            registerAct['needpickup'] = int(info['needPickUp'])
        if 'toPickUp' in info.keys():
            registerAct['topickup'] = int(info['toPickUp'])
        registerAct['phone'] = info['tel']
        registerAct['address'] = info['address']
        registerAct['openid'] = openid
        # activity_id from network is str
        registerAct['activity_id'] = int(activity_id)
        try:
            if db.expr_insert('registerActivities', registerAct) != 1:
                user_logger.error('%s: activity registration failed', openid)
                return json_dump_http_response({'status': 'failure', 'message': '活动注册失败，请重新注册'})
            else:
                return json_dump_http_response({'status': 'success'})
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:
                print('*********xtydbg********',e)
                return json_dump_http_response({'status': 'failure', 'message': '重复报名'})
            return json_dump_http_response({'status': 'failure', 'message': '未知错误，请重新注册'})
    #  view registered activities
    if request.method == 'GET':
        openid = request.headers.get('Authorization')
        activity_id = request.args.get('activityId')
        activities = []
        try:
            activities_info = db.expr_query(['registerActivities', 'activity'], fields=['activity.activity_id', 'activity.title', 'activity.start_time' ,\
                                              'activity.end_time', 'activity.content', 'activity.notice', 'activity.content', 'activity.others',\
                                              'registerActivities.needpickup', 'registerActivities.topickup', 'activity.location', 'registerActivities.phone',\
                                              'registerActivities.address'], \
                                             clauses='registerActivities.openid="{}" and registerActivities.activity_id = activity.activity_id '.format(openid))
        except Exception as e:
            print('*******************xtydbg*****************',e)
        if activities_info is None:
            return json_dump_http_response(activities)
        for item in activities_info:
            activity = {}
            print(item)
            activity['activityId'] = item['activity.activity_id']
            activity['title'] = item['activity.title']
            start = item['activity.start_time']
            end = item['activity.end_time']
            activity['start_time'] = start.strftime('%Y-%m-%d %H:%M:%S')
            activity['end_time'] = end.strftime('%Y-%m-%d %H:%M:%S')
            activity['duration'] = calc_duration(start, end)
            activity['content'] = item['activity.content']
            activity['location'] = item['activity.location']
            activity['notice'] = item['activity.notice']
            activity['others'] = item['activity.others']
            activity['tel'] = item['registerActivities.phone']
            activity['address'] = item['registerActivities.address']
            activity['needPickUp'] = item['registerActivities.needpickup']
            activity['toPickUp'] = item['registerActivities.topickup']
            activities.append(activity)
        if activity_id is not None:
            for item in activities:
                if int(activity_id) == item['activityId']:
                    return json_dump_http_response([item])
            return json_dump_http_response([])
        return json_dump_http_response(activities)
    # cancel specific registered activity
    if request.method == 'DELETE':
        openid = request.headers.get('Authorization')
        print('*****************deleteopenid', type(openid), openid)
        activity_id = request.args.get('activityId')
        try:
            if db.expr_delete(['registerActivities'], clauses='openid="{}" and activity_id={}'.format(openid, activity_id)) == 1:
                return json_dump_http_response({'status': '取消活动成功！'})
            else:
                return json_dump_http_response({'status': '取消活动失败！'})
        except Exception as e:
            print('*******************xtydbg*****************',e)
            return json_dump_http_response({'status': '取消活动失败！'})
        
        
@app.route('/activity_detail', methods = ['GET'])
def get_activity():
    '''view function for the activity_detail'''
    if request.method == 'GET':
        openid = int(request.headers.get('Authorization'))
        activity_id = int(request.args.get('activityId'))
        if db.exist_row('activity', activity_id=activity_id):
            feedback = {'status': 'success'}
            try:
                activity = db.expr_query('activity', activity_id=activity_id)[0]
                if not activity:
                    user_logger.warning('%d: no such activity', activity_id)
                    return json_dump_http_response({'status': 'failure', 'message': '未知活动ID'})
            except:
                user_logger.warning('%d: get activity failed', activity_id)
                return json_dump_http_response({'status': 'failure', 'message': '未知错误'})
            feedback['id'] = activity['activity_id']
            feedback['title'] = activity['title']
            feedback['location'] = activity['location']
            start = activity['start_time']
            end = activity['end_time']
            feedback['start_time'] = start.strftime('%Y-%m-%d %H:%M:%S')
            feedback['end_time'] = end.strftime('%Y-%m-%d %H:%M:%S')
            feedback['duration'] = calc_duration(start, end)
            feedback['content'] = activity['content']
            feedback['notice'] = activity['notice']
            feedback['others'] = activity['others']
            feedback['volunteer_capacity'] = activity['volunteer_capacity']
            feedback['vision_impaired_capacity'] = activity['vision_impaired_capacity']
            feedback['volunteers'] = 1
            feedback['vision_impaireds'] = 0
            feedback['interested'] = 0
            feedback['share'] = 0
            feedback['sign_up'] = 0
            try:
                participants = db.expr_query('activity_participants', activity_id=activity_id, participants_id=openid)[0]
                volunteer_count = db.expr_query(['activity_participants', 'user'], 'COUNT(*)', \
                                             clauses='activity_participants.activity_id = {} ' \
                                             'and activity_participants.participants_id = user.openid and user.role = 0'.format(activity_id))
                vision_impaired_count = db.expr_query(['activity_participants', 'user'], 'COUNT(*)', \
                                             clauses='activity_participants.activity_id = {} ' \
                                             'and activity_participants.participants_id = user.openid and user.role = 1'.format(activity_id))
                
                if not participants:
                    user_logger.warning('%d: no such activity', activity_id)
                    return json_dump_http_response(feedback)
            except Exception as e:
                print('*******************mia*****************', e)
                user_logger.warning('%d: get activity failed', activity_id)
                return json_dump_http_response(feedback)
            feedback['interested'] = participants['interested']
            feedback['share'] = participants['share']
            feedback['sign_up'] = participants['sign_up']
            feedback['volunteers'] = volunteer_count[0]['COUNT(*)']
            feedback['vision_impaireds'] = vision_impaired_count[0]['COUNT(*)']
            
            user_logger.info('%d: get activity successfully', activity_id)
            return json_dump_http_response(feedback)

        user_logger.warning('%d: no such activity', activity_id, )
        return json_dump_http_response({'status': 'failure', 'message': '未知活动ID'})

@app.route('/activity_detail/interest', methods = ['POST'])
def mark_activity():
    '''mark activity as Insterest'''
    if request.method == 'POST':
        openid = int(request.headers.get('Authorization'))
        activity_id = request.args.get('activityId')
        interest = request.args.get('interest')
        feedback = {'status': 'success'}
        if db.exist_row('activity_participants', activity_id = activity_id, participants_id=openid):
            try:
                rc = db.expr_update(tbl = 'activity_participants', vals = {'interested':interest}, activity_id = activity_id, participants_id=openid)
                return json_dump_http_response(feedback)
            except Exception as e:
                user_logger.error('update push_status fail, %s', e)
                user_logger.info('%s: complete user registration success', openid)
            
        return json_dump_http_response({'status': 'failure', 'message': '未知活动ID'})
    
@app.route('/activity_detail/sign_up', methods = ['POST'])
def enroll_activity():
    '''sign_up activity'''
    if request.method == 'POST':
        openid = int(request.headers.get('Authorization'))
        activity_id = request.args.get('activityId')
        sign_up = request.args.get('sign_up')
        feedback = {'status': 'success'}
        if db.exist_row('activity_participants', activity_id = activity_id, participants_id=openid):
            try:
                print('mia sign up test')
                rc = db.expr_update(tbl = 'activity_participants', vals = {'sign_up':sign_up}, activity_id = activity_id, participants_id=openid)
                return json_dump_http_response(feedback)
            except Exception as e:
                user_logger.error('update push_status fail, %s', e)
                user_logger.info('%s: complete user registration success', openid)
            
        return json_dump_http_response({'status': 'failure', 'message': '未知活动ID'})

@app.route('/activity_detail/share', methods = ['POST'])
def share_activity():
    '''share activity'''
    if request.method == 'POST':
        openid = int(request.headers.get('Authorization'))
        activity_id = request.args.get('activityId')
        is_share = int(request.args.get('share'))
        if db.exist_row('activity_participants', activity_id = activity_id, participants_id=openid):
            try:
                participants = db.expr_query('activity_participants', activity_id=activity_id, participants_id=openid)[0]
                if not participants:
                    user_logger.warning('%d: no such activity', activity_id)
                    return json_dump_http_response({'status': 'failure'})
            except Exception as e:
                print('*******************mia*****************', e)
                user_logger.warning('%d: get activity failed', activity_id)
                return json_dump_http_response({'status': 'failure'})
        
            share_count = int(participants['share'])
            if is_share == 1:
                share_count = share_count+1
            else:
                share_count = share_count-1
            try:
                rc = db.expr_update(tbl = 'activity_participants', vals = {'share':share_count}, activity_id = activity_id, participants_id=openid)
                return json_dump_http_response({'status': 'success'})
            except Exception as e:
                user_logger.error('update push_status fail, %s', e)
                user_logger.info('%s: complete user registration success', openid)
            
        return json_dump_http_response({'status': 'failure', 'message': '未知活动ID'})

@app.route('/carousel', methods = ['GET'])
def get_carousel_list():
    '''view function for the activity_detail'''
    if request.method == 'GET':
        user_logger.info('query all carousel info successfully')
        return json_dump_http_response(CAROUSEL_LIST)