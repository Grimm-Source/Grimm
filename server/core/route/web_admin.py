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
import time
from datetime import datetime
import json
from flask import request
import urllib3

import server.core.db as db
import server.utils.password as password
import server.utils.email_verify as email_verify
import server.utils.sms_verify as sms_verify
from server.core import grimm as app
from server import admin_logger


EMAIL_VRF_EXPIRY = 7200


@app.route('/login', methods=['POST'])
def admin_login():
    '''view funciton for admin logging'''
    if request.method == 'POST':
        info = json.loads(request.get_data().decode('utf8'))  # Get user POST info
        feedback = {'status': 'success'}
        if db.exist_row('admin', email=info['email']):
            try:
                admininfo = db.expr_query('admin', email=info['email'])[0]
            except:
                admin_logger.error('Critical: database query failed !')
                return json.dumps({'status': 'failure', 'message': '未知错误'})
            input_password = info['password']
            if password.verify_password('admin', input_password, email=info['email']):
                feedback['id'] = admininfo['admin_id']
                feedback['email'] = admininfo['email']
                feedback['type'] = 'root' if admininfo['admin_id'] == 0 else 'normal'
                feedback['email_verified'] = True if admininfo['email_verified'] else False
                admin_logger.info('%d, %s: admin login successfully', admininfo['admin_id'], admininfo['name'])
            else:
                feedback['status'] = 'failure'
                feedback['message'] = '密码错误'
                admin_logger.warning('%d, %s: admin login failed, wrong password', admininfo['admin_id'], admininfo['name'])
        else:
            feedback['status'] = 'failure'
            feedback['message'] = '未注册邮箱'
            admin_logger.warning('%s: no such admin account', info['email'])

        return json.dumps(feedback)


@app.route('/admins', methods=['GET'])
def admins():
    '''view function to display all admins profile'''
    if request.method == 'GET':
        try:
            adminsinfo = db.expr_query('admin')
        except:
            admin_logger.error('Critical: database query failed !')
            return json.dumps({'status': 'failure', 'message': '未知错误'})
        queries = []
        admin_logger.info('query all admin info successfully')
        for admin in adminsinfo:
            query = {}
            query['id'] = admin['admin_id']
            query['email'] = admin['email']
            query['type'] = 'root' if admin['admin_id'] == 0 else 'normal'
            query['name'] = admin['name']
            queries.append(query)

        return json.dumps(queries)


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
                    return json.dumps({'status': 'failure', 'message': '未知管理员'})
            except:
                admin_logger.error('Critical: database query failed !')
                return json.dumps({'status': 'failure', 'message': '未知错误'})
            feedback['id'] = admininfo['admin_id']
            feedback['email'] = admininfo['email']
            feedback['type'] = 'root' if admininfo['admin_id'] == 0 else 'normal'
            admin_logger.info('%d, %s: query admin info successfully', admininfo['admin_id'], admininfo['name'])
        else:
            admin_logger.warning('%d: query admin info failed', admin_id)
            feedback['status'] = 'failure'

        admin_logger.warning('%d, no such admin', admin_id)
        return json.dumps(feedback)

    if request.method == 'DELETE':
        if admin_id != 0:
            try:
                if db.expr_delete('admin', admin_id=admin_id) == 1:
                    admin_logger.info('%d: admin deleted successfully', admin_id)
                    return json.dumps({'status': 'success'})
            except:
                admin_logger.error('Critical: database delete failed !')
                feedback = {'status': 'failure', 'message': '未知错误'}
        else:
            admin_logger.warning('try to delete root user!')
            feedback = {'status': 'failure', 'message': '不能删除root用户'}

        return json.dumps(feedback)


@app.route('/admin', methods=['POST'])
def new_admin():
    '''view function to create new admin'''
    if request.method == 'POST':
        info = json.loads(request.get_data().decode('utf8'))
        admininfo = feedback = {}
        admininfo['email'] = info['email']
        # add new row if current admin is new
        if not db.exist_row('admin', email=admininfo['email']):
            sql = 'select max(admin_id) from admin'
            try:
                max_admin_id = db.query(sql)[0]
            except:
                return json.dumps({'status': 'failure', 'message': '未知错误'})
            admininfo['admin_id'] = max_admin_id + 1  # new admin id
            admininfo['gender'] = info['gender']
            admininfo['registration_date'] = datetime.now().strftime('%Y-%m-%d')
            admininfo['name'] = f"管理员{max_admin_id + 1}" if 'name' not in info or info['name'] is None else info['name']
            # do database inserting
            try:
                if db.expr_insert('admin', admininfo) != 1:
                    admin_logger.warning('%d, %s: create new admin failed', admininfo['admin_id'], admininfo['name'])
                    return json.dumps({'status': 'failure', 'message': '录入管理员失败'})
            except:
                admin_logger.error('Critical: database insert failed !')
                return json.dumps({'status': 'failure', 'message': '未知错误'})
            # update passcode
            if not password.update_password('admin', info['password'], admin_id=admininfo['admin_id']):
                admin_logger.warning('%d, %s: not strong policy password', admininfo['admin_id'], admininfo['name'])
                return json.dumps({'status': 'failure', 'message': '密码不合规范'})
            # send confirm email
            email_verify.drop_token(admininfo['email'])
            try:
                email_token = email_verify.EmailVerifyToken(admininfo['email'], expiry=EMAIL_VRF_EXPIRY)  # 2hrs expiry
                if not email_token.send_email():
                    admin_logger.warning('%d, %s: send confirm email failed', admininfo['admin_id'], admininfo['name'])
                    return json.dumps({'status': 'failure', 'message': '发送验证邮箱失败'})
            except Exception as err:
                admin_logger.warning('%d, %s: send confirm email failed', admininfo['admin_id'], admininfo['name'])
                return json.dumps({'status': 'failure', 'message': err.args[1]})
            admin_logger.info('%d, %s: send confirm email successfully', admininfo['admin_id'], admininfo['name'])
            email_verify.append_token(email_token)
            admin_logger.info('%d, %s: create new admin procedure completed successfully', admininfo['admin_id'], admininfo['name'])
            return json.dumps({'status': 'success'})

        admin_logger.warning('%s: create new admin with duplicated email account', admininfo['email'])
        return json.dumps({'status': 'failure', 'message': '已注册邮箱'})

# 需前端提示发送验证邮件
@app.route('/send-vrfemail', methods=['GET'])
def send_vrfemail():
    '''view function to send confirm email to user'''
    if request.method == 'GET':
        feedback = {'status': 'success'}
        addr = json.loads(request.get_data().decode('utf8'))['email']
        if db.exist_row('admin', email=addr):
            email_verify.drop_token(admininfo['email'])
            try:
                email_token = email_verify.EmailVerifyToken(addr, expiry=EMAIL_VRF_EXPIRY)  # 2hrs expiry
                if not email_token.send_email():
                    admin_logger.warning('%s: send confirm email failed', addr)
                    return json.dumps({'status': 'failure', 'message': '发送验证邮箱失败'})
            except Exception as err:
                admin_logger.warning('%s: send confirm email failed', addr)
                return json.dumps({'status': 'failure', 'message': err.args[1]})
            admin_logger.info('%s: send confirm email successfully', addr)
            email_verify.append_token(email_token)
            return json.dumps(feedback)

        admin_logger.warning('%s: email is not registered', addr)
        return json.dumps({'status': 'failure', 'message': '邮箱未注册'})


@app.route('/confirm-email/<token>', methods=['GET'])
def confirm_email(token):
    '''view function to confirm confirm email'''
    if request.method == 'GET':
        feedback = {'status': 'success'}
        if not email_verify.validate_email(token):
            admin_logger.warning('%s: email verify failed', password.parse_vrftoken(token))
            feedback = {'status': 'failure'}

        admin_logger.info('%s: email verify successfully', password.parse_vrftoken(token))
        return json.dumps(feedback)


@app.route('/admin/delete', methods=['POST'])
def delete_admin():
    '''view function for root to delete admins'''
    if request.method == 'POST':
        admin_id = json.loads(request.get_data().decode('utf8'))['id']
        if admin_id != 0:
            try:
                if db.expr_delete('admin', admin_id=admin_id) == 1:
                    admin_logger.info('%d: admin deleted successfully', admin_id)
                    return json.dumps({'status': 'success'})
            except:
                admin_logger.error('Critical: database delete failed !')
                feedback = {'status': 'failure', 'message': '未知错误'}
        else:
            admin_logger.warning('try to delete root user!')
            feedback = {'status': 'failure', 'message': '不能删除root用户'}

        return json.dumps(feedback)


@app.route('/activity', methods=['POST'])
def new_activity():
    '''view function to add new activity'''
    if request.method == 'POST':
        info = json.loads(request.get_data().decode('utf8'))
        activity_info = {}
        activity_info['approver'] = info['adminId']
        activity_info['title'] = info['title']
        activity_info['location'] = info['location']
        activity_info['time'] = info['date']
        activity_info['duration'] = info['duration']
        activity_info['content'] = info['content']
        activity_info['notice'] = info['notice']
        activity_info['others'] = info['others']
        activity_info['admin_raiser'] = info['adminId']
        try:
            if db.expr_insert('activity', activity_info) == 1:
                admin_logger.info('%s: create new activity successfully', activity_info['title'])
                return json.dumps({'status': 'success'})
        except:
            pass

        admin_logger.warning('%s: create new activity failed', activity_info['title'])
        return json.dumps({'status': 'failure', 'message': '未知错误'})


@app.route('/activity/<int:activity_id>', methods=['POST', 'GET', 'DELETE'])
def update_activity(activity_id):
    '''view function for the activity raiser to update activity info'''
    if request.method == 'GET':
        if db.exist_row('activity', activity_id='activity'):
            feedback = {'status': 'success'}
            try:
                activity = db.expr_query('activity', activity_id=activity_id)[0]
                if not activity:
                    admin_logger.warning('%d: no such activity', activity_id)
                    return json.dumps({'status': 'failure', 'message': '未知活动ID'})
            except:
                admin_logger.warning('%d: get activity failed', activity_id)
                return json.dumps({'status': 'failure', 'message': '未知错误'})
            feedback['id'] = activity['activity_id']
            feedback['adminId'] = acitivity['approver']
            feedback['title'] = activity['title']
            feedback['location'] = activity['location']
            feedback['date'] = activity['time']
            feedback['duration'] = activity['duration']
            feedback['content'] = activity['content']
            feedback['notice'] = activity['notice']
            feedback['others'] = activity['others']

            admin_logger.info('%d: get activity successfully', activity_id)
            return json.dumps(feedback)

        admin_logger.warning('%d: no such activity', activity_id)
        return json.dumps({'status': 'failure', 'message': '无效活动ID'})

    if request.method == 'DELETE':
        try:
            if db.expr_delete('activity', activity_id=activity_id) == 1:
                admin_logger.info('%d: delete new activity successfully', activity_id)
                return json.dumps({'status': 'success'})
        except:
            pass

        admin_logger.warning('%d: delete new activity failed', activity_id)
        return json.dumps({'status': 'failure', 'message': '未知错误'})

    if request.method == 'POST':
        newinfo = json.loads(request.get_data().decode('utf8'))
        activity_info = {}
        activity_info['approver'] = newinfo['adminId']
        activity_info['title'] = newinfo['title']
        activity_info['location'] = newinfo['location']
        activity_info['time'] = newinfo['date']
        activity_info['duration'] = newinfo['duration']
        activity_info['content'] = newinfo['content']
        activity_info['notice'] = newinfo['notice']
        activity_info['others'] = newinfo['others']
        activity_info['activity_id'] = newinfo['id']
        activity_info['admin_raiser'] = newinfo['adminId']
        try:
            if db.expr_update('activity', activity_info, activity_id=activity_id) == 1:
                admin_logger.info('%d: update activity successfully', activity_id)
                return json.dumps({'status': 'success'})
        except:
            pass

        admin_logger.warning('%d: update activity failed', activity_id)
        return json.dumps({'status': 'failure', 'message': '未知错误'})


@app.route('/activity/delete', methods=['DELETE'])
def delete_activity_with_id():
    '''view function to detele activity with id'''
    if request.method == 'DELETE':
        id_string = request.get_data().decode('utf8')
        if not id_string.isdigit():
            return json.dumps({'status': 'failure', 'message': '请检查活动ID'})

        activity_id = int(id_string)
        try:
            if db.expr_delete('activity', activity_id=activity_id) == 1:
                admin_logger.info('%d: delete new activity successfully', activity_id)
                return json.dumps({'status': 'success'})
        except:
            pass

        admin_logger.warning('%d: delete new activity failed', activity_id)
        return json.dumps({'status': 'failure', 'message': '未知错误'})


@app.route('/activities', methods=['GET'])
def activities():
    '''view function to get all activities info'''
    if request.method == 'GET':
        try:
            activities_info = db.expr_query('activity')
        except:
            admin_logger.warning('get all activities failed')
            return json.dumps({'status': 'failure', 'message': '未知错误'})
        queries = []
        for activity in activities_info:
            if activity is not None:
                query = {}
                query['id'] = activity['activity_id']
                query['adminId'] = activity['approver']
                query['title'] = activity['title']
                query['location'] = activity['location']
                query['date'] = activity['time']
                query['duration'] = activity['duration']
                query['content'] = activity['content']
                query['notice'] = activity['content']
                query['others'] = activity['others']

                queries.append(query)

        admin_logger.info('get all activities successfully')
        return json.dumps(queries)


@app.route('/admin/<int:admin_id>/update-password', methods=['POST'])
def admin_update_password(admin_id):
    '''view function for admins to update new passwords'''
    if request.method == 'POST':
        admin_password = json.loads(request.get_data().decode('utf8'))
        old_pass = admin_password['old_password']
        new_pass = admin_password['new_password']
        if db.exist_row('admin', admin_id=admin_id):
            # check old password
            if not password.verify_password('admin', old_pass, admin_id=admin_id):
                admin_logger.warning('%d: wrong old password', admin_id)
                return json.dumps({'status': 'failure', 'message': '密码错误'})
            # update passcode
            if not password.update_password('admin', new_pass, admin_id=admin_id):
                admin_logger.warning('%d: not strong policy password', admin_id)
                return json.dumps({'status': 'failure', 'message': '密码不合规范'})

            admin_logger.info('%d: update password successfully', admin_id)
            return json.dumps({'status': 'success'})

        admin_logger.waring('%d: no such admin', admin_id)
        return json.dumps({'status': 'failure', 'message': '未知管理员'})


@app.route('/admin/forget-password', methods=['POST'])
def admin_reset_password():
    '''view function for admins to reset new passwords'''
    if request.method == 'POST':
        addr = request.get_data().decode('utf8').strip()
        if db.exist_row('admin', email=addr):
            response, new_pass = email_verify.send_reset(receiver=addr)
            if response:
                admin_logger.warning('%s: send reset email failed', addr)
                return json.dumps({'status': 'failure', 'message': f'{response}'})
            admin_logger.info('%s, send reset email successfully', addr)
            # update passcode
            if not password.update_password('admin', new_pass, email=addr):
                admin_logger.warning('%s: not strong policy password', addr)
                return json.dumps({'status': 'failure', 'message': '密码不符合规范'})

            admin_logger.info('%s, update password successfully', addr)
            return json.dumps({'status': 'success'})

        admin_logger.waring('%s, no such admin account', addr)
        return json.dumps({'status': 'failure', 'message': '未注册邮箱'})


@app.route('/user-audit-status', methods=['GET'])
def user_audit_status():
    '''view function for admins to get all users info with audit status'''
    if request.method == 'GET':
        users = []
        query_fields = ('openid', 'name', 'role', 'audit_status')
        try:
            usersinfo = db.expr_query('user', fields=query_fields)
        except:
            admin_logger.error('Critical: database query failed !')
            return json.dumps({'status': 'failure', 'message': '未知错误'})

        for userinfo in usersinfo:
            info = {}
            info['openid'] = userinfo['openid']
            info['name'] = userinfo['name']
            info['role'] = "视障人士" if userinfo['role'] == 1 else "志愿者"
            if userinfo['audit_status'] == 0:
                info['audit_status'] = 'proceeding'
            elif userinfo['audit_status'] == 1:
                info['audit_status'] = 'approved'
            elif userinfo['audit_status'] == -1:
                info['audit_status'] = 'rejected'

            users.append(info)

        admin_logger.info('query all user audit status successfully')
        return json.dumps(users)


@app.route('/audit-user', methods=['GET', 'POST'])
def admin_audit_user():
    '''view function for admin to audit users'''
    if request.method == 'GET':
        feedback = {'status': 'success'}
        openid = json.loads(request.get_data().decode('utf8'))['openid']
        try:
            userinfo = db.expr_query('user', openid=openid)[0]
            if not userinfo:
                admin_logger.warning('%s, no such user openid', openid)
                return json.dumps({'status': 'failure', 'message': '未知用户'})
        except:
            admin_logger.error('Critical: database query failed !')
            return json.dumps({'status': 'failure', 'message': '未知错误'})

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

        admin_logger.info('%s, query user info successfully', openid)
        return json.dumps(feedback)

    if request.method == 'POST':
        audit_status = json.loads(request.get_data().decode('utf8'))
        for openid, status in audit_status.items():
            try:
                info = db.expr_query('user', ('audit_status', 'phone'), openid=openid)[0]
                if not info:
                    admin_logger.warning('%s, no such user openid', openid)
                    return json.dumps({'status': 'failure', 'message': '未知用户'})
            except:
                admin_logger.error('Critical: database query failed !')
                return json.dumps({'status': 'failure', 'message': '未知错误'})

            # users audit new status
            if info['audit_status'] == 0 and status in ('approved', 'rejected', 'proceeding'):
                if status == 'approved':
                    template = 'NOTIFY_APPROVED'
                    message = "条件合乎要求"
                    new_status = {'audit_status': 1}
                elif status == 'rejected':
                    template = 'NOTIFY_REJECTED'
                    message = "条件不合要求"
                    new_status = {'audit_status': -1}
                else:
                    continue

                # send sms message to notify user the result timely
                try:
                    sms_token = sms_verify.SMSVerifyToken(phone_number=info['phone'], expiry=3600)
                    sms_token.template = template
                    sms_token.vrfcode = message
                    if not sms_token.send_sms():
                        admin_logger.warning('%s, unable to send sms to number', info['phone'])
                        return json.dumps({'status': 'failure', 'message': '发送失败'})
                except:
                    return json.dumps({'status': 'failure', 'message': err.args[1]})

            # update each user audit status
            try:
                if db.expr_update('user', new_status, openid=openid) != 1:
                    admin_logger.warning('%s, update user audit status failed', openid)
                    return json.dumps({'status': 'failure', 'message': '更新失败'})
            except:
                admin_logger.error('Critical: update database failed')
                return json.dumps({'status': 'failure', 'message': '未知错误'})

        admin_logger.info('update users audit status successfully')
        return json.dumps({'status': 'success'})
