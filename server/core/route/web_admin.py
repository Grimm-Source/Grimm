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

# import sys
# import os
# import urllib3
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
import server.utils.db_utils as db_utils
import server.utils.certification_generate as certification_generate
from server.core import api
from server.core import socketio
from server import admin_logger, user_logger
from server.utils.misctools import (
    json_dump_http_response,
    json_load_http_request,
)

from server.core.const import EMAIL_VRF_EXPIRY, COM_SIGNATURE
from flask_restx import Resource


@socketio.on("disconnect")
def notice_disconnect():
    print("Client disconnect", request.sid)


@socketio.on("connect")
def notice_connect():
    print("Client connecetd")
    try:
        unau_users = db.expr_query("user", push_status=0)
    except:
        user_logger.error("Critical: database query failed !")
    unauusers = []
    if unau_users is not None:
        for user in unau_users:
            theuser = {}
            if user is not None:
                theuser["openid"] = user["openid"]
                theuser["name"] = user["name"]
                regdate = user["registration_date"]
                theuser["registrationDate"] = regdate.strftime("%Y-%m-%d")
                theuser["phone"] = user["phone"]
                unauusers.append(theuser)
    emit("new-users", unauusers)
    for user in unauusers:
        try:
            rc = db.expr_update(
                tbl="user", vals={"push_status": 1}, openid=user["openid"]
            )
        except Exception as e:
            print(e)


@api.route("/login")
class admin_login(Resource):
    def post(self):
        """view funciton for admin logging"""
        info = json_load_http_request(request)  # Get user POST info
        feedback = {"status": "success"}
        if db.exist_row("admin", email=info["email"]):
            try:
                admininfo = db.expr_query("admin", email=info["email"])[0]
            except:
                admin_logger.error("Critical: database query failed !")
                return json_dump_http_response({"status": "failure", "message": "未知错误"})
            input_password = info["password"]
            if password.verify_password(input_password, "admin", email=info["email"]):
                if admininfo["email_verified"]:
                    feedback["id"] = admininfo["id"]
                    feedback["email"] = admininfo["email"]
                    feedback["type"] = (
                        "root" if admininfo["id"] == 0 else "normal"
                    )
                    admin_logger.info(
                        "%d, %s: admin login successfully",
                        admininfo["id"],
                        admininfo["name"],
                    )
                else:
                    feedback["message"] = "请先认证邮箱"
                    admin_logger.warning(
                        "%d, %s: admin login failed, email not verified",
                        admininfo["id"],
                        admininfo["name"],
                    )
            else:
                feedback["message"] = "密码错误"
                admin_logger.warning(
                    "%d, %s: admin login failed, wrong password",
                    admininfo["id"],
                    admininfo["name"],
                )
        else:
            feedback["message"] = "未注册邮箱"
            admin_logger.warning("%s: no such admin account", info["email"])

        if "message" in feedback:
            feedback["status"] = "failure"
        return json_dump_http_response(feedback)


@api.route("/admins")
class admins(Resource):
    def get(self):
        """view function to display all admins profile"""
        try:
            adminsinfo = db.expr_query("admin")
        except:
            admin_logger.error("Critical: database query failed !")
            return json_dump_http_response({"status": "failure", "message": "未知错误"})
        queries = []
        admin_logger.info("query all admin info successfully")
        for admin in adminsinfo:
            query = {}
            query["id"] = admin["id"]
            query["email"] = admin["email"]
            query["type"] = "root" if admin["id"] == 0 else "normal"
            query["name"] = admin["name"]
            query["email_verified"] = admin["email_verified"]
            queries.append(query)

        return json_dump_http_response(queries)


@api.route("/admin/<int:admin_id>")
class manage_admin(Resource):
    def get(self, admin_id):
        """ get admin info with a specific admin_id """
        feedback = {"status": "success"}
        if db.exist_row("admin", id=admin_id):
            try:
                admininfo = db.expr_query("admin", id=admin_id)[0]
                if not admininfo:
                    admin_logger.warning("%d, no such admin id", admin_id)
                    return json_dump_http_response(
                        {"status": "failure", "message": "未知管理员"}
                    )
            except:
                admin_logger.error("Critical: database query failed !")
                return json_dump_http_response({"status": "failure", "message": "未知错误"})
            feedback["id"] = admininfo["id"]
            feedback["email"] = admininfo["email"]
            feedback["type"] = "root" if admininfo["id"] == 0 else "normal"
            admin_logger.info(
                "%d, %s: query admin info successfully",
                admininfo["id"],
                admininfo["name"],
            )
        else:
            admin_logger.warning("%d: query admin info failed", admin_id)
            feedback["status"] = "failure"

        admin_logger.warning("%d, no such admin", admin_id)
        return json_dump_http_response(feedback)

    def delete(self, admin_id):
        """ delete admin with a admin_id"""
        if admin_id != 0:
            try:
                if db.expr_delete("admin", id=admin_id) == 1:
                    admin_logger.info("%d: admin deleted successfully", admin_id)
                    return json_dump_http_response({"status": "success"})
            except:
                admin_logger.error("Critical: database delete failed !")
                feedback = {"status": "failure", "message": "未知错误"}
        else:
            admin_logger.warning("try to delete root user!")
            feedback = {"status": "failure", "message": "不能删除root用户"}

        return json_dump_http_response(feedback)


@api.route("/user")
class manage_user(Resource):
    def delete(self):
        """ delete user with an openid"""
        openid = request.args.get("openid")
        if openid is not None:
            try:
                if db.expr_delete("user", openid=openid) == 1:
                    admin_logger.info("%d: user deleted successfully", openid)
                    return json_dump_http_response({"status": "success"})
            except:
                admin_logger.error("Critical: database delete failed !")
                json_dump_http_response({"status": "failure", "message": "无法删除用户"})

        return json_dump_http_response({"status": "failure", "message": "openid 为空"})

@api.route("/admin")
class new_admin(Resource):
    def post(self):
        """view function to create new admin"""
        info = json_load_http_request(request)
        admininfo = feedback = {}
        admininfo["email"] = info["email"]
        # add new row if current admin is new
        if not db.exist_row("admin", email=admininfo["email"]):
            sql = "select max(id) from admin"
            try:
                max_admin_id = db.query(sql)[0]
            except:
                return json_dump_http_response({"status": "failure", "message": "未知错误"})
            admininfo["id"] = max_admin_id + 1  # new admin id
            admininfo["registration_date"] = datetime.now().strftime("%Y-%m-%d")
            admininfo["name"] = (
                f"管理员{max_admin_id + 1}"
                if "name" not in info or info["name"] is None
                else info["name"]
            )
            # do database inserting
            try:
                if db.expr_insert("admin", admininfo) != 1:
                    admin_logger.warning(
                        "%d, %s: create new admin failed",
                        admininfo["id"],
                        admininfo["name"],
                    )
                    return json_dump_http_response(
                        {"status": "failure", "message": "录入管理员失败"}
                    )
            except:
                admin_logger.error("Critical: database insert failed !")
                return json_dump_http_response({"status": "failure", "message": "未知错误"})
            # update passcode
            if not password.update_password(
                info["password"], "admin", id=admininfo["id"]
            ):
                admin_logger.warning(
                    "%d, %s: not strong policy password",
                    admininfo["id"],
                    admininfo["name"],
                )
                return json_dump_http_response(
                    {"status": "failure", "message": "密码不合规范"}
                )
            # send confirm email
            try:
                email_verify.drop_token(admininfo["email"])
                email_token = email_verify.EmailVerifyToken(
                    admininfo["email"], expiry=EMAIL_VRF_EXPIRY
                )  # 2hrs expiry
                if not email_token.send_email():
                    admin_logger.warning(
                        "%d, %s: send confirm email failed",
                        admininfo["id"],
                        admininfo["email"],
                    )
                    return json_dump_http_response(
                        {"status": "failure", "message": "发送验证邮箱失败"}
                    )
            except Exception as err:
                admin_logger.warning(
                    "%d, %s: send confirm email failed",
                    admininfo["id"],
                    admininfo["email"],
                )
                return json_dump_http_response(
                    {"status": "failure", "message": f"{err.args}"}
                )
            admin_logger.info(
                "%d, %s: send confirm email successfully",
                admininfo["id"],
                admininfo["email"],
            )
            email_verify.append_token(email_token)
            admin_logger.info(
                "%d, %s: create new admin procedure completed successfully",
                admininfo["id"],
                admininfo["name"],
            )
            return json_dump_http_response({"status": "success"})

        admin_logger.warning(
            "%s: create new admin with duplicated email account", admininfo["email"]
        )
        return json_dump_http_response({"status": "failure", "message": "已注册邮箱"})


@api.route("/admin-email")
class send_vrfemail(Resource):
    def get(self):
        """ view function to send and verify admin email"""
        feedback = {"status": "success"}
        # send confirm email
        send_addr = request.args.get('email')
        if send_addr:
            if db.exist_row("admin", email=send_addr):
                try:
                    email_verify.drop_token(send_addr)
                    email_token = email_verify.EmailVerifyToken(
                        send_addr, expiry=EMAIL_VRF_EXPIRY
                    )  # 2hrs expiry
                    if not email_token.send_email():
                        admin_logger.warning("%s: send confirm email failed", send_addr)
                        return json_dump_http_response(
                            {"status": "failure", "message": "发送验证邮件失败"}
                        )
                except Exception as err:
                    admin_logger.warning("%s: send confirm email failed", send_addr)
                    return json_dump_http_response(
                        {"status": "failure", "message": f"{err.args}"}
                    )
                admin_logger.info("%s: send confirm email successfully", send_addr)
                email_verify.append_token(email_token)
                return json_dump_http_response(feedback)
            else:
                admin_logger.warning("%s: email is not registered", send_addr)
                feedback = {"status": "failure", "message": "未注册邮箱"}

        # verify email link
        recv_email_token = request.args.get('verify_token')
        if recv_email_token:
            if email_verify.validate_email(recv_email_token):
                admin_logger.info(
                    "%s: email verify successfully", vrfcode.parse_vrftoken(recv_email_token)
                )
            else:
                admin_logger.warning(
                    "%s: email verify failed", vrfcode.parse_vrftoken(recv_email_token)
                )
                feedback = {"status": "failure", "message": "邮箱验证失败"}

        return json_dump_http_response(feedback)


@api.route("/activity")
class new_activity(Resource):
    def post(self):
        """view function to add new activity"""
        info = json_load_http_request(request)
        activity_info = {}
        activity_info["approver"] = info["adminId"]
        activity_info["title"] = info["title"]
        activity_info["location"] = info["location"]
        activity_info["sign_in_radius"] = info["sign_in_radius"]
        activity_info["start_time"] = info["start_time"]
        activity_info["end_time"] = info["end_time"]
        activity_info["content"] = info["content"]
        activity_info["notice"] = info["notice"]
        activity_info["others"] = info["others"]
        activity_info["admin_raiser"] = info["adminId"]
        activity_info["tag_ids"] = tag_converter.convert_tagstring_to_idstring(
            info["tag"]
        )
        activity_info["volunteer_capacity"] = info["volunteer_capacity"]
        activity_info["vision_impaired_capacity"] = info["vision_impaired_capacity"]
        activity_info["volunteer_job_title"] = info["volunteer_job_title"]
        activity_info["volunteer_job_content"] = info["volunteer_job_content"]
        activity_info["activity_fee"] = info["activity_fee"] if 'activity_fee' in info else 0
        try:
            if db.expr_insert("activity", activity_info) == 1:
                admin_logger.info(
                    "%s: create new activity successfully", activity_info["title"]
                )
                return json_dump_http_response({"status": "success"})
        except:
            pass

        admin_logger.warning("%s: create new activity failed", activity_info["title"])
        return json_dump_http_response({"status": "failure", "message": "未知错误"})


@api.route("/activity/<int:activity_id>", methods=["POST", "GET", "DELETE"])
class activity(Resource):
    def get(self, activity_id):
        """ get a activity with a specific id """
        if db.exist_row("activity", id=activity_id):
            try:
                activity = db.expr_query("activity", id=activity_id)[0]
                if not activity:
                    admin_logger.warning("%d: no such activity", activity_id)
                    return json_dump_http_response(
                        {"status": "failure", "message": "未知活动ID"}
                    )
            except:
                admin_logger.warning("%d: get activity failed", activity_id)
                return json_dump_http_response({"status": "failure", "message": "未知错误"})
            feedback = db_utils.convert_db_activity_to_http_query(activity)

            admin_logger.info("%d: get activity successfully", activity_id)
            return json_dump_http_response(feedback)

        admin_logger.warning("%d: no such activity", activity_id)
        return json_dump_http_response({"status": "failure", "message": "无效活动 ID"})

    def delete(self, activity_id):
        """ delete a activity with a specific id """
        try:
            if db.expr_delete("activity", id=activity_id) == 1:
                admin_logger.info("%d: delete new activity successfully", activity_id)
                return json_dump_http_response({"status": "success"})
        except:
            pass

        admin_logger.warning("%d: delete new activity failed", activity_id)
        return json_dump_http_response({"status": "failure", "message": "未知错误"})

    def post(self, activity_id):
        """ update a activity with a specific id """
        feedback = {"status": "failure", "message": "无效活动 ID"}
        if db.exist_row("activity", id=activity_id):
            newinfo = json_load_http_request(request)
            activity_info = {}
            activity_info["approver"] = newinfo["adminId"]
            activity_info["title"] = newinfo["title"]
            activity_info["location"] = newinfo["location"]
            activity_info["sign_in_radius"] = newinfo["sign_in_radius"]
            activity_info["start_time"] = newinfo["start_time"]
            activity_info["end_time"] = newinfo["end_time"]
            activity_info["content"] = newinfo["content"]
            activity_info["notice"] = newinfo["notice"]
            activity_info["others"] = newinfo["others"]
            activity_info["admin_raiser"] = newinfo["adminId"]
            activity_info["tag_ids"] = tag_converter.convert_tagstring_to_idstring(
                newinfo["tag"]
            )
            activity_info["volunteer_capacity"] = newinfo["volunteer_capacity"]
            activity_info["vision_impaired_capacity"] = newinfo[
                "vision_impaired_capacity"
            ]
            activity_info["volunteer_job_title"] = newinfo["volunteer_job_title"]
            activity_info["volunteer_job_content"] = newinfo["volunteer_job_content"]
            activity_info["activity_fee"] = newinfo["activity_fee"]
            try:
                if (
                    db.expr_update("activity", activity_info, id=activity_id)
                    == 1
                ):
                    admin_logger.info("%d: update activity successfully", activity_id)
                    return json_dump_http_response({"status": "success"})
            except:
                feedback = {"status": "failure", "message": "未知错误"}

        admin_logger.warning("%d: update activity failed", activity_id)
        return json_dump_http_response(feedback)


@api.route("/activities")
class activities(Resource):
    def get(self):
        """view function to get activities info"""
        try:
            activities_info = db.expr_query("activity")
        except:
            admin_logger.warning("get all activities failed")
            return json_dump_http_response({"status": "failure", "message": "未知错误"})
        keyword = request.args.get("keyword")
        queries = []
        if not activities_info: return json_dump_http_response(queries)

        if keyword and len(keyword) != 0:
            queries = [
                db_utils.convert_db_activity_to_http_query(activity)
                for activity in activities_info
                if should_append_by_keyword(activity, keyword)
            ]
            admin_logger.info("get all activities successfully")
            return json_dump_http_response(queries)

        target_tag_list = request.args.get("tags")
        if not target_tag_list or len(target_tag_list) == 0:
            target_tag_list = "all"
        filter_time = request.args.get("time")
        if not filter_time or len(filter_time) == 0:
            filter_time = "all"
        sorted_activities_info = sort_by_time(activities_info, filter_time)
        queries = [
            db_utils.convert_db_activity_to_http_query(activity)
            for activity in sorted_activities_info
            if should_append_by_tag(activity, target_tag_list)
        ]

        admin_logger.info("get all activities successfully")
        return json_dump_http_response(queries)


def sort_by_time(activities_info, filter_time):
    if filter_time == "all":
        return reversed(
            [
                activity
                for activity in activities_info
                if datetime.today() - timedelta(days=365) < activity["end_time"]
            ]
        )
    elif filter_time == "latest":
        return reversed(
            [
                activity
                for activity in activities_info
                if datetime.today() < activity["end_time"]
            ]
        )
    elif filter_time == "weekends":
        res_info = [
            activity
            for activity in activities_info
            if should_append_by_weekends(activity)
        ]
        return sorted(res_info, key=lambda activity: activity["start_time"])
    elif filter_time == "recents":
        res_info = [
            activity
            for activity in activities_info
            if should_append_by_recents(activity)
        ]
        return sorted(res_info, key=lambda activity: activity["start_time"])
    else:
        res_info = [
            activity
            for activity in activities_info
            if should_append_by_time_span(activity, filter_time)
        ]
        return sorted(res_info, key=lambda activity: activity["start_time"])


def should_append_by_tag(activity, target_tag_list):
    if not activity:
        return False
    if target_tag_list == "all":
        return True
    if activity["tag_ids"] is not None:
        current_tag_list = activity["tag_ids"].split(",")
        for target_tag_id in target_tag_list.split(","):
            if target_tag_id in current_tag_list:
                return True
    return False


def should_append_by_keyword(activity, keyword):
    if not activity:
        return False
    if keyword in activity["title"]:
        return True
    else:
        return False


def should_append_by_time_span(activity, filter_time):
    filter_start = datetime.strptime(filter_time.split(" - ")[0], "%Y-%m-%d")
    filter_end = datetime.strptime(filter_time.split(" - ")[1], "%Y-%m-%d") + timedelta(
        days=1
    )
    start = activity["start_time"]
    end = activity["end_time"]
    if filter_end < start or filter_start > end:
        return False
    return True


def should_append_by_weekends(activity):
    today = datetime.today()
    end = activity["end_time"]
    if today > end:
        return False
    start = activity["start_time"] if activity["start_time"] > today else today
    while start < end:
        if start.weekday() >= 5:
            return True
        start += timedelta(days=1)
    return False


def should_append_by_recents(activity):
    filter_start = datetime.today()
    filter_end = filter_start + timedelta(days=7)
    start = activity["start_time"]
    end = activity["end_time"]
    if filter_end < start or filter_start > end:
        return False
    return True


@api.route("/admin/<int:admin_id>/update-password")
class admin_update_password(Resource):
    def post(self, admin_id):
        """view function for admins to update new passwords"""
        admin_password = json_load_http_request(request)
        old_pass = admin_password["old_password"]
        new_pass = admin_password["new_password"]
        if db.exist_row("admin", id=admin_id):
            # check old password
            if not password.verify_password(old_pass, "admin", id=admin_id):
                admin_logger.warning("%d: wrong old password", admin_id)
                return json_dump_http_response({"status": "failure", "message": "密码错误"})
            # update passcode
            if not password.update_password(new_pass, "admin", id=admin_id):
                admin_logger.warning("%d: not strong policy password", admin_id)
                return json_dump_http_response(
                    {"status": "failure", "message": "密码不合规范"}
                )

            admin_logger.info("%d: update password successfully", admin_id)
            return json_dump_http_response({"status": "success"})

        admin_logger.warning("%d: no such admin", admin_id)
        return json_dump_http_response({"status": "failure", "message": "未知管理员"})


@api.route("/admin/forget-password")
class admin_reset_password(Resource):
    def get(self):
        """view function for admins to reset new passwords"""
        addr = request.args.get("email")
        if db.exist_row("admin", email=addr):
            response, new_pass = email_verify.send_reset(receiver=addr)
            if response:
                admin_logger.warning("%s: send reset email failed", addr)
                return json_dump_http_response(
                    {"status": "failure", "message": f"{response}"}
                )
            admin_logger.info("%s, send reset email successfully", addr)
            # update passcode
            if not password.update_password(
                new_pass, "admin", policy_check=False, email=addr
            ):
                admin_logger.warning("%s: not strong policy password", addr)
                return json_dump_http_response(
                    {"status": "failure", "message": "密码不符合规范"}
                )

            admin_logger.info("%s, update password successfully", addr)
            return json_dump_http_response({"status": "success"})

        admin_logger.warning("%s, no such admin account", addr)
        return json_dump_http_response({"status": "failure", "message": "未注册邮箱"})


@api.route("/users")
class users(Resource):
    def get(self):
        """ get wechat user list (volunteer) """
        user_type = request.args.get("role")
        if user_type == "volunteer":
            kwargs = {"role": 0}
        elif user_type == "disabled":
            kwargs = {"role": 1}
        else:
            kwargs = {}

        try:
            usersinfo = db.expr_query("user", **kwargs)
        except:
            admin_logger.error("Critical: database query failed !")
            return json_dump_http_response({"status": "failure", "message": "未知错误"})

        users = []
        if usersinfo:
            for userinfo in usersinfo:
                info = {}
                info["openid"] = userinfo["openid"]
                info["name"] = userinfo["name"]
                info["role"] = "视障人士" if userinfo["role"] == 1 else "志愿者"
                info["birthdate"] = str(userinfo["birth"])
                info["comment"] = userinfo["remark"]
                if userinfo["role"] == 1:
                    info["disabledID"] = userinfo["disabled_id"]
                info["emergencyPerson"] = userinfo["emergent_contact"]
                info["emergencyTel"] = userinfo["emergent_contact_phone"]
                info["gender"] = userinfo["gender"]
                info["idcard"] = userinfo["idcard"]
                info["linkaddress"] = userinfo["address"]
                info["linktel"] = userinfo["contact"]
                info["phone"] = userinfo["phone"]
                info["registrationDate"] = str(userinfo["registration_date"])
                info["activitiesJoined"] = userinfo["activities_joined"]
                info["activitiesAbsence"] = userinfo["activities_absence"]
                info["joindHours"] = 4 * userinfo["activities_joined"]
                if userinfo["audit_status"] == 0:
                    info["audit_status"] = "pending"
                elif userinfo["audit_status"] == 1:
                    info["audit_status"] = "approved"
                elif userinfo["audit_status"] == 2:
                    info["audit_status"] = "imported"
                elif userinfo["audit_status"] == -1:
                    info["audit_status"] = "rejected"
                else:
                    info["audit_status"] = "unknown"

                users.append(info)

            admin_logger.info("query all user info with role type successfully")
        return json_dump_http_response(users)

    def patch(self):
        """ for admin to set user audit status """
        audit_info = json_load_http_request(request)
        for audit in audit_info:
            openid = audit["openid"]
            status = audit["audit_status"]
            try:
                userinfo = db.expr_query(
                    "user", fields=("audit_status", "phone"), openid=openid
                )[0]
                if not userinfo:
                    admin_logger.warning("%s, no such user openid", openid)
                    return json_dump_http_response(
                        {"status": "failure", "message": "未知用户"}
                    )
            except:
                admin_logger.error("Critical: database query failed !")
                return json_dump_http_response({"status": "failure", "message": "未知错误"})
            # users audit new status
            if userinfo["audit_status"] == 0 and status in (
                "approved",
                "rejected",
                "pending",
            ):
                if status == "approved":
                    sms_template = "NOTIFY_APPROVED"
                    new_status = {"audit_status": 1}
                    # update each user audit status
                    try:
                        if db.expr_update("user", new_status, openid=openid) != 1:
                            admin_logger.warning(
                                "%s, update user audit status failed", openid
                            )
                            return json_dump_http_response(
                                {"status": "failure", "message": "审核状态更新失败"}
                            )
                    except:
                        admin_logger.error("Critical: update database failed")
                        return json_dump_http_response(
                            {"status": "failure", "message": "未知错误"}
                        )
                elif status == "rejected":
                    sms_template = "NOTIFY_REJECTED"
                    try:
                        if db.expr_delete("user", openid=openid) != 1:
                            admin_logger.warning("%s, delete user failed", openid)
                            return json_dump_http_response(
                                {"status": "failure", "message": "delete user failed"}
                            )
                    except Exception as e:
                        admin_logger.error("Critical: delete user failed")
                        return json_dump_http_response(
                            {"status": "failure", "message": "未知错误"}
                        )
                else:
                    continue
                # send sms message to notify user the result timely
                try:
                    sms_token = sms_verify.SMSVerifyToken(
                        phone_number=userinfo["phone"], expiry=3600
                    )
                    sms_token.template = sms_template
                    sms_token.vrfcode = ""
                    sms_token.signature = COM_SIGNATURE
                    if not sms_token.send_sms():
                        admin_logger.warning(
                            "%s, unable to send sms to number", userinfo["phone"]
                        )
                except Exception as err:
                    pass

        admin_logger.info("update users audit status successfully")
        return json_dump_http_response({"status": "success"})


@api.route("/tags")
class tags_db(Resource):
    def get(self):
        """view function to get all tags info"""
        tags_list = tag_converter.get_all_tags()
        admin_logger.info("query all tags info successfully")
        return json_dump_http_response(tags_list)


@api.route("/activityRegistration/<int:activity_id>", methods=["POST", "GET"])
class activity_registration(Resource):
    def get(self, activity_id):
        """ get an activity registration list with a specific id """
        if db.exist_row("activity", id=activity_id):
            activities_registration_list = db.expr_query(
                "registered_activity",
                activity_id=activity_id
            )
            feedback = {"status": "success"}
            users = []
            for item in activities_registration_list:
                openid = item["user_openid"]
                user_info = db.expr_query("user", openid=openid)[0]
                user = {}
                user["openid"] = openid
                user["name"] = user_info["name"]
                user["role"] = user_info["role"]
                user["phone"] = item["phone"]
                user["address"] = item["address"]
                user["accepted"] = item["accepted"]
                user["needpickup"] = item["needpickup"]
                user["topickup"] = item["topickup"]
                users.append(user)
            feedback["users"] = users
            return json_dump_http_response(feedback)

        admin_logger.warning("%d: no such activity", activity_id)
        return json_dump_http_response({"status": "failure", "message": "无效活动 ID"})
    
    def post(self, activity_id):
        """Modify user acceptance status of an activity"""
        if db.exist_row("activity", id=activity_id):
            openid = request.args.get("openid")
            accepted = request.args.get("accepted")
            if db.exist_row(
                "registered_activity", activity_id=activity_id, user_openid=openid
            ):
                try:
                    rc = db.expr_update(
                        tbl="registered_activity",
                        vals={"accepted": accepted},
                        activity_id=activity_id,
                        user_openid=openid,
                    )
                    return json_dump_http_response({"status": "success"})
                except Exception as e:
                    user_logger.error("Update registered_activity fail, %s", e)
                    return json_dump_http_response({"status": "failure", "message": "未知错误"})
            else:
                return json_dump_http_response({"status": "failure", "message": " 此人未报名"})
        else:
            return json_dump_http_response({"status": "failure", "message": "无效活动 ID"})


@api.route("/activityParticipant")
class activity_participant(Resource):
    def get(self):
        """ get an activity participant list with a participant_openid """
        participant_openid = request.args.get("participant_openid")
        try:
            activity_participant_infos = db.expr_query("activity_participant")
        except:
            admin_logger.warning("get all activity_participant info failed")
            return json_dump_http_response({"status": "failure", "message": "未知错误"})

        admin_logger.info("query all activity_participant info successfully")
        feedback = {"status": "success", "participant_openid": participant_openid, "activities": []}

        for activity_participant in activity_participant_infos:
            if activity_participant["participant_openid"] == participant_openid:
                activity_id = int(activity_participant["activity_id"])
                try:
                    activity_info = db.expr_query("activity", id=activity_id)[0]
                except:
                    admin_logger.warning("get activity info failed")
                    return json_dump_http_response({"status": "failure", "message": "未知错误"})
                activity = {"id": activity_info["id"], "title": activity_info["title"],
                            "location": activity_info["location"]}
                start = activity_info["start_time"]
                end = activity_info["end_time"]
                activity["start_time"] = start.strftime("%Y-%m-%dT%H:%M:%S")
                activity["end_time"] = end.strftime("%Y-%m-%dT%H:%M:%S")
                activity["content"] = activity_info["content"]

                activity["certificated"] = activity_participant["certificated"]

                feedback["activities"].append(activity)
                # email_verify.send("email_resource/confirm-user.html",
                # "jftt_pt@hotmail.com", "test", "test", "12345678")

        return json_dump_http_response(feedback)

    def post(self):
        """ sent certification to participant according to user's input """
        info = json_load_http_request(request)
        participant_openid = info.get("participant_openid", None)
        activity_id = info.get("activity_id", None)
        real_name = info.get("real_name", None)
        id_type = info.get("id_type", None)
        idcard = info.get("idcard", None)
        email = info.get("email", None)
        paper_certificate = info.get("paper_certificate", None)
        try:
            activity_info = db.expr_query("activity", id=activity_id)[0]
        except:
            admin_logger.warning("get activity info failed")
            return json_dump_http_response({"status": "failure", "message": "未知错误"})
        activity_title = activity_info.get("title", None)
        start = activity_info["start_time"]
        end = activity_info["end_time"]
        activity_duration = (end - start).days * 24 + (end - start).seconds//3600

        feedback = {"status": "success",
                    "participant_openid": participant_openid,
                    "activity_id": activity_id,
                    "activity_title": activity_title,
                    "real_name": real_name,
                    "id_type": id_type,
                    "idcard": idcard,
                    "email": email,
                    "paper_certificate": paper_certificate
                    }

        # Always set "certificated" to 0 when test
        db.expr_update("activity_participant", {"certificated": 0},
                       activity_id=activity_id, participant_openid=participant_openid)

        try:
            activity_participant_info = db.expr_query("activity_participant",
                                                      activity_id=activity_id,
                                                      participant_openid=participant_openid)[0]
        except:
            admin_logger.warning("get all activity_participant info failed")
            return json_dump_http_response({"status": "failure", "message": "未知错误"})

        print(activity_participant_info)

        certificated_user_info = {"real_name": real_name,
                                  "id_type": id_type,
                                  "idcard": idcard,
                                  "email": email}
        certificated_info = {"paper_certificate": paper_certificate}

        if paper_certificate:
            recipient_name = info.get("recipient_name", None)
            recipient_address = info.get("recipient_address", None)
            recipient_phone = info.get("recipient_phone", None)
            certificated_user_info["recipient_name"] = recipient_name
            certificated_user_info["recipient_address"] = recipient_address
            certificated_user_info["recipient_phone"] = recipient_phone
            feedback["recipient_name"] = recipient_name
            feedback["recipient_address"] = recipient_address
            feedback["recipient_phone"] = recipient_phone

        if not activity_participant_info["certificated"]:
            certificated_info["certificated"] = 1
            certificated_info["certificate_date"] = datetime.now().strftime("%Y-%m-%d")
            try:
                if db.expr_update("activity_participant", certificated_info,
                                  activity_id=activity_id, participant_openid=participant_openid) != 1:
                    admin_logger.warning(
                        f"participant_openid:{participant_openid} "
                        f"activity_id:{activity_id} "
                        f"update participant certificated status failed"
                    )
                    return json_dump_http_response(
                        {"status": "failure", "message": "证书状态更新失败"}
                    )
            except:
                admin_logger.error("Critical: update database failed")
                return json_dump_http_response(
                    {"status": "failure", "message": "未知错误 in activity_participant update"}
                )

            # update participant's related user info in user table
            print(certificated_user_info)
            try:
                # if db.expr_update("user", certificated_user_info, openid=participant_openid) != 1:
                #     admin_logger.warning(
                #         "%s, update user audit status failed", participant_openid
                #     )
                #     return json_dump_http_response(
                #         {"status": "failure", "message": "证书用户信息更新失败"}
                #     )
                db.expr_update("user", certificated_user_info, openid=participant_openid)
            except:
                admin_logger.error("Critical: update database failed")
                return json_dump_http_response(
                    {"status": "failure", "message": "未知错误 in user update"}
                )

            certification_info = {"name": real_name,
                                  "certificate_type": id_type,
                                  "certificate_code": idcard,
                                  "activity_title": activity_title,
                                  "activity_during": str(activity_duration) + "小时",
                                  "director": "王臻",
                                  "manager": "刘莉娟",
                                  "contact_code": "1388888888"
                                  }

            certification_file = certification_generate.generate_certification(certification_info)

            email_verify.send("email_resource/certificate-letter.html",
                              email, real_name + "'s certification",
                              "test", "12345678",
                              attachment_file=certification_file)

        return json_dump_http_response(feedback)