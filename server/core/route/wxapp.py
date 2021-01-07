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
        if db.exist_row('user', openid=openid):
            user_logger.error("%s: user is registered already", openid)
            return json_dump_http_response({"status": "failure", "message": "用户已注册，请登录"})

        if info['role'] == 'volunteer':
            userinfo['role'] = 0
        elif info['role'] == 'impaired':
            userinfo['role'] = 1
        else:
            userinfo['role'] = 2

        if userinfo['role'] == 1:
            userinfo['disabled_id'] = info['disabledID']
            userinfo['disabled_id_verified'] = 0
        print("xtydbg", info)
        userinfo["birth"] = info["birthdate"] if "birthdate" in info.keys() else datetime.now().strftime("%Y-%m-%d")
        # userinfo['remark'] = info['comment']
        userinfo["gender"] = info["gender"]
        # userinfo['idcard'] = info['idcard']
        userinfo["address"] = info["linkaddress"]
        # userinfo['contact'] = info['linktel']
        userinfo["name"] = info["name"]
        if 'idcard' in info:
            userinfo['idcard'] = info['idcard']
            userinfo['idcard_verified'] = 0
        userinfo["audit_status"] = 0
        userinfo["registration_date"] = datetime.now().strftime("%Y-%m-%d")
        userinfo["phone"] = info["phone"]
        userinfo["phone_verified"] = 1
        userinfo["email"] = info["email"]
        userinfo["email_verified"] = 0
        db_utils.set_openid_if_user_info_exists(openid, userinfo['idcard'], userinfo["phone"], userinfo["email"], userinfo['disabled_id'] if userinfo['role'] == 1 else None)
        if not db.exist_row("user", openid=openid):
            try:
                if db.expr_insert("user", userinfo) != 1:
                    user_logger.error("%s: user registration failed", openid)
                    return json_dump_http_response(
                        {"status": "failure", "message": "录入用户失败，请重新注册"}
                    )
            except Exception as e:
                user_logger.error("user registration failed: \n%s: ", e)
                return json_dump_http_response(
                    {"status": "failure", "message": "未知错误，请重新注册"}
                )
        else:
            # the user already improted will automatically set to approved.
            userinfo['audit_status'] = 1
            try:
                db.expr_update(tbl='user', vals=userinfo, openid=userinfo['openid'])
            except Exception as e:
                user_logger.error("user registration failed as user info already imported\n %s", e)
                return json_dump_http_response(
                    {"status": "failure", "message": "用户信息已存在，请联系管理员。"}
                )

        socketio.emit("new-users", [userinfo])
        try:
            db.expr_update(tbl="user", vals={"push_status": 1}, openid=userinfo["openid"])
        except Exception as e:
            user_logger.error("update push_status fail, %s", e)
        user_logger.info("%s: complete user registration success", openid)
        return json_dump_http_response({"status": "success"})


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
            feedback["email"] = userinfo["email"]
            feedback["registrationDate"] = str(userinfo["registration_date"])
            feedback["activitiesJoined"] = userinfo["activities_joined"]
            feedback["activitiesAbsence"] = userinfo["activities_absence"]
            feedback["joindHours"] = 4 * userinfo["activities_joined"]
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
        status["email"] = newinfo["email"]

        if newinfo["role"] == 'volunteer': status["role"] = 0
        elif newinfo["role"] == 'impaired': status["role"] = 1
        else: status["role"] = 2
        if status['role'] == 1 and newinfo['disabledID']:
            status['disabled_id'] = newinfo['disabledID']
            status['disabled_id_verified'] = 0
        if 'idcard' in newinfo:
            status['idcard'] = newinfo['idcard']
            status['idcard_verified'] = 0
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
        registerAct["user_openid"] = openid
        # activity_id from network is str
        registerAct["activity_id"] = int(activity_id)
        registerAct["accepted"] = -1
        
        # Auto approve, not auto reject -- Hangzhou Backend
        try:
            activeinfo = db.expr_query("registered_activity", activity_id=int(activity_id))
            volunteer = db.expr_query(
                ["activity_participant", "user"],
                fields=[
                    "activity_participant.activity_id","user.openid"
                ],
                clauses='activity_participant.activity_id="{}" and activity_participant.participant_openid = user.openid and user.role=0'.format(
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
            user_logger.error("%s: activeinfo no return. Skip to auto approve, insert register still",)
            #return json_dump_http_response(
            #    {"status": "failure", "message": "未能获取志愿者人数信息"}
            #)

        try:
            if db.expr_insert("registered_activity", registerAct) != 1:
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
                    ["registered_activity"],
                    clauses='user_openid="{}" and activity_id={}'.format(
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
        if db.exist_row("activity", id=activity_id):
            try:
                activity = db.expr_query("activity", id=activity_id)[0]
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
            "activity_participant", activity_id=activity_id, participant_openid=openid
        ):
            try:
                rc = db.expr_update(
                    tbl="activity_participant",
                    vals={"interested": interest},
                    activity_id=activity_id,
                    participant_openid=openid,
                )
                return json_dump_http_response(feedback)
            except Exception as e:
                user_logger.error("update push_status fail, %s", e)
                user_logger.info("%s: complete user registration success", openid)
        else:
            activity_participant_info = {}
            activity_participant_info["activity_id"] = activity_id
            activity_participant_info["participant_openid"] = openid
            activity_participant_info["interested"] = interest
            activity_participant_info["share"] = 0
            activity_participant_info["thumbs_up"] = 0
            if db.expr_insert("activity_participant", activity_participant_info) == 1:
                user_logger.info("Create new activity_participant_info successfully")
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
            "activity_participant", activity_id=activity_id, participant_openid=openid
        ):
            try:
                rc = db.expr_update(
                    tbl="activity_participant",
                    vals={"thumbs_up": thumbs_up},
                    activity_id=activity_id,
                    participant_openid=openid,
                )
                return json_dump_http_response(feedback)
            except Exception as e:
                user_logger.error("update push_status fail, %s", e)
                user_logger.info("%s: complete user registration success", openid)
        else:
            activity_participant_info = {}
            activity_participant_info["activity_id"] = activity_id
            activity_participant_info["participant_openid"] = openid
            activity_participant_info["interested"] = 0
            activity_participant_info["share"] = 0
            activity_participant_info["thumbs_up"] = thumbs_up
            if db.expr_insert("activity_participant", activity_participant_info) == 1:
                user_logger.info("Create new activity_participant_info successfully")
                return json_dump_http_response(feedback)

        return json_dump_http_response({"status": "failure", "message": "未知活动ID"})


@api.route("/activity_detail/share")
class share_activity(Resource):
    def post(self):
        """share activity"""
        openid = request.headers.get("Authorization")
        activity_id = request.args.get("activityId")
        if db.exist_row(
            "activity_participant", activity_id=activity_id, participant_openid=openid
        ):
            try:
                participant = db.expr_query(
                    "activity_participant",
                    activity_id=activity_id,
                    participant_openid=openid,
                )[0]
                if not participant:
                    user_logger.warning("%d: no such activity", activity_id)
                    return json_dump_http_response({"status": "failure"})
            except Exception as e:
                print("*******************mia*****************", e)
                user_logger.warning("%d: get activity failed", activity_id)
                return json_dump_http_response({"status": "failure"})

            share_count = int(participant["share"])
            share_count += 1
            try:
                rc = db.expr_update(
                    tbl="activity_participant",
                    vals={"share": share_count},
                    activity_id=activity_id,
                    participant_openid=openid,
                )
                return json_dump_http_response({"status": "success"})
            except Exception as e:
                user_logger.error("update push_status fail, %s", e)
                user_logger.info("%s: complete user registration success", openid)
        else:
            activity_participant_info = {}
            activity_participant_info["activity_id"] = activity_id
            activity_participant_info["participant_openid"] = openid
            activity_participant_info["interested"] = 0
            activity_participant_info["share"] = 1
            activity_participant_info["thumbs_up"] = 0
            if db.expr_insert("activity_participant", activity_participant_info) == 1:
                user_logger.info(
                    "Create new activity_participant_info with share successfully"
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
                ["activity_participant", "activity"],
                fields=[
                    "activity.id",
                    "activity.end_time",
                ],
                clauses='activity_participant.participant_openid="{}" and activity_participant.activity_id = activity.id and activity_participant.interested = 1'.format(
                    openid
                ),
            )
            registered_activities_info = db.expr_query(
                ["registered_activity", "activity"],
                fields=[
                    "activity.id",
                    "activity.end_time",
                ],
                clauses='registered_activity.user_openid="{}" and registered_activity.activity_id = activity.id'.format(
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
                    id_set.append(item["activity.id"])
            if registered_activities_info is not None:
                for item in registered_activities_info:
                    if item["activity.id"] not in id_set:
                        target_activities_info.append(item)
                        id_set.append(item["activity.id"])
        target_activities_info.sort(
            key=lambda item: item["activity.id"], reverse=True
        )
        target_activities_info = [
            item
            for item in target_activities_info
            if datetime.today() - timedelta(days=365) < item["activity.end_time"]
        ]

        queries = []
        for item in target_activities_info:
            activity_id = item["activity.id"]
            activity = db.expr_query("activity", id=activity_id)[0]
            queries.append(db_utils.convert_db_activity_to_http_query(activity, openid))
        return json_dump_http_response(queries)
