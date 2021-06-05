#
# File: misc.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: password related utilities.
#
# To-Dos:
#   1. make other supplements if needed.
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#   1. 2019/08/15, Ming, create first revision, add password encryption method.
#

import re
import six

from grimm import db
from grimm.models.admin import User


def check_password_policy(password):
    """ check password policy to ensure strong policy password """
    password = six.ensure_str(password)
    if not isinstance(password, str):
        return False
    rules = [lambda s: any(c.isupper() for c in s) or 'no uppercase character',       # check uppercase
             lambda s: any(c.islower() for c in s) or 'no lowercase character',       # check lowercase
             lambda s: any(c.isdigit() for c in s) or 'no digit character',           # check digit character
             lambda s: not re.match("^[a-zA-Z0-9_]*$", s) or 'no special character',  # check special character
             lambda s: len(s) > 7 or 'password too short',                            # check short length
             lambda s: len(s) < 17 or 'password too long']                            # check long length
    result = [rule(password) for rule in rules]
    final = [x for x in result if x is not True]
    return True if not final else False


def set_openid_if_user_info_exists(openid, idcard=None, phone=None, email=None, disableid=None):
    if idcard:
        userinfo = db.session.query(User).filter(User.idcard == idcard).first()
        if userinfo and userinfo.audit_status == 2:
            userinfo.openid = openid
            db.session.commit()
            return
    if phone:
        userinfo = db.session.query(User).filter(User.phone == phone).first()
        if userinfo and userinfo.audit_status == 2:
            userinfo.openid = openid
            db.session.commit()
            return
    if email:
        userinfo = db.session.query(User).filter(User.email == email).first()
        if userinfo and userinfo.audit_status == 2:
            userinfo.openid = openid
            db.session.commit()
            return
    if disableid:
        userinfo = db.session.query(User).filter(User.disabled_id == disableid).first()
        if userinfo and userinfo.audit_status == 2:
            userinfo.openid = openid
            db.session.commit()
            return
