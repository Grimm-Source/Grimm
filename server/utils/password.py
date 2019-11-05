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
import bcrypt
import server.core.db as db

from server import sys_logger
from server.core.const import DEFAULT_PASSWORD_SALT, DB_QUOTED_TYPES


def check_password_policy(password):
    '''check password policy to ensure strong policy password'''
    if isinstance(password, bytes):
        password = password.decode('utf8')

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


def update_password(password, tbl='admin', policy_check=True, **kwargs):
    '''update user password'''
    if kwargs is None or len(kwargs) > 1:
        sys_logger.error('password.update_password: invalid argument')
        return False

    for key, val in kwargs.items():
        pass
    typeinfo = db.query_tbl_fields_datatype(tbl, key)
    need_quote = True if typeinfo[key] in DB_QUOTED_TYPES else False
    kwargs[key] = f"'{val}'" if need_quote and isinstance(val, str) and val[0] not in '\'"' else val

    policy_pass = check_password_policy(password) if policy_check else True
    if policy_pass is True:
        salt = bcrypt.gensalt(DEFAULT_PASSWORD_SALT)
        if isinstance(password, str):
            password = password.encode('utf-8')
        bcrypt_passcode = bcrypt.hashpw(password, salt)
        passcode = {'password': bcrypt_passcode}
        try:
            if db.expr_update(tbl=tbl, vals=passcode, **kwargs) == 1:
                return True
        except:
            pass
    return False


def verify_password(password, tbl='admin', **kwargs):
    '''verify user password when login or register'''
    try:
        query = db.expr_query(tbl, 'password', **kwargs)
        if len(query) == 1:
            bcrypt_password = query[0]['password']
            if isinstance(password, str):
                password = password.encode('utf-8')
            if isinstance(bcrypt_password, str):
                bcrypt_password = bcrypt_password.encode('utf-8')
            return bcrypt.checkpw(password, bcrypt_password)
    except:
        pass
    return False
