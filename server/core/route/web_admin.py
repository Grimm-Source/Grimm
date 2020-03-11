#
# File: web.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: all view functions for web,
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
import urllib3
from flask import request
from datetime import datetime
from datetime import timedelta
from flask_socketio import emit

import server.core.db as db
import server.utils.password as password
import server.utils.email_verify as email_verify
import server.utils.sms_verify as sms_verify
import server.utils.vrfcode as vrfcode
import server.utils.tag_converter as tag_converter
from server.core import grimm as app
from server.core import socketio
from server import admin_logger, user_logger
from server.utils.misctools import json_dump_http_response, json_load_http_request, calc_duration

from server.core.const import EMAIL_VRF_EXPIRY, COM_SIGNATURE

@socketio.on('disconnect')
def notice_disconnect():
    print('Client disconnect', request.sid)

@socketio.on('connect')
def notice_connect():
    print('Client connecetd')
    try:
        unau_users = db.expr_query('user', push_status=0)
    except:
        user_logger.error('Critical: database query failed !')
    unauusers = []
    if unau_users is not None:
        for user in unau_users:
            theuser = {}
            if user is not None:
                theuser['openid'] = user['openid']
                theuser['name'] = user['name']
                regdate = user['registration_date']
                theuser['registrationDate'] = regdate.strftime('%Y-%m-%d')
                theuser['phone'] = user['phone']
                unauusers.append(theuser)
    emit('new-users', unauusers)
    for user in unauusers:
        try:
            rc = db.expr_update(tbl = 'user', vals = {'push_status':1}, openid = user['openid'])
        except Exception as e:
            print(e)



@app.route('/')
def home():
    return json_dump_http_response({'status': 'success'})


@app.route('/login', methods=['POST'])
def admin_login():
    '''view funciton for admin logging'''
    if request.method == 'POST':
        info = json_load_http_request(request)  # Get user POST info
        feedback = {'status': 'success'}
        if db.exist_row('admin', email=info['email']):
            try:
                admininfo = db.expr_query('admin', email=info['email'])[0]
            except:
                admin_logger.error('Critical: database query failed !')
                return json_dump_http_response({'status': 'failure', 'message': '未知错误'})
            input_password = info['password']
            if password.verify_password(input_password, 'admin', email=info['email']):
                if admininfo['email_verified']:
                    feedback['id'] = admininfo['admin_id']
                    feedback['email'] = admininfo['email']
                    feedback['type'] = 'root' if admininfo['admin_id'] == 0 else 'normal'
                    admin_logger.info('%d, %s: admin login successfully', admininfo['admin_id'], admininfo['name'])
                else:
                    feedback['message'] = '请先认证邮箱'
                    admin_logger.warning('%d, %s: admin login failed, email not verified', admininfo['admin_id'], admininfo['name'])
            else:
                feedback['message'] = '密码错误'
                admin_logger.warning('%d, %s: admin login failed, wrong password', admininfo['admin_id'], admininfo['name'])
        else:
            feedback['message'] = '未注册邮箱'
            admin_logger.warning('%s: no such admin account', info['email'])

        if 'message' in feedback:
            feedback['status'] = 'failure'
        return json_dump_http_response(feedback)


@app.route('/admins', methods=['GET'])
def admins():
    '''view function to display all admins profile'''
    if request.method == 'GET':
        try:
            adminsinfo = db.expr_query('admin')
        except:
            admin_logger.error('Critical: database query failed !')
            return json_dump_http_response({'status': 'failure', 'message': '未知错误'})
        queries = []
        admin_logger.info('query all admin info successfully')
        for admin in adminsinfo:
            query = {}
            query['id'] = admin['admin_id']
            query['email'] = admin['email']
            query['type'] = 'root' if admin['admin_id'] == 0 else 'normal'
            query['name'] = admin['name']
            query['email_verified'] = admin['email_verified']
            queries.append(query)

        return json_dump_http_response(queries)


@app.route('/admin/<int:admin_id>', methods=['GET', 'DELETE'])
def manage_admin(admin_id):
    '''view function for root user to manage other admins'''
    feedback = {'status': 'success'}
    if request.method == 'GET':
        if db.exist_row('admin', admin_id=admin_id):
            try:
                admininfo = db.expr_query('admin', admin_id=admin_id)[0]
                if not admininfo:
                    admin_logger.warning('%d, no such admin id', admin_id)
                    return json_dump_http_response({'status': 'failure', 'message': '未知管理员'})
            except:
                admin_logger.error('Critical: database query failed !')
                return json_dump_http_response({'status': 'failure', 'message': '未知错误'})
            feedback['id'] = admininfo['admin_id']
            feedback['email'] = admininfo['email']
            feedback['type'] = 'root' if admininfo['admin_id'] == 0 else 'normal'
            admin_logger.info('%d, %s: query admin info successfully', admininfo['admin_id'], admininfo['name'])
        else:
            admin_logger.warning('%d: query admin info failed', admin_id)
            feedback['status'] = 'failure'

        admin_logger.warning('%d, no such admin', admin_id)
        return json_dump_http_response(feedback)

    if request.method == 'DELETE':
        if admin_id != 0:
            try:
                if db.expr_delete('admin', admin_id=admin_id) == 1:
                    admin_logger.info('%d: admin deleted successfully', admin_id)
                    return json_dump_http_response({'status': 'success'})
            except:
                admin_logger.error('Critical: database delete failed !')
                feedback = {'status': 'failure', 'message': '未知错误'}
        else:
            admin_logger.warning('try to delete root user!')
            feedback = {'status': 'failure', 'message': '不能删除root用户'}

        return json_dump_http_response(feedback)


@app.route('/admin', methods=['POST'])
def new_admin():
    '''view function to create new admin'''
    if request.method == 'POST':
        info = json_load_http_request(request)
        admininfo = feedback = {}
        admininfo['email'] = info['email']
        # add new row if current admin is new
        if not db.exist_row('admin', email=admininfo['email']):
            sql = 'select max(admin_id) from admin'
            try:
                max_admin_id = db.query(sql)[0]
            except:
                return json_dump_http_response({'status': 'failure', 'message': '未知错误'})
            admininfo['admin_id'] = max_admin_id + 1  # new admin id
            admininfo['registration_date'] = datetime.now().strftime('%Y-%m-%d')
            admininfo['name'] = f"管理员{max_admin_id + 1}" if 'name' not in info or info['name'] is None else info['name']
            # do database inserting
            try:
                if db.expr_insert('admin', admininfo) != 1:
                    admin_logger.warning('%d, %s: create new admin failed', admininfo['admin_id'], admininfo['name'])
                    return json_dump_http_response({'status': 'failure', 'message': '录入管理员失败'})
            except:
                admin_logger.error('Critical: database insert failed !')
                return json_dump_http_response({'status': 'failure', 'message': '未知错误'})
            # update passcode
            if not password.update_password(info['password'], 'admin', admin_id=admininfo['admin_id']):
                admin_logger.warning('%d, %s: not strong policy password', admininfo['admin_id'], admininfo['name'])
                return json_dump_http_response({'status': 'failure', 'message': '密码不合规范'})
            # send confirm email
            try:
                email_verify.drop_token(admininfo['email'])
                email_token = email_verify.EmailVerifyToken(admininfo['email'], expiry=EMAIL_VRF_EXPIRY)  # 2hrs expiry
                if not email_token.send_email():
                    admin_logger.warning('%d, %s: send confirm email failed', admininfo['admin_id'], admininfo['email'])
                    return json_dump_http_response({'status': 'failure', 'message': '发送验证邮箱失败'})
            except Exception as err:
                admin_logger.warning('%d, %s: send confirm email failed', admininfo['admin_id'], admininfo['email'])
                return json_dump_http_response({'status': 'failure', 'message': f"{err.args}"})
            admin_logger.info('%d, %s: send confirm email successfully', admininfo['admin_id'], admininfo['email'])
            email_verify.append_token(email_token)
            admin_logger.info('%d, %s: create new admin procedure completed successfully', admininfo['admin_id'], admininfo['name'])
            return json_dump_http_response({'status': 'success'})

        admin_logger.warning('%s: create new admin with duplicated email account', admininfo['email'])
        return json_dump_http_response({'status': 'failure', 'message': '已注册邮箱'})


@app.route('/email', methods=['GET'])
def send_vrfemail():
    '''view function to send and validate confirm email'''
    if request.method == 'GET':
        addr = request.args.get('email')
        feedback = {'status': 'success'}
        # send confirm email
        if addr is not None:
            if db.exist_row('admin', email=addr):
                try:
                    email_verify.drop_token(addr)
                    email_token = email_verify.EmailVerifyToken(addr, expiry=EMAIL_VRF_EXPIRY)  # 2hrs expiry
                    if not email_token.send_email():
                        admin_logger.warning('%s: send confirm email failed', addr)
                        return json_dump_http_response({'status': 'failure', 'message': '发送验证邮箱失败'})
                except Exception as err:
                    admin_logger.warning('%s: send confirm email failed', addr)
                    return json_dump_http_response({'status': 'failure', 'message': f"{err.args}"})
                admin_logger.info('%s: send confirm email successfully', addr)
                email_verify.append_token(email_token)
                return json_dump_http_response(feedback)

            admin_logger.warning('%s: email is not registered', addr)
            feedback = {'status': 'failure', 'message': '邮箱未注册'}
        # validate confirm email
        else:
            token = request.args.get('token')
            if not email_verify.validate_email(token):
                admin_logger.warning('%s: email verify failed', vrfcode.parse_vrftoken(token))
                return json_dump_http_response({'status': 'failure', 'message':'您的邮箱验证失败'})
            admin_logger.info('%s: email verify successfully', vrfcode.parse_vrftoken(token))

        return json_dump_http_response(feedback)


@app.route('/admin/delete', methods=['POST'])
def delete_admin():
    '''view function for root to delete admins'''
    if request.method == 'POST':
        admin_id = json_load_http_request(request, keys='id')
        if admin_id != 0:
            try:
                if db.expr_delete('admin', admin_id=admin_id) == 1:
                    admin_logger.info('%d: admin deleted successfully', admin_id)
                    return json_dump_http_response({'status': 'success'})
            except:
                admin_logger.error('Critical: database delete failed !')
                feedback = {'status': 'failure', 'message': '未知错误'}
        else:
            admin_logger.warning('try to delete root user!')
            feedback = {'status': 'failure', 'message': '不能删除root用户'}

        return json_dump_http_response(feedback)


@app.route('/activity', methods=['POST'])
def new_activity():
    '''view function to add new activity'''
    if request.method == 'POST':
        info = json_load_http_request(request)
        activity_info = {}
        activity_info['approver'] = info['adminId']
        activity_info['title'] = info['title']
        activity_info['location'] = info['location']
        activity_info['start_time'] = info['start_time']
        activity_info['end_time'] = info['end_time']
        activity_info['content'] = info['content']
        activity_info['notice'] = info['notice']
        activity_info['others'] = info['others']
        activity_info['admin_raiser'] = info['adminId']
        activity_info['tag_ids'] = tag_converter.convert_tagstring_to_idstring(info['tag'])
        try:
            if db.expr_insert('activity', activity_info) == 1:
                admin_logger.info('%s: create new activity successfully', activity_info['title'])
                return json_dump_http_response({'status': 'success'})
        except:
            pass

        admin_logger.warning('%s: create new activity failed', activity_info['title'])
        return json_dump_http_response({'status': 'failure', 'message': '未知错误'})


@app.route('/activity/<int:activity_id>', methods=['POST', 'GET', 'DELETE'])
def update_activity(activity_id):
    '''view function for the activity raiser to update activity info'''
    if request.method == 'GET':
        if db.exist_row('activity', activity_id=activity_id):
            try:
                activity = db.expr_query('activity', activity_id=activity_id)[0]
                if not activity:
                    admin_logger.warning('%d: no such activity', activity_id)
                    return json_dump_http_response({'status': 'failure', 'message': '未知活动ID'})
            except:
                admin_logger.warning('%d: get activity failed', activity_id)
                return json_dump_http_response({'status': 'failure', 'message': '未知错误'})
            feedback = convert_activity_to_query(activity)
            feedback = {'status': 'success'}

            admin_logger.info('%d: get activity successfully', activity_id)
            return json_dump_http_response(feedback)

        admin_logger.warning('%d: no such activity', activity_id)
        return json_dump_http_response({'status': 'failure', 'message': '无效活动 ID'})

    if request.method == 'DELETE':
        try:
            if db.expr_delete('activity', activity_id=activity_id) == 1:
                admin_logger.info('%d: delete new activity successfully', activity_id)
                return json_dump_http_response({'status': 'success'})
        except:
            pass

        admin_logger.warning('%d: delete new activity failed', activity_id)
        return json_dump_http_response({'status': 'failure', 'message': '未知错误'})

    if request.method == 'POST':
        if db.exist_row('activity', activity_id=activity_id):
            newinfo = json_load_http_request(request)
            activity_info = {}
            activity_info['approver'] = newinfo['adminId']
            activity_info['title'] = newinfo['title']
            activity_info['location'] = newinfo['location']
            activity_info['start_time'] = newinfo['start_time']
            activity_info['end_time'] = newinfo['end_time']
            activity_info['content'] = newinfo['content']
            activity_info['notice'] = newinfo['notice']
            activity_info['others'] = newinfo['others']
            activity_info['admin_raiser'] = newinfo['adminId']
            activity_info['tag_ids'] = tag_converter.convert_tagstring_to_idstring(newinfo['tag'])
            try:
                if db.expr_update('activity', activity_info, activity_id=activity_id) == 1:
                    admin_logger.info('%d: update activity successfully', activity_id)
                    return json_dump_http_response({'status': 'success'})
            except:
                feedback = {'status': 'failure', 'message': '未知错误'}
        else:
            feedback = {'status': 'failure', 'message': '无效活动 ID'}

        admin_logger.warning('%d: update activity failed', activity_id)
        return json_dump_http_response(feedback)


@app.route('/activity/delete', methods=['DELETE'])
def delete_activity_with_id():
    '''view function to detele activity with id'''
    if request.method == 'DELETE':
        id_string = request.get_data().decode('utf8')
        if not id_string.isdigit():
            return json_dump_http_response({'status': 'failure', 'message': '请检查活动ID'})

        activity_id = int(id_string)
        try:
            if db.expr_delete('activity', activity_id=activity_id) == 1:
                admin_logger.info('%d: delete new activity successfully', activity_id)
                return json_dump_http_response({'status': 'success'})
        except:
            pass

        admin_logger.warning('%d: delete new activity failed', activity_id)
        return json_dump_http_response({'status': 'failure', 'message': '未知错误'})


@app.route('/activities', methods=['GET'])
def activities():
    '''view function to get all activities info'''
    if request.method == 'GET':
        target_tag_list = request.args.get('tags')
        filter_time = request.args.get('time')
        weekends = request.args.get('weekends') is not None
        try:
            activities_info = db.expr_query('activity')
        except:
            admin_logger.warning('get all activities failed')
            return json_dump_http_response({'status': 'failure', 'message': '未知错误'})
        queries = []
        for activity in activities_info:
            if should_append(activity, target_tag_list, filter_time, weekends):
                query = convert_activity_to_query(activity)
                queries.append(query)

        admin_logger.info('get all activities successfully')
        return json_dump_http_response(queries)

def should_append(activity, target_tag_list, filter_time, weekends):
    should_append = False
    if not activity:
        return False
    elif not target_tag_list and not filter_time:
        should_append = True
    elif not filter_time:
        should_append = should_append_by_tag(activity, target_tag_list)
    elif not target_tag_list:
        should_append = should_append_by_time(activity, filter_time)
    else:
        should_append = should_append_by_tag(activity, target_tag_list) and should_append_by_time(activity, filter_time)
    
    if weekends:
        return should_append and should_append_by_weekends(activity)
    else:
        return should_append

def should_append_by_tag(activity, target_tag_list):
    current_tag_list = activity['tag_ids'].split(',')
    for target_tag_id in target_tag_list.split(','):
        if target_tag_id in current_tag_list:
            return True
    return False

def should_append_by_time(activity, filter_time):
    filter_start = datetime.strptime(filter_time.split(' - ')[0], '%Y-%m-%d')
    filter_end = datetime.strptime(filter_time.split(' - ')[1], '%Y-%m-%d') + timedelta(days=1)
    start = activity['start_time']
    end = activity['end_time']
    if filter_end < start or filter_start > end:
        return False
    return True

def should_append_by_weekends(activity):
    today = datetime.today()
    end = activity['end_time']
    if today > end:
        return False
    start = activity['start_time'] if activity['start_time'] > today else today
    while start < end:
        if start.weekday() >= 5:
            return True
        start += timedelta(days=1)
    return False

@app.route('/admin/<int:admin_id>/update-password', methods=['POST'])
def admin_update_password(admin_id):
    '''view function for admins to update new passwords'''
    if request.method == 'POST':
        admin_password = json_load_http_request(request)
        old_pass = admin_password['old_password']
        new_pass = admin_password['new_password']
        if db.exist_row('admin', admin_id=admin_id):
            # check old password
            if not password.verify_password(old_pass, 'admin', admin_id=admin_id):
                admin_logger.warning('%d: wrong old password', admin_id)
                return json_dump_http_response({'status': 'failure', 'message': '密码错误'})
            # update passcode
            if not password.update_password(new_pass, 'admin', admin_id=admin_id):
                admin_logger.warning('%d: not strong policy password', admin_id)
                return json_dump_http_response({'status': 'failure', 'message': '密码不合规范'})

            admin_logger.info('%d: update password successfully', admin_id)
            return json_dump_http_response({'status': 'success'})

        admin_logger.warning('%d: no such admin', admin_id)
        return json_dump_http_response({'status': 'failure', 'message': '未知管理员'})


@app.route('/admin/forget-password', methods=['GET'])
def admin_reset_password():
    '''view function for admins to reset new passwords'''
    if request.method == 'GET':
        addr = request.args.get('email')
        if db.exist_row('admin', email=addr):
            response, new_pass = email_verify.send_reset(receiver=addr)
            if response:
                admin_logger.warning('%s: send reset email failed', addr)
                return json_dump_http_response({'status': 'failure', 'message': f'{response}'})
            admin_logger.info('%s, send reset email successfully', addr)
            # update passcode
            if not password.update_password(new_pass, 'admin', policy_check=False, email=addr):
                admin_logger.warning('%s: not strong policy password', addr)
                return json_dump_http_response({'status': 'failure', 'message': '密码不符合规范'})

            admin_logger.info('%s, update password successfully', addr)
            return json_dump_http_response({'status': 'success'})

        admin_logger.warning('%s, no such admin account', addr)
        return json_dump_http_response({'status': 'failure', 'message': '未注册邮箱'})


@app.route('/users', methods=['GET', 'PATCH'])
def users():
    '''view function for admins to get all users info with role type'''
    # for admin to get user info
    if request.method == 'GET':
        user_type = request.args.get('role')
        if user_type == 'volunteer':
            kwargs = {'role': 0}
        elif user_type == 'disabled':
            kwargs = {'role': 1}
        else:
            kwargs = {}

        try:
            usersinfo = db.expr_query('user', **kwargs)
        except:
            admin_logger.error('Critical: database query failed !')
            return json_dump_http_response({'status': 'failure', 'message': '未知错误'})

        users = []
        for userinfo in usersinfo:
            info = {}
            info['openid'] = userinfo['openid']
            info['name'] = userinfo['name']
            info['role'] = "视障人士" if userinfo['role'] == 1 else "志愿者"
            info['birthdate'] = userinfo['birth']
            info['comment'] = userinfo['remark']
            info['disabledID'] = userinfo['disabled_id']
            info['emergencyPerson'] = userinfo['emergent_contact']
            info['emergencyTel'] = userinfo['emergent_contact_phone']
            info['gender'] = userinfo['gender']
            info['idcard'] = userinfo['idcard']
            info['linkaddress'] = userinfo['address']
            info['linktel'] = userinfo['contact']
            info['tel'] = userinfo['phone']
            info['registrationDate'] = userinfo['registration_date']
            if userinfo['audit_status'] == 0:
                info['audit_status'] = 'pending'
            elif userinfo['audit_status'] == 1:
                info['audit_status'] = 'approved'
            elif userinfo['audit_status'] == -1:
                info['audit_status'] = 'rejected'
            else:
                info['audit_status'] = 'unknown'

            users.append(info)

        admin_logger.info('query all user info with role type successfully')
        return json_dump_http_response(users)
    # for admin to set user audit status
    if request.method == 'PATCH':
        audit_info = json_load_http_request(request)
        for audit in audit_info:
            openid = audit['openid']
            status = audit['audit_status']
            try:
                userinfo = db.expr_query('user', fields=('audit_status', 'phone'), openid=openid)[0]
                if not userinfo:
                    admin_logger.warning('%s, no such user openid', openid)
                    return json_dump_http_response({'status': 'failure', 'message': '未知用户'})
            except:
                admin_logger.error('Critical: database query failed !')
                return json_dump_http_response({'status': 'failure', 'message': '未知错误'})
            # users audit new status
            if userinfo['audit_status'] == 0 and status in ('approved', 'rejected', 'pending'):
                if status == 'approved':
                    sms_template = 'NOTIFY_APPROVED'
                    new_status = {'audit_status': 1}
                elif status == 'rejected':
                    sms_template = 'NOTIFY_REJECTED'
                    new_status = {'audit_status': -1}
                else:
                    continue
                # update each user audit status
                try:
                    if db.expr_update('user', new_status, openid=openid) != 1:
                        admin_logger.warning('%s, update user audit status failed', openid)
                        return json_dump_http_response({'status': 'failure', 'message': '审核状态更新失败'})
                except:
                    admin_logger.error('Critical: update database failed')
                    return json_dump_http_response({'status': 'failure', 'message': '未知错误'})
                # send sms message to notify user the result timely
                try:
                    sms_token = sms_verify.SMSVerifyToken(phone_number=userinfo['phone'], expiry=3600)
                    sms_token.template = sms_template
                    sms_token.vrfcode = ''
                    sms_token.signature = COM_SIGNATURE
                    if not sms_token.send_sms():
                        admin_logger.warning('%s, unable to send sms to number', userinfo['phone'])
                except Exception as err:
                    pass

        admin_logger.info('update users audit status successfully')
        return json_dump_http_response({'status': 'success'})


@app.route('/tags', methods=['GET'])
def tags_db():
    '''view function to get all tags info'''
    if request.method == 'GET':
        tags_list = tag_converter.get_all_tags()
        admin_logger.info('query all tags info successfully')
        return json_dump_http_response(tags_list)


def convert_activity_to_query(activity):
    query = {}
    query['id'] = activity['activity_id']
    query['adminId'] = activity['approver']
    query['title'] = activity['title']
    query['location'] = activity['location']
    start = activity['start_time']
    end = activity['end_time']
    query['start_time'] = start.strftime('%Y-%m-%dT%H:%M:%S')
    query['end_time'] = end.strftime('%Y-%m-%dT%H:%M:%S')
    query['duration'] = calc_duration(start, end)
    query['content'] = activity['content']
    query['notice'] = activity['content']
    query['others'] = activity['others']
    query['tag'] = tag_converter.convert_idstring_to_tagstring(activity['tag_ids'])
    return query
