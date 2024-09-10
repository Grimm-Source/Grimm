import json
import math
import traceback

from datetime import datetime, timedelta

import os
import bcrypt
import urllib3
import uuid
from flask import request, jsonify, send_file, current_app as app
from flask_restx import Resource, fields, reqparse
from werkzeug.datastructures import FileStorage


from grimm import logger, db, engine, GrimmConfig, api
# from grimm import socketio
from grimm.admin import admin, adminbiz
from grimm.admin.admindto import AdminDto
from grimm.models.activity import ActivityParticipant, Activity
from grimm.models.admin import Admin, User, PreSignedUrl
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
        admin_info = Admin()
        admin_info.registration_date = datetime.now().strftime("%Y-%m-%d")
        admin_info.email = info["email"]

        # update pass code
        if not adminbiz.check_password_policy(info["password"]):
            logger.warning("%s: not strong policy password", admin_info.name)
            return jsonify({"status": "failure", "message": "密码不合规范"})
        salt = bcrypt.gensalt(constants.DEFAULT_PASSWORD_SALT)
        bcrypt_password = bcrypt.hashpw(info["password"].encode('utf-8'), salt)
        admin_info.password = bcrypt_password
        db.session.add(admin_info)

        # to get admin_info.id set by DB automatically
        db.session.flush()
        admin_info.name = info.get('name') or f"管理员{admin_info.id}"

        db.session.commit()

        # send confirm email
        try:
            emailverify.drop_token(admin_info.email)
            email_token = emailverify.EmailVerifyToken(admin_info.email,
                                                       expiry=constants.EMAIL_VRF_EXPIRY)  # 2hrs expiry
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
            logger.error(getattr(err, 'message', repr(err)))
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
            "joindHours": 4 * user_info["activities_joined"]
        }

        # calculate activity join count when sign off
        joined_participants = db.session.query(ActivityParticipant.signup_time,
                                               ActivityParticipant.signoff_time,
                                               Activity.start_time,
                                               Activity.end_time) \
            .filter(ActivityParticipant.participant_openid == openid,
                    ActivityParticipant.current_state == "signed_off",
                    ActivityParticipant.activity_id == Activity.id).all()
        effective_join_count = 0
        effective_join_seconds = 0
        for part in joined_participants:
            sign_up_time = part[0]
            sign_off_time = part[1]
            activity_start_time = part[2]
            activity_end_time = part[3]

            if not sign_up_time or not sign_off_time:
                continue

            if sign_off_time <= activity_start_time or sign_up_time >= activity_end_time:
                # invalid activity joined
                effective_join_count = effective_join_count + 0
                effective_join_hours = effective_join_seconds + 0
            else:
                effective_join_count = effective_join_count + 1
                if sign_off_time >= activity_end_time:
                    effective_end_time = activity_end_time
                else:
                    effective_end_time = sign_off_time
                if sign_up_time >= activity_start_time:
                    effective_start_time = sign_up_time
                else:
                    effective_start_time = activity_start_time
                effective_seconds = (effective_end_time - effective_start_time).total_seconds()
                effective_join_seconds = effective_join_seconds + effective_seconds
        if effective_join_count > 0:
            user_info = db.session.query(User).filter(User.openid == openid).first()
            user_info.activities_joined = int(effective_join_count)
            db.session.commit()
            feedback['activitiesJoined'] = effective_join_count
        if effective_join_seconds > 0:
            feedback['joindHours'] = math.ceil(effective_join_seconds / 3600)

        logger.info(f"{openid}: user login successfully")
        return jsonify(feedback)

    def post(self):
        # update profile
        new_info = json.loads(request.get_data())  # get request POST user data
        openid = request.headers.get("Authorization")
        status = db.session.query(User).filter(User.openid == openid).first()
        if status is None:
            # set same response as success to prevent enumeration attack
            return jsonify({"status": "success"})

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
        if info.get("js_code") is None:
            return jsonify({"status": "failure"})

        js_code = info["js_code"]
        encrypted_data = info["encryptedData"]
        iv = info["iv"]
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

        if retry == 0:
            logger.error("request wxapp authorization exceed max retry")
            feedback["status"] = "failure"

        if retry != 0:
            feedback["server_errcode"] = 0
            if "session_key" in feedback:
                sessionKey = feedback["session_key"]

                phone_decrypt = decrypt.PhoneNumberDecrypt(GrimmConfig.WX_APP_ID, sessionKey)
                decryptData = phone_decrypt.decrypt(encrypted_data, iv)
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
        if 'email' in info:
            user_info = User.query.filter(User.email == info["email"]).first()
            if user_info:
                return jsonify({"status": "failure", "message": "邮件已注册"})
        if 'idcard' in info:
            user_info = User.query.filter(User.idcard == info['idcard']).first()
            if user_info:
                return jsonify({"status": "failure", "message": "该身份证已注册"})
        if 'phone' in info:
            user_info = User.query.filter(User.phone == info["phone"]).first()
            if user_info:
                return jsonify({"status": "failure", "message": "该手机号已注册"})

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

        # legacy logic, may not right
        user_info.birth = datetime.now().strftime("%Y-%m-%d")
        try:
            user_info.birth = datetime.strptime(info.get("birthdate"), "%Y-%m-%d")
        except:
            pass

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
        user_info.avatar_url = info['avatarUrl']
        adminbiz.set_openid_if_user_info_exists(openid, user_info.idcard, user_info.phone, user_info.email,
                                                user_info.disabled_id if user_info.role == 1 else None)

        exist_info = User.query.filter(User.openid == openid).first()
        if not exist_info:
            db.session.add(user_info)
            db.session.commit()
        else:
            user_info.audit_status = 1

        # socketio.emit("new-users", [user_info])
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
        # SMS_VERIFIED_OPENID is not used anywhere else, why do this?
        # and no `expr_update` function in SQLAlchemy, comment these for now
        # try update database first, if no successful, append this openid.
        # try:
        #     if db.expr_update("user", {"phone_verified": 1}, openid=openid) is False:
        #         SMS_VERIFIED_OPENID[openid] = phone_number
        # except:
        #     logger.warning("%s: update user phone valid status failed", openid)
        #     return jsonify(
        #         {"status": "failure", "message": "未知错误，请重新短信验证"}
        #     )

        logger.info(
            "%s, %s: sms code validates successfully", phone_number, vrfcode
        )
        return jsonify({"status": "success"})


# TODO really need this? and attrs like idcard may should be filtered
@admin.route("/authorize_user", methods=['GET'])
class AuthorizeUser(Resource):
    def get(self):
        openid = request.headers.get('Authorization')
        user_info = User.query.filter(User.openid == openid).first()
        if user_info is None:
            return jsonify(None)

        return jsonify(dbutils.serialize(user_info))

def is_admin(userId):
    return Admin.query.filter(Admin.id == userId).first() is not None

def user_idcard_realpath(filename):
    return os.path.realpath(
            os.path.join(GrimmConfig.GRIMM_USER_DOCUMENT_UPLOAD_PATH,
            filename))

def user_disabled_id_realpath(filename):
    return os.path.realpath(
            os.path.join(GrimmConfig.GRIMM_DISABLED_ID_UPLOAD_PATH,
            filename))

def pre_sign_user_identity_image(side, requester, target):
    expire_in_minutes = 3
    return {
        'token': uuid.uuid4().hex,
        'expire_at': datetime.now() + \
                timedelta(minutes=expire_in_minutes),
        'openid': requester,
        'target_openid': target,
        'side': side,
    }

def verify_picture(picture_data: FileStorage):
    return picture_data.content_length < 1e+6

def verify_presigned_url(token, side, requester_openid, target_openid):
    '''
        return JSON error message with HTTP status_code if verification failed
        return User instance if verification passed
    '''

    status_code = 404
    record = PreSignedUrl.query.filter(PreSignedUrl.token == token, PreSignedUrl.side==side).first()

    if not record or record.openid != requester_openid or record.target_openid != target_openid:
        return {
            "status": "failure",
            "error": "非法口令"
        }, status_code

    if datetime.now() > record.expire_at:
        return {
            "status": "failure",
            "error": "口令已过期"
        }, status_code

    return User.query.filter(User.openid == target_openid).first()

ErrorResponseModel = api.model('ErrorResponse', {
    'status': fields.String,
    'error': fields.String,
})

@admin.route("/user_idcard/urls/<string:target_user>", methods=['GET'])
class UserIdentity(Resource):
    signed_image_urls = api.model('UserIDcardImageURLs', {
        'obverse': fields.String,
        'reverse': fields.String
    })
    UserIdentityResponseModel = api.model('UserIDcardResponse', {
        'status': fields.String,
        'urls': fields.Nested(signed_image_urls, required=True, description="所请求照片的签名后链接"),
    })

    @api.response(200, 'Success', UserIdentityResponseModel)
    @api.response(404, 'User identity not found', ErrorResponseModel)
    @api.response(401, 'Unauthorized', ErrorResponseModel)
    @api.response(500, 'InternalError', ErrorResponseModel)
    def get(self, target_user):
        # TODO change to JWT get_jwt_identity
        requester = request.headers.get('Authorization')
        if requester != target_user and not is_admin(requester):
            return {
                "status": "failure",
                "error": "该用户无法读取其他用户的信息"
            }, 401

        if User.query.filter(User.openid == target_user).first() is None:
            return {
                'status': 'failure',
                'error': '用户信息未找到'
            }, 404

        ret = {}
        try:
            for side in constants.USER_IDENTITY_IMAGE_SIDE:
                params = pre_sign_user_identity_image(side,
                        requester, target_user)
                psu = PreSignedUrl(**params)
                db.session.add(psu)
                ret[side] = '/user_idcard/image/{}?token={}&side={}'.format(target_user, params['token'], side)
            db.session.commit()
        except Exception as e:
            logger.error("failed to commit to database: %s", e)
            return {
                "status": "failure",
                "error": f"发生未知服务器错误: {e}",
            }, 500
        else:
            return {
                "status": "success",
                "urls": ret
            }

user_identity_post_parser = reqparse.RequestParser()
user_identity_post_parser.add_argument('obverse', type=FileStorage, required=False, location="files")
user_identity_post_parser.add_argument('reverse', type=FileStorage, required=False, location="files")

@admin.route("/user_idcard/image/<string:target_openid>", methods=['POST'])
class UploadUserIdentity(Resource):
    UserIdentityPostModel = api.model('UserIdentityPost', {
        "reverse": fields.String(required=True, description="身份证反面照片"),
        "obverse": fields.String(required=True, description="身份证正面照片"),
    })


    @api.doc('上传身份证正反面照片', body=UserIdentityPostModel)
    @api.response(200, 'Success')
    @api.response(400, 'Invalid request body', ErrorResponseModel)
    @api.expect(user_identity_post_parser)
    def post(self, target_openid):
        # TODO change to JWT get_jwt_identity
        # openid = request.headers.get('Authorization')
        openid = target_openid

        files = user_identity_post_parser.parse_args()
        pic = files.get('obverse')
        side = 'obverse'
        if pic is None:
            pic = files.get('reverse')
            if pic is None:
                return {
                    'status': 'failure',
                    'error': '未找到照片'
                }, 400

            side = 'reverse'

        if not verify_picture(pic):
            return {
                'status': 'failure',
                'error': '照片文件内容过大'
            }, 400

        user = User.query.filter(User.openid == openid).first()
        if user is None:
            return {
                'status': 'failure',
                'error': '用户信息未找到'
            }, 404

        filename = f'{openid}_{side}_side.jpg'
        pic.save(user_idcard_realpath(filename))
        setattr(user, f'idcard_{side}_path', filename)

        params = pre_sign_user_identity_image(side, openid, openid)
        psu = PreSignedUrl(**params)

        # FIXME this code is for test, remove this before release
        user.audit_status = 0

        db.session.add(user)
        db.session.add(psu)
        db.session.commit()

        ret = {}
        ret[side] = '/user_idcard/image/{}?token={}&side={}'.format(openid, params['token'], side)

        return {
            'status': 'success',
            'urls': ret
        }, 200

user_identity_image_get_parser = reqparse.RequestParser()
user_identity_image_get_parser.add_argument('side', type=str, required=True, location="args")
user_identity_image_get_parser.add_argument('token', type=str, required=True, location="args")

@admin.route("/user_idcard/image/<string:target_openid>", methods=['GET'])
class UserIdentityImage(Resource):
    @api.expect(user_identity_image_get_parser)
    def get(self, target_openid):
        args = user_identity_image_get_parser.parse_args()
        side = args.get('side')
        token = args.get('token')
        # TODO change to JWT get_jwt_identity
        requester_openid = request.headers.get('Authorization')

        if side not in ('obverse', 'reverse'):
            return {
                "status": "failure",
                "error": "参数错误: side"
            }, 400

        record = PreSignedUrl.query.filter(PreSignedUrl.token == token, PreSignedUrl.side==side).first()
        # TODO validate requester_openid and target_openid
        if record is None:
            return {
                "status": "failure",
                "error": "非法口令"
            }, 404
        if datetime.now() > record.expire_at:
            return {
                "status": "failure",
                "error": "口令已过期"
            }, 404

        user = User.query.filter(User.openid == target_openid).first()
        file_path = getattr(user, f'idcard_{side}_path', None)
        if not file_path:
            return {
                "status": "failure",
                "error": "用户身份证信息未找到"
            }, 404

        return send_file(user_idcard_realpath(file_path), mimetype='image/jpeg')

user_disabled_id_file_post_parser = reqparse.RequestParser()
user_disabled_id_file_post_parser.add_argument('obverse', type=FileStorage, required=False, location="files")

@admin.route("/user_disabled_id/image/<string:target_openid>", methods=['POST'])
class UploadUserDisabledIdImage(Resource):
    UserDisabledIdPostModel = api.model('UserDisabledIdPost', {
        "disabled_id_obverse": fields.String(required=True, description="身份证正面照片"),
    })


    @api.doc('上传身份证正反面照片', body=UserDisabledIdPostModel)
    @api.response(200, 'Success')
    @api.response(400, 'Invalid request body', ErrorResponseModel)
    @api.expect(user_disabled_id_file_post_parser)
    def post(self, target_openid):
        # TODO change to JWT get_jwt_identity
        # openid = request.headers.get('Authorization')
        openid = target_openid

        files = user_disabled_id_file_post_parser.parse_args()
        side = 'obverse'
        pic = files.get(side)
        if pic is None:
            return {
                'status': 'failure',
                'error': '未找到照片'
            }, 400

        if not verify_picture(pic):
            return {
                'status': 'failure',
                'error': '照片文件内容过大'
            }, 400

        user = User.query.filter(User.openid == openid).first()
        if user is None:
            return {
                'status': 'failure',
                'error': '用户信息未找到'
            }, 404

        filename = f'{openid}_{side}_side.jpg'
        pic.save(user_disabled_id_realpath(filename))
        setattr(user, f'disabled_id_obverse_path', filename)

        params = pre_sign_user_identity_image('disabled_id_obverse', openid, openid)
        psu = PreSignedUrl(**params)

        db.session.add(user)
        db.session.add(psu)
        db.session.commit()

        ret = {}
        ret[side] = '/user_disabled_id/image/{}?token={}&side={}'.format(openid, params['token'], side)

        return {
            'status': 'success',
            'urls': ret
        }, 200

user_disabled_id_image_get_parser = reqparse.RequestParser()
user_disabled_id_image_get_parser.add_argument('token', type=str, required=True, location="args")

@admin.route("/user_disabled_id/image/<string:target_openid>", methods=['GET'])
class UserDisabledIdImage(Resource):
    @api.expect(user_disabled_id_image_get_parser)
    def get(self, target_openid):
        args = user_disabled_id_image_get_parser.parse_args()
        side = 'obverse'
        token = args.get('token')
        # TODO change to JWT get_jwt_identity
        requester_openid = request.headers.get('Authorization')

        if side != 'obverse':
            return {
                "status": "failure",
                "error": "参数错误: side"
            }, 400

        result = verify_presigned_url(token, 'disabled_id_obverse',
                requester_openid, target_openid)

        if not isinstance(result, User):
            return result

        file_path = getattr(result, f'disabled_id_{side}_path')
        if not file_path:
            return {
                "status": "failure",
                "error": "用户残疾证信息未找到"
            }, 404

        return send_file(user_disabled_id_realpath(file_path), mimetype='image/jpeg')

@admin.route("/user_identities/urls/<string:target_user>", methods=['GET'])
class UserIdentities(Resource):
    signed_image_urls = api.model('UserIdentityImageURLs', {
        'obverse': fields.String,
        'reverse': fields.String,
        'disabled_id_obverse': fields.String
    })
    UserIdentityResponseModel = api.model('UserIdentityResponse', {
        'status': fields.String,
        'urls': fields.Nested(signed_image_urls, required=True, description="所请求照片的签名后链接"),
    })

    @api.response(200, 'Success', UserIdentityResponseModel)
    @api.response(404, 'User identity not found', ErrorResponseModel)
    @api.response(401, 'Unauthorized', ErrorResponseModel)
    @api.response(500, 'InternalError', ErrorResponseModel)
    def get(self, target_user):
        # TODO change to JWT get_jwt_identity
        requester = request.headers.get('Authorization')
        if requester != target_user and not is_admin(requester):
            return {
                "status": "failure",
                "error": "该用户无法读取其他用户的信息"
            }, 401

        if User.query.filter(User.openid == target_user).first() is None:
            return {
                'status': 'failure',
                'error': '用户信息未找到'
            }, 404

        ret = {}
        try:
            for side in ['obverse', 'reverse', 'disabled_id_obverse']:
                params = pre_sign_user_identity_image(side,
                        requester, target_user)
                psu = PreSignedUrl(**params)
                db.session.add(psu)
                if side in ['obverse', 'reverse']:
                    ret[side] = '/user_idcard/image/{}?token={}&side={}'.format(target_user, params['token'], side)
                else:
                    ret[side] = '/user_disabled_id/image/{}?token={}'.format(target_user, params['token'])
            db.session.commit()
        except Exception as e:
            logger.error("failed to commit to database: %s", e)
            return {
                "status": "failure",
                "error": f"发生未知服务器错误: {e}",
            }, 500
        else:
            return {
                "status": "success",
                "urls": ret
            }

# FIXME for test purpose
@admin.route("/user_tmp_toggle/<string:username>", methods=['GET'])
class TmpToggleUserRole(Resource):
    def get(self, username):
        user = User.query.filter(User.name == username).first()
        if user is None:
            return {
                "status": "failure",
                "error": f"用户信息未找到 {username}"
            }, 404

        user.role = 0 if user.role == 1 else 1
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'status': f'success,当前为 {"志愿者" if user.role == 0 else "视障者"}',
        })
