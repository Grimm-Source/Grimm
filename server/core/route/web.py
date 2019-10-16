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
from flask import request, url_for, redirect
import urllib3

import server.core.db as db
import server.utils.password as password
import server.utils.email_verify as email_verify
from server.core import grimm as app
from server import sys_logger


EMAIL_VRF_EXPIRY = 7200


@app.route('/login', methods=['POST'])
def admin_login():
    '''view funciton for admin logging'''
    if request.method == 'POST':
        info = json.loads(request.get_data().decode('utf8'))  # Get user POST info
        feedback = {'status': 'success'}
        if db.exist_row('admin', email=info['email']):
            try:
                admininfo = db.expr_query('admin', email=info['email'])
            except:
                sys_logger.error('Critical: database query failed !')
                return json.dumps({'status': 'failure', 'message': '未知错误'}, encoding='utf8')
            input_password = info['password']
            if password.verify_password('admin', input_password, email=info['email']):
                feedback['id'] = admininfo['admin_id']
                feedback['email'] = admininfo['email']
                feedback['type'] = 'root' if admininfo['admin_id'] == 0 else 'normal'
                feedback['email_verified'] = True if admininfo['email_verified'] else False
                sys_logger.info('%d, %s: admin login successfully', admininfo['admin_id'], admininfo['name'])
            else:
                feedback['status'] = 'failure'
                feedback['message'] = '密码错误'
                sys_logger.warning('%d, %s: admin login failed, wrong password', admininfo['admin_id'], admininfo['name'])
        else:
            feedback['status'] = 'failure'
            feedback['message'] = '账户邮箱错误'
            sys_logger.warning('%d, %s: admin login failed, wrong email account', admininfo['admin_id'], admininfo['name'])

        return json.dumps(feedback, encoding='utf8')


@app.route('/admins', methods=['GET'])
def get_all_admins():
    '''view function to display all admins profile'''
    if request.method == 'GET':
        try:
            adminsinfo = db.expr_query('admin')
        except:
            sys_logger.error('Critical: database query failed !')
            return json.dumps({'status': 'failure', 'message': '未知错误'}, encoding='utf8')
        queries = []
        sys_logger.info('query all admin info successfully')
        for admin in adminsinfo:
            query = {}
            query['id'] = admin['admin_id']
            query['email'] = admin['email']
            query['type'] = admin['account']  # ???
            queries.append(query)

        return json.dumps(queries, encoding='utf8')


@app.route('/admin/<int:admin_id>', methods=['GET', 'DELETE'])
def manage_admin(admin_id):
    '''view function for root user to manage other admins'''
    feedback = {'status': 'success'}
    if request.method == 'GET':
        if db.exist_row('admin', admin_id=admin_id):
            try:
                admininfo = db.expr_query('admin', admin_id=admin_id)
            except:
                sys_logger.error('Critical: database query failed !')
                return json.dumps({'status': 'failure', 'message': '未知错误'}, encoding='utf8')
            feedback['id'] = admininfo['admin_id']
            feedback['email'] = admininfo['email']
            feedback['type'] = 'root' if admininfo['admin_id'] == 0 else 'normal'
            sys_logger.info('%d, %s: query admin info successfully', admininfo['admin_id'], admininfo['name'])
        else:
            sys_logger.warning('%d, %s: query admin info failed', admininfo['admin_id'], admininfo['name'])
            feedback['status'] = 'failure'

        sys_logger.warning('%d, no such admin', admin_id)
        return json.dumps(feedback, encoding='utf8')

    if request.method == 'DELETE':
        if admin_id != 0:
            try:
                if db.expr_delete('admin', admin_id=admin_id) != 1:
                    feedback['status'] = 'failure'
                    feedback['message'] = '删除失败'
            except:
                sys_logger.error('Critical: database delete failed !')
                feedback = {'status': 'failure', 'message': '未知错误'}
        else:
            sys_logger.warning('try to delete root user!')
            feedback['status'] = 'failure'
            feedback['message'] = '不能删除root用户'

        sys_logger.info('%d: admin deleted successfully', admin_id)
        return json.dumps(feedback, encoding='utf8')


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
                return json.dumps({'status': 'failure', 'message': '未知错误'}, encoding='utf8')
            admininfo['admin_id'] = max_admin_id + 1  # new admin id
            admininfo['gender'] = info['gender']
            admininfo['registration_date'] = datetime.now().strftime('%Y-%m-%d')
            admininfo['name'] = f"管理员{max_admin_id + 1}" if 'name' not in info or info['name'] is None else info['name']
            # do database inserting
            try:
                if db.expr_insert('admin', admininfo) != 1:
                    sys_logger.warning('%d, %s: create new admin failed', admininfo['admin_id'], admininfo['name'])
                    return json.dumps({'status': 'failure', 'message': '录入管理员失败'}, encoding='utf8')
            except:
                sys_logger.error('Critical: database insert failed !')
                return json.dumps({'status': 'failure', 'message': '未知错误'}, encoding='utf8')
            sys_logger.info('%d, %s: create new admin successfully', admininfo['admin_id'], admininfo['name'])
            # update passcode
            if not password.update_password('admin', info['password'], admin_id=admininfo['admin_id']):
                sys_logger.warning('%d, %s: not strong policy password', admininfo['admin_id'], admininfo['name'])
                return json.dumps({'status': 'failure', 'message': '密码不符合规范'}, encoding='utf8')
            # send confirm email
            email_verify.drop_token(admininfo['email'])
            try:
                email_token = email_verify.EmailVerifyToken(admininfo['email'], expiry=EMAIL_VRF_EXPIRY)  # 2hrs expiry
                if not email_token.send_email():
                    sys_logger.warning('%d, %s: send confirm email failed', admininfo['admin_id'], admininfo['name'])
                    return json.dumps({'status': 'failure', 'message': '发送验证邮箱失败'}, encoding='utf8')
            except Exception as err:
                sys_logger.warning('%d, %s: send confirm email failed', admininfo['admin_id'], admininfo['name'])
                return json.dumps({'status': 'failure', 'message': err.args[1]}, encoding='utf8')
            sys_logger.info('%d, %s: send confirm email successfully', admininfo['admin_id'], admininfo['name'])
            email_verify.append_token(email_token)
            sys_logger.info('%d, %s: create new admin procedure completed', admininfo['admin_id'], admininfo['name'])
            return json.dumps({'status': 'success'}, encoding='utf8')

        sys_logger.warning('%s: create new admin with duplicated email account', admininfo['email'])
        return json.dumps({'status': 'failure', 'message': '已注册邮箱'}, encoding='utf8')

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
                    sys_logger.warning('%s: send confirm email failed', addr)
                    return json.dumps({'status': 'failure', 'message': '发送验证邮箱失败'}, encoding='utf8')
            except Exception as err:
                sys_logger.warning('%s: send confirm email failed', addr)
                return json.dumps({'status': 'failure', 'message': err.args[1]}, encoding='utf8')
            sys_logger.info('%s: send confirm email successfully', addr)
            email_verify.append_token(email_token)
            return json.dumps(feedback, encoding='utf8')

        sys_logger.warning('%s: email is not registered', addr)
        return json.dumps({'status': 'failure', 'message': '邮箱未注册'}, encoding='utf8')


@app.route('/confirm-email/<token>', methods=['GET'])
def confirm_email(token):
    '''view function to confirm confirm email'''
    if request.method == 'GET':
        feedback = {'status': 'success'}
        if not email_verify.validate_email(token):
            sys_logger.warning('%s: email verify failed', password.parse_vrftoken(token))
            feedback = {'status': 'failure'}

        sys_logger.info('%s: email verify successfully', password.parse_vrftoken(token))
        return json.dumps(feedback, encoding='utf8')


@app.route('/admin/delete', methods=['POST'])
def delete_admin():
    '''view function for root to delete admins'''
    if request.method == 'POST':
        feedback = {'status': 'success'}
        admin_id = json.loads(request.get_data().decode('utf8'))['id']
        if admin_id != 0:
            try:
                if db.expr_delete('admin', admin_id=admin_id) != 1:
                    sys_logger.warning('%d: delete admin failed', admin_id)
                    feedback['status'] = 'failure'
                    feedback['message'] = '删除管理员失败'
            except:
                feedback = {'status': 'failure', 'message': '未知错误'}
        else:
            sys_logger.warning('try to delete root user!')
            feedback['status'] = 'failure'
            feedback['message'] = '不能删除root用户'

        sys_logger.info('%d: delete admin successfully', admin_id)
        return json.dumps(feedback, encoding='utf8')

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
        try:
            activity_info['raiser'] = db.expr_query('admin', 'name', admin_id=info['adminId'])
        except:
            activity_info['raiser'] = 'Unknown'

        try:
            feedback = {'status': 'success'} if db.expr_insert('activity', activity_info) == 1 else {'status': 'failure', 'message': '录入失败'}
        except:
            sys_logger.warning('%s: create new activity failed', activity_info['title'])
            feedback = {'status': 'failure', 'message': '未知错误'}

        sys_logger.info('%s: create new activity successfully', activity_info['title'])
        return json.dumps(feedback, encoding='utf8')


@app.route('activity/<int:activity_id>', methods=['POST', 'GET', 'DELETE'])
def update_activity(activity_id):
    '''view function for the activity raiser to update activity info'''
    if request.method == 'GET':
        if db.exist_row('activity', activity_id='activity'):
            feedback = {'status': 'success'}
            try:
                activity_info = db.expr_query('activity', activity_id=activity_id)
            except:
                sys_logger.warning('%d: get activity failed', activity_id)
                return json.dumps({'status': 'failure', 'message': '未知错误'}, encoding='utf8')
            feedback['id'] = activity['activity_id']
            feedback['adminId'] = acitivity['approver']
            feedback['title'] = activity['title']
            feedback['location'] = activity['location']
            feedback['date'] = activity['time']
            feedback['duration'] = activity['duration']
            feedback['content'] = activity['content']
            feedback['notice'] = activity['notice']
            feedback['others'] = activity['others']

            sys_logger.info('%d: get activity successfully', activity_id)
            return json.dumps(feedback, encoding='utf8')

        sys_logger.warning('%d: no such activity', activity_id)
        return json.dumps({'status': 'failure', 'message': '无效活动ID'}, encoding='utf8')

    if request.method == 'DELETE':
        try:
            feedback = {'status': 'success'} if db.expr_delete('activity', activity_id=activity_id) == 1 else {'status': 'failure', 'message': '删除失败'}
        except:
            sys_logger.warning('%d: delete activity failed', activity_id)
            feedback = {'status': 'failure', 'message': '未知错误'}

        sys_logger.info('%d: delete activity successfully', activity_id)
        return json.dumps(feedback, encoding='utf8')

    if request.method == 'POST':
        newinfo = json.loads(request.get_data().decode('utf8'))
        activity_info = {}
        activity_info['approver'] = newinfo['adminId']
        try:
            activity_info['raiser'] = db.expr_query('admin', 'name', admin_id=info['adminId'])
        except:
            activity_info['raiser'] = 'Unknown'
        activity_info['title'] = newinfo['title']
        activity_info['location'] = newinfo['location']
        activity_info['time'] = newinfo['date']
        activity_info['duration'] = newinfo['duration']
        activity_info['content'] = newinfo['content']
        activity_info['notice'] = newinfo['notice']
        activity_info['others'] = newinfo['others']
        activity_info['activity_id'] = newinfo['id']
        try:
            feedback = {'status': 'success'} if db.expr_update('activity', activity_info, activity_id) == 1 else {'status': 'failure', 'message': '更新失败'}
        except:
            sys_logger.warning('%d: update activity failed', activity_id)
            feedback = {'status': 'failure', 'message': '未知错误'}

        sys_logger.info('%d: update activity successfully', activity_id)
        return json.dumps(feedback, encoding='utf8')


@app.route('activity/delete', methods=['DELETE'])
def delete_activity_with_id():
    '''view function to detele activity with id'''
    if request.method == 'DELETE':
        id_string = request.get_data().decode('utf8')
        if not id_string.isdigit():
            return json.dumps({'status': 'failure', 'message': '请检查活动ID'}, encoding='utf8')

        activity_id = int(id_string)
        try:
            feedback = {'status': 'success'} if db.expr_delete('activity', activity_id=activity_id) == 1 else {'status': 'failure', 'message': '删除失败'}
        except:
            sys_logger.warning('%d: delete activity failed', activity_id)
            feedback = {'status': 'failure', 'message': '未知错误'}

        sys_logger.info('%d: delete activity successfully', activity_id)
        return json.dumps(feedback, encoding='utf8')


@app.route('/activities', methods=['GET'])
def activities():
    '''view function to get all activities info'''
    if request.method == 'GET':
        try:
            activities_info = db.expr_query('activity')
        except:
            sys_logger.warning('get all activities failed')
            return json.dumps({'status': 'failure', 'message': '未知错误'}, encoding='utf8')
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

        sys_logger.info('get all activities successfully')
        return json.dumps(queries, encoding='utf8')


@app.route('/admin/<int:admin_id>/update-password', methods=['POST'])
def admin_update_password(admin_id):
    '''view function for admins to update new passwords'''
    if request.method == 'POST':
        new_pass = request.get_data().decode('utf8')
        if db.exist_row('admin', admin_id=admin_id):
            # update passcode
            if not password.update_password('admin', new_pass, admin_id=admin_id):
                sys_logger.warning('%d: not strong policy password', admin_id)
                return json.dumps({'status': 'failure', 'message': '密码不符合规范'}, encoding='utf8')

            sys_logger.info('%d: update password successfully', admin_id)
            return json.dumps({'status': 'success'}, encoding='utf8')

        sys_logger.waring('%d: no such admin', admin_id)
        return json.dumps({'status': 'failure', 'message': '未创建管理员'}, encoding='utf8')


@app.route('/admin/forget-password', methods=['POST'])
def admin_reset_password():
    '''view function for admins to reset new passwords'''
    if request.method == 'POST':
        addr = request.get_data().decode('utf8').strip()
        if db.exist_row('admin', email=addr):
            response, new_pass = email_verify.send_reset(receiver=addr)
            if response:
                sys_logger.warning('%s: send reset email failed', addr)
                return json.dumps({'status': 'failure', 'message': f'{response}'}, encoding='utf8')
            sys_logger.info('%s, send reset email successfully', addr)
            # update passcode
            if not password.update_password('admin', new_pass, email=addr):
                sys_logger.warning('%s: not strong policy password', addr)
                return json.dumps({'status': 'failure', 'message': '密码不符合规范'}, encoding='utf8')

            sys_logger.info('%s, update password successfully', addr)
            return json.dumps({'status': 'success'}, encoding='utf8')

        sys_logger.waring('%s, no such admin account', addr)
        return json.dumps({'status': 'failure', 'message': '未注册邮箱'}, encoding='utf8')
