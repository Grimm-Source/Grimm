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
from datetime import datetime, timedelta
from flask import request, url_for

import server.core.db as db
import server.utils.sms_verify as sms_verify
import server.utils.tag_converter as tag_converter
from server.core import api
from server.core import wxappid, wxsecret, socketio
from server import user_logger
from server.utils.misctools import (
    json_dump_http_response,
    json_load_http_request,
)
import server.utils.db_utils as db_utils

from server.core.const import SMS_VRF_EXPIRY
from server.core.const import CAROUSEL_LIST

from server.utils.decrypt import PhoneNumberDecrypt
from flask_restx import Resource

SMS_VERIFIED_OPENID = {}


@api.route("/jscode2session")
class wxjscode2session(Resource):
    def get(self):
        """view function for validating weixin user openid"""
        js_code = request.args.get("js_code")
        if js_code is None:
            return json_dump_http_response({"status": "failure"})
        prefix = "https://api.weixin.qq.com/sns/jscode2session?appid="
        suffix = "&grant_type=authorization_code"
        url = prefix + wxappid + "&secret=" + wxsecret + "&js_code=" + js_code + suffix
        user_logger.info("user login, wxapp authorization: %s", url)
        retry = 3
        while retry > 0:
            http = urllib3.PoolManager()
            response = http.request("GET", url)
            feedback = json.loads(response.data)
            # authorization success
            if response.status == 200 and "openid" in feedback:
                break
            retry -= 1

        if retry != 0:
            feedback["server_errcode"] = 0
            openid = feedback["openid"]
            if "session_key" in feedback:
                del feedback["session_key"]
            # query user in database
            if db.exist_row("user", openid=openid):
                try:
                    userinfo = db.expr_query("user", openid=openid)[0]
                except:
                    return json_dump_http_response(
                        {"status": "failure", "message": "未知错误"}
                    )
                feedback["isRegistered"] = True
                if userinfo["audit_status"] == 0:
                    feedback["auditStatus"] = "pending"
                elif userinfo["audit_status"] == 1:
                    feedback["auditStatus"] = "approved"
                elif userinfo["audit_status"] == -1:
                    feedback["auditStatus"] = "rejected"
                feedback["role"] = "volunteer" if userinfo["role"] == 0 else "impaired"
            else:
                feedback["isRegistered"] = False
                feedback["auditStatus"] = "pending"
            feedback["status"] = "success"
            user_logger.info("%s: wxapp authorization success", openid)
        else:
            user_logger.error("wxapp authorization failed")
            feedback["status"] = "failure"

        return json_dump_http_response(feedback)


@api.route("/getPhoneNumber")
class getPhoneNumber(Resource):
    def post(self):
        """get weixin user phoneNumber"""
        info = json_load_http_request(request)  # get http POST data bytes format
        print(info)
        js_code = info["js_code"]
        encrypted_data = info["encryptedData"]
        iv = info["iv"]
        if js_code is None:
            return json_dump_http_response({"status": "failure"})
        prefix = "https://api.weixin.qq.com/sns/jscode2session?appid="
        suffix = "&grant_type=authorization_code"
        url = prefix + wxappid + "&secret=" + wxsecret + "&js_code=" + js_code + suffix
        user_logger.info("user login, wxapp authorization: %s", url)
        retry = 3
        while retry > 0:
            http = urllib3.PoolManager()
            response = http.request("GET", url)
            feedback = json.loads(response.data)
            # authorization success
            if response.status == 200 and "openid" in feedback:
                break
            retry -= 1

        if retry != 0:
            feedback["server_errcode"] = 0
            if "session_key" in feedback:
                sessionKey = feedback["session_key"]

                phone_decrypt = PhoneNumberDecrypt(wxappid, sessionKey)
                decryptData = phone_decrypt.decrypt(encrypted_data, iv)
                print(decryptData)
                feedback["decrypt_data"] = decryptData
                del feedback["session_key"]
                feedback["status"] = "success"
            else:
                user_logger.error("wxapp authorization failed")
                feedback["status"] = "failure"
        return json_dump_http_response(feedback)


@api.route("/register")
class register(Resource):
    def post(self):
        """view function for registering new user to database"""
        global SMS_VERIFIED_OPENID
        userinfo = {}
        info = json_load_http_request(request)  # get http POST data bytes format
        # fetch data from front end
        userinfo["openid"] = request.headers.get("Authorization")
        openid = userinfo["openid"]
        if not db.exist_row("user", openid=openid):
            # confirm sms-code
            # if not ('verification_code' in info or openid in SMS_VERIFIED_OPENID):
            #     user_logger.warning('%s: user registers before sms verification', openid)
            #     return json_dump_http_response({'status': 'failure', 'message': '未认证注册用户'})
            # if 'verification_code' in info:
            #     vrfcode = info['verification_code']
            #     phone_number = info['phone']
            #     sms_token = sms_verify.fetch_token(phone_number)
            #     if sms_token is None:
            #         user_logger.warning('%s: no such a sms token for number', phone_number)
            #         return json_dump_http_response({'status': 'failure', 'message': '未向该用户发送验证短信'})
            #     if sms_token.expired:
            #         user_logger.warning('%s, %s: try to validate user with expired token', phone_number, sms_token.vrfcode)
            #         sms_verify.drop_token(phone_number)
            #         return json_dump_http_response({'status': 'failure', 'message': '过期验证码'})
            #     if not sms_token.valid:
            #         user_logger.warning('%s: try to validate user with invalid token', phone_number)
            #         sms_verify.drop_token(phone_number)
            #         return json_dump_http_response({'status': 'failure', 'message': '无效验证码'})

            #     result = sms_token.validate(phone_number=phone_number, vrfcode=vrfcode)
            #     if result is not True:
            #         user_logger.warning('%s, %s: sms code validation failed, %s', phone_number, vrfcode, result)
            #         return json_dump_http_response({'status': 'failure', 'message': result })
            #     user_logger.info('%s, %s: sms code validates successfully', phone_number, vrfcode)
            #     sms_verify.drop_token(phone_number)  # drop token from pool after validation
            # else:
            #     del SMS_VERIFIED_OPENID[openid]
            # mock user info and do inserting
            # reduce part of user info to simplify register
            if info['role'] == 'volunteer': userinfo['role'] = 0
            elif info['role'] == 'impaired': userinfo['role'] = 1
            else: userinfo['role'] = 2
            # if userinfo['role'] == 1:
            # userinfo['disabled_id'] = info['disabledID']
            # userinfo['emergent_contact'] = info['emergencyPerson']
            # userinfo['emergent_contact_phone'] = info['emergencyTel']
            print("xtydbg", info)
            userinfo["birth"] = info["birthdate"] if "birthdate" in info.keys() else datetime.now().strftime("%Y-%m-%d")
            print(userinfo["birth"])
            # userinfo['remark'] = info['comment']
            userinfo["gender"] = info["gender"]
            # userinfo['idcard'] = info['idcard']
            userinfo["address"] = info["linkaddress"]
            # userinfo['contact'] = info['linktel']
            userinfo["name"] = info["name"]
            userinfo["audit_status"] = 0
            userinfo["registration_date"] = datetime.now().strftime("%Y-%m-%d")
            userinfo["phone"] = info["phone"]
            userinfo["phone_verified"] = 1
            try:
                if db.expr_insert("user", userinfo) != 1:
                    user_logger.error("%s: user registration failed", openid)
                    return json_dump_http_response(
                        {"status": "failure", "message": "录入用户失败，请重新注册"}
                    )
            except:
                user_logger.error("%s: user registration failed", openid)
                return json_dump_http_response(
                    {"status": "failure", "message": "未知错误，请重新注册"}
                )

            socketio.emit("new-users", [userinfo])
            try:
                rc = db.expr_update(
                    tbl="user", vals={"push_status": 1}, openid=userinfo["openid"]
                )
            except Exception as e:
                user_logger.error("update push_status fail, %s", e)
            user_logger.info("%s: complete user registration success", openid)
            return json_dump_http_response({"status": "success"})

        user_logger.error("%s: user is registered already", openid)
        return json_dump_http_response({"status": "failure", "message": "用户已注册，请登录"})


@api.route("/profile")
class profile(Resource):
    def get(self):
        """ display profile """
        feedback = {"status": "success"}
        openid = request.headers.get("Authorization")
        if db.exist_row("user", openid=openid):
            try:
                userinfo = db.expr_query("user", openid=openid)[0]
            except:
                return json_dump_http_response({"status": "failure", "message": "未知错误"})
            feedback["openid"] = userinfo["openid"]
            feedback["birthDate"] = str(userinfo["birth"])
            feedback["usercomment"] = userinfo["remark"]
            feedback["disabledID"] = userinfo["disabled_id"]
            feedback["emergencyPerson"] = userinfo["emergent_contact"]
            feedback["emergencyTel"] = userinfo["emergent_contact_phone"]
            feedback["gender"] = userinfo["gender"]
            feedback["idcard"] = userinfo["idcard"]
            feedback["linkaddress"] = userinfo["address"]
            feedback["linktel"] = userinfo["contact"]
            feedback["name"] = userinfo["name"]
            feedback["role"] = 'volunteer' if userinfo["role"] == 0 else 'impaired'
            feedback["phone"] = userinfo["phone"]
            feedback["registrationDate"] = str(userinfo["registration_date"])
            user_logger.info("%s: user login successfully", userinfo["openid"])
            return json_dump_http_response(feedback)

        user_logger.warning("%s: user not registered", openid)
        return json_dump_http_response({"status": "failure", "message": "用户未注册"})

    def post(self):
        " update profile"
        newinfo = json_load_http_request(request)  # get request POST user data
        openid = request.headers.get("Authorization")
        status = {}
        status["gender"] = newinfo["gender"]
        status["birth"] = newinfo["birthDate"]
        status["name"] = newinfo["name"]
        status["address"] = newinfo["linkaddress"]
        if newinfo["role"] == 'volunteer': status["role"] = 0
        elif newinfo["role"] == 'impaired': status["role"] = 1
        else: status["role"] = 2
        try:
            db.expr_update("user", vals=status, openid=openid)
        except Exception as e:
            return json_dump_http_response({"status": "failure", "message": "未知错误"})

        user_logger.info("%s: complete user profile updating successfully", openid)
        return json_dump_http_response({"status": "success"})


@api.route("/smscode")
class smscode(Resource):
    def get(self):
        """ send sms code """
        phone_number = request.args.get("phone")
        if phone_number is None:
            user_logger.warning("invalid url parameter phone_number")
            return json_dump_http_response({"status": "failure", "message": "无效url参数"})
        try:
            sms_verify.drop_token(phone_number)  # drop old token if it exists
            sms_token = sms_verify.SMSVerifyToken(
                phone_number=phone_number,
                expiry=SMS_VRF_EXPIRY,
                template="REGISTER_USER",
            )
            if not sms_token.send_sms():
                user_logger.warning("%s, unable to send sms to number", phone_number)
                return json_dump_http_response({"status": "failure", "message": "发送失败"})
        except Exception as err:
            return json_dump_http_response(
                {"status": "failure", "message": f"{err.args}"}
            )
        # append new token to pool
        sms_verify.append_token(sms_token)

        user_logger.info(
            "%s, %s: send sms to number successfully", phone_number, sms_token.vrfcode
        )
        return json_dump_http_response({"status": "success"})

    def post(self):
        """ verify sms code """
        global SMS_VERIFIED_OPENID
        data = json_load_http_request(request)
        phone_number = data["phone"]
        vrfcode = data["verification_code"]
        openid = request.headers.get("Authorization")
        sms_token = sms_verify.fetch_token(phone_number)
        if sms_token is None:
            user_logger.warning("%s: no such a sms token for number", phone_number)
            return json_dump_http_response(
                {"status": "failure", "message": "未向该用户发送验证短信"}
            )
        result = sms_token.validate(phone_number=phone_number, vrfcode=vrfcode)
        if result is not True:
            user_logger.warning(
                "%s, %s: sms code validation failed, %s", phone_number, vrfcode, result
            )
            return json_dump_http_response({"status": "failure", "message": result})
        sms_verify.drop_token(phone_number)  # drop token from pool if validated
        # try update database first, if no successful, append this openid.
        try:
            if db.expr_update("user", {"phone_verified": 1}, openid=openid) is False:
                SMS_VERIFIED_OPENID[openid] = phone_number
        except:
            user_logger.warning("%s: update user phone valid status failed", openid)
            return json_dump_http_response(
                {"status": "failure", "message": "未知错误，请重新短信验证"}
            )

        user_logger.info(
            "%s, %s: sms code validates successfully", phone_number, vrfcode
        )
        return json_dump_http_response({"status": "success"})


@api.route("/registeredActivities")
class registeredActivities(Resource):
    def post(self):
        """ register an activity """
        print(request)
        print(request.headers)
        print(request.view_args)
        openid = request.headers.get("Authorization")
        info = json_load_http_request(request)
        activity_id = info["activityId"]
        registerAct = {}
        if "needPickUp" in info.keys():
            registerAct["needpickup"] = int(info["needPickUp"])
        if "toPickUp" in info.keys():
            registerAct["topickup"] = int(info["toPickUp"])
        if "phone" in info.keys():
            registerAct["phone"] = info["phone"]
        else:
            try:
                userinfo = db.expr_query("user", openid=openid)[0]
                registerAct["phone"] = userinfo["phone"]
            except:
                return json_dump_http_response(
                    {"status": "failure", "message": "未能获取用户信息"}
                )
        if "address" in info.keys():
            registerAct["address"] = info["address"]
        else:
            try:
                userinfo = db.expr_query("user", openid=openid)[0]
                registerAct["address"] = userinfo["address"]
            except:
                return json_dump_http_response(
                    {"status": "failure", "message": "未能获取用户信息"}
                )
        registerAct["openid"] = openid
        # activity_id from network is str
        registerAct["activity_id"] = int(activity_id)
        registerAct["accepted"] = -1
        
        # Auto approve, not auto reject -- Hangzhou Backend
        try:
            activeinfo = db.expr_query("registerActivities", activity_id=int(activity_id))
            volunteer = db.expr_query(
                ["activity_participants", "user"],
                fields=[
                    "activity_participants.activity_id","user.openid"
                ],
                clauses='activity_participants.activity_id="{}" and activity_participants.participants_id = user.openid and user.role=0'.format(
                    int(activity_id)
                ),
            )

            user_logger.error("%s: volunteer", volunteer)
            if activeinfo:
                user_logger.error("%s: activeinfo", activeinfo[0])
                if len(volunteer) < activeinfo[0]["volunteer_capacity"]:
                    registerAct["accepted"] = 1
            else:
                registerAct["accepted"] = -1
        except:
            return json_dump_http_response(
                {"status": "failure", "message": "未能获取活动信息"}
            )
            
        try:
            if db.expr_insert("registerActivities", registerAct) != 1:
                user_logger.error("%s: activity registration failed", openid)
                return json_dump_http_response(
                    {"status": "failure", "message": "活动注册失败，请重新注册"}
                )
            else:
                return json_dump_http_response({"status": "success"})
        except pymysql.err.IntegrityError as e:
            if e.args[0] == 1062:
                return json_dump_http_response({"status": "failure", "message": "重复报名"})
            return json_dump_http_response(
                {"status": "failure", "message": "未知错误，请重新注册"}
            )

    def delete(self):
        """ cancel specific registered activity """
        openid = request.headers.get("Authorization")
        print("*****************deleteopenid", type(openid), openid)
        activity_id = request.args.get("activityId")
        try:
            if (
                db.expr_delete(
                    ["registerActivities"],
                    clauses='openid="{}" and activity_id={}'.format(
                        openid, activity_id
                    ),
                )
                == 1
            ):
                return json_dump_http_response({"status": "取消活动成功！"})
            else:
                return json_dump_http_response({"status": "取消活动失败！"})
        except Exception as e:
            return json_dump_http_response({"status": "取消活动失败！"})


@api.route("/activity_detail")
class get_activity(Resource):
    def get(self):
        """ get activity detail with activityId """
        openid = request.headers.get("Authorization")
        activity_id = int(request.args.get("activityId"))
        if db.exist_row("activity", activity_id=activity_id):
            try:
                activity = db.expr_query("activity", activity_id=activity_id)[0]
                if not activity:
                    user_logger.warning("%d: no such activity", activity_id)
                    return json_dump_http_response(
                        {"status": "failure", "message": "未知活动ID"}
                    )
            except:
                user_logger.warning("%d: get activity failed", activity_id)
                return json_dump_http_response({"status": "failure", "message": "未知错误"})
            feedback = db_utils.convert_db_activity_to_http_query(activity, openid)
            feedback["status"] = "success"
            user_logger.info("%d: get activity successfully", activity_id)
            return json_dump_http_response(feedback)

        user_logger.warning(
            "%d: no such activity",
            activity_id,
        )
        return json_dump_http_response({"status": "failure", "message": "未知活动ID"})


@api.route("/activity_detail/interest")
class mark_activity(Resource):
    def post(self):
        """mark activity as Insterest"""
        openid = request.headers.get("Authorization")
        activity_id = request.args.get("activityId")
        interest = request.args.get("interest")
        feedback = {"status": "success"}
        if db.exist_row(
            "activity_participants", activity_id=activity_id, participants_id=openid
        ):
            try:
                rc = db.expr_update(
                    tbl="activity_participants",
                    vals={"interested": interest},
                    activity_id=activity_id,
                    participants_id=openid,
                )
                return json_dump_http_response(feedback)
            except Exception as e:
                user_logger.error("update push_status fail, %s", e)
                user_logger.info("%s: complete user registration success", openid)
        else:
            activity_participants_info = {}
            activity_participants_info["activity_id"] = activity_id
            activity_participants_info["participants_id"] = openid
            activity_participants_info["interested"] = interest
            activity_participants_info["share"] = 0
            activity_participants_info["thumbs_up"] = 0
            if db.expr_insert("activity_participants", activity_participants_info) == 1:
                user_logger.info("Create new activity_participants_info successfully")
                return json_dump_http_response(feedback)

        return json_dump_http_response({"status": "failure", "message": "未知活动ID"})


@api.route("/activity_detail/thumbs_up")
class thumbsup_activity(Resource):
    def post(self):
        """mark activity as thumbs_up"""
        openid = request.headers.get("Authorization")
        activity_id = request.args.get("activityId")
        thumbs_up = request.args.get("thumbs_up")
        feedback = {"status": "success"}
        if db.exist_row(
            "activity_participants", activity_id=activity_id, participants_id=openid
        ):
            try:
                rc = db.expr_update(
                    tbl="activity_participants",
                    vals={"thumbs_up": thumbs_up},
                    activity_id=activity_id,
                    participants_id=openid,
                )
                return json_dump_http_response(feedback)
            except Exception as e:
                user_logger.error("update push_status fail, %s", e)
                user_logger.info("%s: complete user registration success", openid)
        else:
            activity_participants_info = {}
            activity_participants_info["activity_id"] = activity_id
            activity_participants_info["participants_id"] = openid
            activity_participants_info["interested"] = 0
            activity_participants_info["share"] = 0
            activity_participants_info["thumbs_up"] = thumbs_up
            if db.expr_insert("activity_participants", activity_participants_info) == 1:
                user_logger.info("Create new activity_participants_info successfully")
                return json_dump_http_response(feedback)

        return json_dump_http_response({"status": "failure", "message": "未知活动ID"})


@api.route("/activity_detail/share")
class share_activity(Resource):
    def post(self):
        """share activity"""
        openid = request.headers.get("Authorization")
        activity_id = request.args.get("activityId")
        if db.exist_row(
            "activity_participants", activity_id=activity_id, participants_id=openid
        ):
            try:
                participants = db.expr_query(
                    "activity_participants",
                    activity_id=activity_id,
                    participants_id=openid,
                )[0]
                if not participants:
                    user_logger.warning("%d: no such activity", activity_id)
                    return json_dump_http_response({"status": "failure"})
            except Exception as e:
                print("*******************mia*****************", e)
                user_logger.warning("%d: get activity failed", activity_id)
                return json_dump_http_response({"status": "failure"})

            share_count = int(participants["share"])
            share_count += 1
            try:
                rc = db.expr_update(
                    tbl="activity_participants",
                    vals={"share": share_count},
                    activity_id=activity_id,
                    participants_id=openid,
                )
                return json_dump_http_response({"status": "success"})
            except Exception as e:
                user_logger.error("update push_status fail, %s", e)
                user_logger.info("%s: complete user registration success", openid)
        else:
            activity_participants_info = {}
            activity_participants_info["activity_id"] = activity_id
            activity_participants_info["participants_id"] = openid
            activity_participants_info["interested"] = 0
            activity_participants_info["share"] = 1
            activity_participants_info["thumbs_up"] = 0
            if db.expr_insert("activity_participants", activity_participants_info) == 1:
                user_logger.info(
                    "Create new activity_participants_info with share successfully"
                )
                return json_dump_http_response({"status": "success"})

        return json_dump_http_response({"status": "failure", "message": "未知活动ID"})


@api.route("/carousel")
class get_carousel_list(Resource):
    def get(self):
        """view function for the activity_detail"""
        user_logger.info("query all carousel info successfully")
        return json_dump_http_response(CAROUSEL_LIST)


@api.route("/myActivities")
class get_favorite_activities(Resource):
    def get(self):
        """ list my activities"""
        openid = request.headers.get("Authorization")
        target_filter = request.args.get("filter")
        if not target_filter or len(target_filter) == 0:
            target_filter = "all"
        favorite_activities_info = []
        registered_activities_info = []
        try:
            favorite_activities_info = db.expr_query(
                ["activity_participants", "activity"],
                fields=[
                    "activity.activity_id",
                    "activity.end_time",
                ],
                clauses='activity_participants.participants_id="{}" and activity_participants.activity_id = activity.activity_id and activity_participants.interested = 1'.format(
                    openid
                ),
            )
            registered_activities_info = db.expr_query(
                ["registerActivities", "activity"],
                fields=[
                    "activity.activity_id",
                    "activity.end_time",
                ],
                clauses='registerActivities.openid="{}" and registerActivities.activity_id = activity.activity_id'.format(
                    openid
                ),
            )
        except Exception as e:
            print("*******************albertdbg*****************", e)

        target_activities_info = []
        if target_filter == "favorite":
            if favorite_activities_info is not None:
                for item in favorite_activities_info:
                    target_activities_info.append(item)
        elif target_filter == "registered":
            if registered_activities_info is not None:
                for item in registered_activities_info:
                    target_activities_info.append(item)
        elif target_filter == "all":
            id_set = []
            if favorite_activities_info is not None:
                for item in favorite_activities_info:
                    target_activities_info.append(item)
                    id_set.append(item["activity.activity_id"])
            if registered_activities_info is not None:
                for item in registered_activities_info:
                    if item["activity.activity_id"] not in id_set:
                        target_activities_info.append(item)
                        id_set.append(item["activity.activity_id"])
        target_activities_info.sort(
            key=lambda item: item["activity.activity_id"], reverse=True
        )
        target_activities_info = [
            item
            for item in target_activities_info
            if datetime.today() - timedelta(days=365) < item["activity.end_time"]
        ]

        queries = []
        for item in target_activities_info:
            activity_id = item["activity.activity_id"]
            activity = db.expr_query("activity", activity_id=activity_id)[0]
            queries.append(db_utils.convert_db_activity_to_http_query(activity, openid))
        return json_dump_http_response(queries)
