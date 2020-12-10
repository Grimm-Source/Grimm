# Python 3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import server.core.db as db
import server.utils.db_utils as db_utils
import server.utils.import_user as imptuser
import server.utils.misctools as misc
from server import admin_logger, user_logger
from server.core import api
from flask import request
from flask_restx import Resource


@api.route("/devtools/importusers")
class dev_tools(Resource):
    def get(self):
        """this import history user data into database"""
        importAll()
        return misc.json_dump_http_response(
            {"status": "success", "message": "import all users complete"}
        )
    
def importAll():
    cur_dir = misc.get_pardir(os.path.abspath(__file__))
    vol_file = cur_dir + "/volunteer.csv"
    imp_file = cur_dir + "/impaired.csv"
    users = imptuser.importUser(vol_file, 0) + imptuser.importUser(imp_file, 1)
    fake_id = 0
    for u in users:
        userinfo = {}
        userinfo["openid"] = "fakeid_" + str(fake_id)
        openid = userinfo["openid"]
        if db.exist_row("user", openid=openid):
            continue
        userinfo['role'] = u['role']
        userinfo['idcard'] = 'fake_idcard_' + str(fake_id) if u['idcard'] == '' else u['idcard']
        userinfo['idcard_verified'] = 0
        if userinfo['role'] == 1:
            userinfo['disabled_id'] = 'fake_disable_id_' + str(fake_id)
            userinfo['disabled_id_verified'] = 0
        userinfo["birth"] = datetime.now().strftime("%Y-%m-%d")
        userinfo['remark'] = u['remark']
        # userinfo["gender"] = u["gender"]
        # userinfo["address"] = u["linkaddress"]
        # userinfo['contact'] = u['linktel']
        userinfo["name"] = u["name"]
        userinfo["audit_status"] = u["audit_status"]
        userinfo["registration_date"] = u['reg_date']
        userinfo["phone"] = 'fake_phone_' + str(fake_id) if u['phone'] == '' else u['phone']
        if db.exist_row('user', phone=userinfo['phone']):
            userinfo['phone'] = 'fake_phone_' + str(fake_id)
            userinfo['remark'] += ' 重复电话: ' + u['phone']
        userinfo["phone_verified"] = 0
        userinfo["email"] = 'fake_email_' + str(fake_id)
        userinfo["email_verified"] = 0
        userinfo['activities_joined'] = u['act_joined']
        fake_id += 1
        try:
            if db.expr_insert("user", userinfo) != 1:
                user_logger.error("%s: user registration failed", openid)
                continue
        except:
            user_logger.error("%s: user registration failed", openid)
            continue
