import json
import traceback

import pandas as pd
from datetime import datetime

import bcrypt
import urllib3
from flask import request, jsonify
from flask_restx import Resource

from grimm import logger, db, engine, GrimmConfig, socketio
from grimm.admin import admin, adminbiz
from grimm.admin.admindto import AdminDto
from grimm.models.admin import Admin, User
from grimm.utils import constants, smsverify, emailverify, dbutils, decrypt


@admin.route('/login', methods=['POST'])
class AdminLogin(Resource):
    @admin.doc(
        "Admin login test",
        responses={
            200: ("Logged in", AdminDto.login_success),
            403: "Incorrect password or incomplete credentials.",
            404: "Email does not match any account.",
            10086: "Email not verified."
        }
    )
    @admin.expect(AdminDto.login, validate=False)
    def post(self):
        info = json.loads(request.get_data())
        feedback = {"status": "success"}
        admin_info = Admin.query.filter(Admin.email == info["email"]).first()
        if not admin_info:
            feedback["message"] = "未注册邮箱"
            logger.warning("%s: no such admin account", info["email"])
            feedback["status"] = "failure"
            return feedback, 404
        input_password = info["password"]
        if not bcrypt.checkpw(input_password.encode('utf-8'), admin_info.password):
            feedback["message"] = "密码错误"
            feedback["status"] = "failure"
            logger.warning("%d, %s: admin login failed, wrong password", admin_info.id, admin_info.name)
            return feedback, 403
        if not admin_info.email_verified:
            feedback["message"] = "请先认证邮箱"
            feedback["status"] = "failure"
            logger.warning("%d, %s: admin login failed, email not verified", admin_info.id, admin_info.name)
            return feedback, 10086
        feedback["id"] = admin_info.id
        feedback["email"] = admin_info.email
        feedback["type"] = ("root" if admin_info.id == 1 else "normal")
        logger.info("%d, %s: admin login successfully", admin_info.id, admin_info.name)
        return feedback


@admin.route('/admins', methods=['GET'])
class GetAdmins(Resource):
    def get(self):
        """view function to display all admins profile"""
        admins_info = Admin.query.all()
        queries = []
        logger.info("query all admin info successfully")
        for admin_info in admins_info:
            query = {"id": admin_info.id,
                     "email": admin_info.email,
                     "type": "root" if admin_info.id == 1 else "normal",
                     "name": admin_info.name,
                     "email_verified": admin_info.email_verified}
            queries.append(query)
        return jsonify(queries)


@admin.route("/admin/<int:admin_id>", methods=['GET', 'DELETE'])
class ManageAdmin(Resource):
    def get(self, admin_id):
        feedback = {"status": "success"}
        admin_info = Admin.query.filter(Admin.id == admin_id).first()
        if not admin_info:
            logger.warning("%d, no such admin id", admin_id)
            return jsonify({"status": "failure", "message": "未知管理员"})
        feedback["id"] = admin_info.id
        feedback["email"] = admin_info.email
        feedback["type"] = "root" if admin_info.id == 1 else "normal"
        logger.info("%d, %s: query admin info successfully", admin_info.id, admin_info.name)
        return jsonify(feedback)

    def delete(self, admin_id):
        if admin_id != 0:
            admin_info = db.session.query(Admin).filter(Admin.id == admin_id).first()
            db.session.delete(admin_info)
            db.session.commit()
            return jsonify({"status": "success"})
        logger.warning("try to delete root user!")
        feedback = {"status": "failure", "message": "不能删除root用户"}
        return jsonify(feedback)
    
    
@admin.route("/admin", methods=['POST'])
class NewAdmin(Resource):
    def post(self):
        """view function to create new admin"""
        info = json.loads(request.get_data())
        exist_admin = Admin.query.filter(Admin.email == info["email"]).first()
        if exist_admin:
            logger.warning("%s: create new admin with duplicated email account", info["email"])
            return jsonify({"status": "failure", "message": "已注册邮箱"})

        # add new row if current admin is new
        sql = "select max(id) max_admin_id from admin"
        max_admin_id = pd.read_sql_query(sql, engine)['max_admin_id'].iloc[0]
        admin_info = Admin()
        admin_info.id = max_admin_id + 1  # new admin id
        admin_info.registration_date = datetime.now().strftime("%Y-%m-%d")
        admin_info.email = info["email"]
        admin_info.name = (f"管理员{max_admin_id + 1}" if "name" not in info or info["name"] is None else info["name"])

        # update pass code
        if not adminbiz.check_password_policy(info["password"]):
            logger.warning("%d, %s: not strong policy password", admin_info.id, admin_info.name)
            return jsonify({"status": "failure", "message": "密码不合规范"})
        salt = bcrypt.gensalt(constants.DEFAULT_PASSWORD_SALT)
        bcrypt_password = bcrypt.hashpw(info["password"].encode('utf-8'), salt)
        admin_info.password = bcrypt_password
        db.session.add(admin_info)
        db.session.commit()

        # send confirm email
        try:
            emailverify.drop_token(admin_info.email)
            email_token = emailverify.EmailVerifyToken(admin_info.email, expiry=constants.EMAIL_VRF_EXPIRY)  # 2hrs expiry
            if not email_token.send_email():
                logger.warning(
                    "%d, %s: send confirm email failed",
                    admin_info.id,
                    admin_info.email,
                )
                return jsonify(
                    {"status": "failure", "message": "发送验证邮箱失败"}
                )
        except Exception as err:
            logger.info(traceback.format_exc())
            logger.warning(
                "%d, %s: send confirm email failed",
                admin_info.id,
                admin_info.email,
            )
            return jsonify(
                {"status": "failure", "message": f"{err.args}"}
            )
        logger.info(
            "%d, %s: send confirm email successfully",
            admin_info.id,
            admin_info.email,
        )
        emailverify.append_token(email_token)
        logger.info(
            "%d, %s: create new admin procedure completed successfully",
            admin_info.id,
            admin_info.name,
        )
        return jsonify({"status": "success"})


@admin.route('/users', methods=['GET', 'PATCH', 'POST'])
class Users(Resource):
    def get(self):
        user_type = request.args.get("role")
        role = 0 if user_type == 'volunteer' else 1 if user_type == 'disabled' else None
        users_info = User.query.filter(User.role == role).all() if role in [1, 0] else User.query.all()
        if not users_info:
            return jsonify([])

        display_users = []
        for user_info in users_info:
            info = {"openid": user_info.openid,
                    "name": user_info.name,
                    "role": "视障人士" if user_info.role == 1 else "志愿者",
                    "birthdate": str(user_info.birth),
                    "comment": user_info.remark,
                    "emergencyPerson": user_info.emergent_contact,
                    "emergencyTel": user_info.emergent_contact_phone,
                    "gender": user_info.gender,
                    "idcard": user_info.idcard,
                    "linkaddress": user_info.address,
                    "linktel": user_info.contact,
                    "phone": user_info.phone,
                    "registrationDate": str(user_info.registration_date),
                    "activitiesJoined": user_info.activities_joined,
                    "activitiesAbsence": user_info.activities_absence,
                    "joindHours": 4 * user_info.activities_joined}
            if user_info.role == 1:
                info["disabledID"] = user_info.disabled_id
            if user_info.audit_status == 0:
                info["audit_status"] = "pending"
            elif user_info.audit_status == 1:
                info["audit_status"] = "approved"
            elif user_info.audit_status == 2:
                info["audit_status"] = "imported"
            elif user_info.audit_status == -1:
                info["audit_status"] = "rejected"
            else:
                info["audit_status"] = "unknown"
            display_users.append(info)
        logger.info("query all user info with role type successfully")
        return jsonify(display_users)

    def patch(self):
        audit_info = json.loads(request.get_data())
        for audit in audit_info:
            openid = audit["openid"]
            status = audit["audit_status"]
            user_info = db.session.query(User).filter(User.openid == openid).first()
            if not user_info:
                logger.warning("%s, no such user openid", openid)
                return jsonify({"status": "failure", "message": "未知用户"})
            # users audit new status
            if user_info.audit_status == 0 and status in ("approved", "rejected", "pending"):
                if status == "approved":
                    sms_template = "NOTIFY_APPROVED"
                    user_info.audit_status = 1
                    db.session.commit()
                elif status == "rejected":
                    sms_template = "NOTIFY_REJECTED"
                    db.session.delete(user_info)
                    db.session.commit()
                else:
                    continue
                # send sms message to notify user the result timely
                try:
                    sms_token = smsverify.SMSVerifyToken(
                        phone_number=user_info.phone, expiry=3600
                    )
                    sms_token.template = sms_template
                    sms_token.vrfcode = ""
                    sms_token.signature = constants.COM_SIGNATURE
                    if not sms_token.send_sms():
                        logger.warning("%s, unable to send sms to number", user_info.phone)
                except Exception as e:
                    logger.error(getattr(e, 'message', repr(e)))
                    pass

        logger.info("update users audit status successfully")
        return jsonify({"status": "success"})


@admin.route('/admin/<int:admin_id>/update-password', methods=['POST'])
class AdminUpdatePassword(Resource):
    def post(self, admin_id):
        admin_password = json.loads(request.get_data())
        old_pass, new_pass = admin_password["old_password"], admin_password["new_password"]
        admin_info = db.session.query(Admin).filter(Admin.id == admin_id).first()
        if not admin_info:
            logger.warning("%d: admin not exist.", admin_id)
            return jsonify({"status": "failure", "message": "账户不存在"})
        if not bcrypt.checkpw(old_pass.encode('utf-8'), admin_info.password):
            logger.warning("%d: wrong old password", admin_id)
            return jsonify({"status": "failure", "message": "密码错误"})
        if not adminbiz.check_password_policy(new_pass):
            logger.warning("%d: not strong policy password", admin_id)
            return jsonify({"status": "failure", "message": "密码不合规范"})
        salt = bcrypt.gensalt(constants.DEFAULT_PASSWORD_SALT)
        bcrypt_password = bcrypt.hashpw(new_pass.encode('utf-8'), salt)
        admin_info.password = bcrypt_password
        db.session.commit()
        logger.info("%d: update password successfully", admin_id)
        return jsonify({"status": "success"})


@admin.route("/admin/forget-password", methods=['GET'])
class AdminResetPassword(Resource):
    def get(self):
        address = request.args.get("email")
        admin_info = db.session.query(Admin).filter(Admin.email == address).first()
        if not admin_info:
            logger.warning("%s, no such admin account", address)
            return jsonify({"status": "failure", "message": "未注册邮箱"})

        response, new_pass = emailverify.send_reset(receiver=address)
        if response:
            logger.warning("%s: send reset email failed", address)
            return jsonify({"status": "failure", "message": f"{response}"})
        logger.info("%s, send reset email successfully", address)

        salt = bcrypt.gensalt(constants.DEFAULT_PASSWORD_SALT)
        bcrypt_password = bcrypt.hashpw(new_pass.encode('utf-8'), salt)
        admin_info.password = bcrypt_password
        db.session.commit()
        logger.info("%s, update password successfully", address)
        return jsonify({"status": "success"})


@admin.route("/profile", methods=["GET", 'POST'])
class ProfileOperate(Resource):
    def get(self):
        openid = request.headers.get("Authorization")
        user_info = User.query.filter(User.openid == openid).first()
        if not user_info:
            logger.warning("%s: user not registered", openid)
            return jsonify({"status": "failure", "message": "用户未注册"})
        user_info = dbutils.serialize(user_info)
        feedback = {
            "status": "success",
            "openid": user_info["openid"],
            "birthDate": str(user_info["birth"]),
            "usercomment": user_info["remark"],
            "disabledID": user_info["disabled_id"],
            "emergencyPerson": user_info["emergent_contact"],
            "emergencyTel": user_info["emergent_contact_phone"],
            "gender": user_info["gender"],
            "idcard": user_info["idcard"],
            "linkaddress": user_info["address"],
            "linktel": user_info["contact"],
            "name": user_info["name"],
            "role": 'volunteer' if user_info["role"] == 0 else 'impaired',
            "phone": user_info["phone"],
            "email": user_info["email"],
            "registrationDate": str(user_info["registration_date"]),
            "activitiesJoined": user_info["activities_joined"],
            "activitiesAbsence": user_info["activities_absence"],
            "joindHours": 4 * user_info["activities_joined"]
        }
        logger.info("%s: user login successfully", user_info["openid"])
        return jsonify(feedback)

    def post(self):
        # update profile
        new_info = json.loads(request.get_data())  # get request POST user data
        openid = request.headers.get("Authorization")
        status = db.session.query(User).filter(User.openid == openid).first()
        status.gender = new_info["gender"]
        status.birth = new_info["birthDate"]
        status.name = new_info["name"]
        status.address = new_info["linkaddress"]
        status.email = new_info["email"]

        if new_info["role"] == 'volunteer':
            status.role = 0
        elif new_info["role"] == 'impaired':
            status.role = 1
        else:
            status.role = 2
        if status.role == 1 and new_info['disabledID']:
            status.disabled_id = new_info['disabledID']
            status.disabled_id_verified = 0
        if 'idcard' in new_info:
            status.idcard = new_info['idcard']
            status.idcard_verified = 0

        db.session.commit()
        logger.info("%s: complete user profile updating successfully", openid)
        return jsonify({"status": "success"})


@admin.route("/getPhoneNumber", methods=['POST'])
class GetPhoneNumber(Resource):
    def post(self):
        """get weixin user phoneNumber"""
        info = request.get_json()  # get http POST data bytes format
        print(info)
        js_code = info["js_code"]
        encrypted_data = info["encryptedData"]
        iv = info["iv"]
        if js_code is None:
            return jsonify({"status": "failure"})
        prefix = "https://api.weixin.qq.com/sns/jscode2session?appid="
        suffix = "&grant_type=authorization_code"
        url = prefix + GrimmConfig.WX_APP_ID + "&secret=" + GrimmConfig.WX_APP_SECRET + "&js_code=" + js_code + suffix
        logger.info("user login, wxapp authorization: %s", url)
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

                phone_decrypt = decrypt.PhoneNumberDecrypt(GrimmConfig.WX_APP_ID, sessionKey)
                decryptData = phone_decrypt.decrypt(encrypted_data, iv)
                print(decryptData)
                feedback["decrypt_data"] = decryptData
                del feedback["session_key"]
                feedback["status"] = "success"
            else:
                logger.error("wxapp authorization failed")
                feedback["status"] = "failure"
        return jsonify(feedback)


@admin.route("/register", methods=['POST'])
class RegisterInfo(Resource):
    def post(self):
        """view function for registering new user to database"""
        global SMS_VERIFIED_OPENID
        info = request.get_json()  # get http POST data bytes format
        # fetch data from front end

        openid = request.headers.get("Authorization")
        user_info = User.query.filter(User.openid == openid).first()
        if user_info:
            logger.error("%s: user is registered already", openid)
            return jsonify({"status": "failure", "message": "用户已注册，请登录"})

        if not user_info:
            user_info = User()
        user_info.openid = request.headers.get("Authorization")
        if info['role'] == 'volunteer':
            user_info.role = 0
        elif info['role'] == 'impaired':
            user_info.role = 1
        else:
            user_info.role = 2

        if user_info.role == 1:
            user_info.disabled_id = info['disabledID']
            user_info.disabled_id_verified = 0

        user_info.birth = info["birthdate"] if "birthdate" in info.keys() else datetime.now().strftime("%Y-%m-%d")
        # user_info['remark'] = info['comment']
        user_info.gender = info["gender"]
        # user_info['idcard'] = info['idcard']
        user_info.address = info["linkaddress"]
        # user_info['contact'] = info['linktel']
        user_info.name = info["name"]
        if 'idcard' in info:
            user_info.idcard = info['idcard']
            user_info.idcard_verified = 0
        user_info.audit_status = 0
        user_info.registration_date = datetime.now().strftime("%Y-%m-%d")
        user_info.phone = info["phone"]
        user_info.phone_verified = 1
        user_info.email = info["email"]
        user_info.email_verified = 0
        adminbiz.set_openid_if_user_info_exists(openid, user_info.idcard, user_info.phone, user_info.email,
                                                user_info.disabled_id if user_info.role == 1 else None)

        exist_info = User.query.filter(User.openid == openid).first()
        if not exist_info:
            db.session.add(user_info)
            db.session.commit()
        else:
            user_info.audit_status = 1

        socketio.emit("new-users", [user_info])
        user_info.push_status = 1
        db.session.commit()
        logger.info("%s: complete user registration success", openid)
        return jsonify({"status": "success"})


@admin.route("/smscode", methods=['GET', 'POST'])
class SMSCode(Resource):
    def get(self):
        phone_number = request.args.get("phone")
        if phone_number is None:
            logger.warning("invalid url parameter phone_number")
            return jsonify({"status": "failure", "message": "无效url参数"})
        try:
            smsverify.drop_token(phone_number)  # drop old token if it exists
            sms_token = smsverify.SMSVerifyToken(
                phone_number=phone_number,
                expiry=constants.SMS_VRF_EXPIRY,
                template="REGISTER_USER",
            )
            if not sms_token.send_sms():
                logger.warning("%s, unable to send sms to number", phone_number)
                return jsonify({"status": "failure", "message": "发送失败"})
        except Exception as err:
            return jsonify(
                {"status": "failure", "message": f"{err.args}"}
            )
        # append new token to pool
        smsverify.append_token(sms_token)

        logger.info(
            "%s, %s: send sms to number successfully", phone_number, sms_token.vrfcode
        )
        return jsonify({"status": "success"})

    def post(self):
        global SMS_VERIFIED_OPENID
        data = request.get_json()
        phone_number = data["phone"]
        vrfcode = data["verification_code"]
        openid = request.headers.get("Authorization")
        sms_token = smsverify.fetch_token(phone_number)
        if sms_token is None:
            logger.warning("%s: no such a sms token for number", phone_number)
            return jsonify(
                {"status": "failure", "message": "未向该用户发送验证短信"}
            )
        result = sms_token.validate(phone_number=phone_number, vrfcode=vrfcode)
        if result is not True:
            logger.warning(
                "%s, %s: sms code validation failed, %s", phone_number, vrfcode, result
            )
            return jsonify({"status": "failure", "message": result})
        smsverify.drop_token(phone_number)  # drop token from pool if validated
        # try update database first, if no successful, append this openid.
        try:
            if db.expr_update("user", {"phone_verified": 1}, openid=openid) is False:
                SMS_VERIFIED_OPENID[openid] = phone_number
        except:
            logger.warning("%s: update user phone valid status failed", openid)
            return jsonify(
                {"status": "failure", "message": "未知错误，请重新短信验证"}
            )

        logger.info(
            "%s, %s: sms code validates successfully", phone_number, vrfcode
        )
        return jsonify({"status": "success"})
