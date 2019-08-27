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
from core.db import expr_query, expr_update
from core.exceptions import UserNotFound, UserInvalidPassword


# Bigger this value is, more time the method takes, more security it offers.
DEFAULT_PASSWD_HASH_COST = 3


def update_usr_passwd(usr, input_passwd):
    '''update user password'''
    salt = bcrypt.gensalt(DEFAULT_PASSWD_HASH_COST)
    bcrypt_passwd = bcrypt.hashpw(input_passwd, salt)
    new_info = {'passwd': bcrypt_passwd}
    return expr_update(tbl=usr.role, account=usr.account, pairs=new_info)


def verify_usr_passwd(usr, input_passwd):
    '''verify user password when login or register'''
    col = 'passwd'
    data = expr_query(tbls=usr.role, cols=col, account=usr.account)
    if len(data) == 1:
        bcrypt_passwd = data[0][col]
        return bcrypt.checkpw(input_passwd, bcrypt_passwd)
    raise UserNotFound(usr.account)


def check_passwd_policy(input_passwd):
    '''check password policy to ensure strong policy password'''
    if isinstance(input_passwd, bytes):
        input_passwd = input_passwd.decode('utf8')

    if not isinstance(input_passwd, str):
        raise UserInvalidPassword('invalid arguement type')

    rules = [lambda s: any(c.isupper() for c in s) or 'no uppercase character',       # check uppercase
             lambda s: any(c.islower() for c in s) or 'no lowercase character',       # check lowercase
             lambda s: any(c.isdigit() for c in s) or 'no digit character',           # check digit character
             lambda s: not re.match("^[a-zA-Z0-9_]*$", s) or 'no special character',  # check special character
             lambda s: len(s) > 8 or 'password too short',                            # check short length
             lambda s: len(s) < 21 or 'password too long']                            # check long length

    result = [rule(input_passwd) for rule in rules]

    final = [x for x in result if x is not True]

    return True if not final else tuple(final)
