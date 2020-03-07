#
# File: server/core/view_function/activity.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: activity related view functions for wxapp,
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

import pymysql
from datetime import datetime
from flask import request, url_for, jsonify

import server.core.db as db
from server.core import grimm as app
from server import user_logger
from server.utils.misc import json_load_request, calc_duration, request_success, request_fail

from server.core.globals import CAROUSEL_LIST


@app.route('/registeredActivities', methods = ['POST', 'GET', 'DELETE'])
def registeredActivities():
    # register an activity
    if request.method == 'POST':
        openid = request.headers.get('Authorization')
        info = json_load_request(request)[0]
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
                return request_fail('活动注册失败，请重新注册')
            else:
                return request_success()
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:
                user_logger.warning('%s: duplicated registration', openid)
                return request_fail('重复报名')
            return request_fail('未知错误，请重新注册')
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
            return request_fail('未知错误')
        if activities_info is None:
            return jsonify(activities)
        for item in activities_info:
            activity = {}
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
                    return jsonify([item])
            return jsonify([])
        return jsonify(activities)
    # cancel specific registered activity
    if request.method == 'DELETE':
        openid = request.headers.get('Authorization')
        activity_id = request.args.get('activityId')
        try:
            if db.expr_delete('registerActivities', openid=openid, activity_id=activity_id) == 1:
                return request_success(message='取消活动成功!')
        except Exception as e:
            pass
        return request_fail('取消活动失败!')

        
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
                    return request_fail('未知活动ID')
            except:
                user_logger.warning('%d: get activity failed', activity_id)
                return request_fail('未知错误')
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
                    return jsonify(feedback)
            except Exception as e:
                print('*******************mia*****************', e)
                user_logger.warning('%d: get activity failed', activity_id)
                return jsonify(feedback)
            feedback['interested'] = participants['interested']
            feedback['share'] = participants['share']
            feedback['sign_up'] = participants['sign_up']
            feedback['volunteers'] = volunteer_count[0]['COUNT(*)']
            feedback['vision_impaireds'] = vision_impaired_count[0]['COUNT(*)']
            
            user_logger.info('%d: get activity successfully', activity_id)
            return jsonify(feedback)

        user_logger.warning('%d: no such activity', activity_id, )
        return request_fail('未知活动ID')


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
                return jsonify(feedback)
            except Exception as e:
                user_logger.error('update push_status fail, %s', e)
                user_logger.info('%s: complete user registration success', openid)
            
        return request_fail('未知活动ID')
   

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
                return jsonify(feedback)
            except Exception as e:
                user_logger.error('update push_status fail, %s', e)
                user_logger.info('%s: complete user registration success', openid)
            
        return request_fail('未知活动ID')


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
                    return request_fail('无此活动')
            except Exception as e:
                print('*******************mia*****************', e)
                user_logger.warning('%d: get activity failed', activity_id)
                return request_fail('')
        
            share_count = int(participants['share'])
            if is_share == 1:
                share_count = share_count+1
            else:
                share_count = share_count-1
            try:
                rc = db.expr_update(tbl = 'activity_participants', vals = {'share':share_count}, activity_id = activity_id, participants_id=openid)
                return request_success()
            except Exception as e:
                user_logger.error('update push_status fail, %s', e)
                user_logger.info('%s: complete user registration success', openid)
            
        return request_fail('未知活动ID')


@app.route('/carousel', methods = ['GET'])
def get_carousel_list():
    '''view function for the activity_detail'''
    if request.method == 'GET':
        user_logger.info('query all carousel info successfully')
        return jsonify(CAROUSEL_LIST)
