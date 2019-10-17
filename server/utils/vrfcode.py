#
# File: vrfcode.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: generate transaction ID and verification code,
# keeping them unique.
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

import uuid
import time
import random
import string

from flask import url_for
from itsdangerous import URLSafeTimedSerializer

from server import sys_logger
from server.core import grimm
from server import HOST, PORT


VRFCODE_POOL = {}
SERIAL_BYTES = 32
VRFCODE_BYTES = 6

PROTOCOL = 'http'

def new_serial_number(_bytes=SERIAL_BYTES):
    '''generate new serial number'''
    return uuid.uuid1().hex[0:_bytes]


def new_vrfcode(_bytes=VRFCODE_BYTES):
    '''generate new verification code'''
    global VRFCODE_POOL
    code = ''.join(random.choices(string.digits, k=_bytes))
    if code in VRFCODE_POOL:
        return new_vrfcode()
    else:
        start = int(time.time())
        VRFCODE_POOL[code] = start
    return code


def check_vrfcode_expiry(code, limit=600):
    '''check code expiry, return True if not expired, otherwise False'''
    global VRFCODE_POOL
    if isinstance(code, bytes):
        code = code.decode('utf8')
    if isinstance(code, int):
        code = '%06d' % (code)
    if isinstance(code, str):
        if code in VRFCODE_POOL:
            start = VRFCODE_POOL[code]
        else:
            sys_logger.error('invalid verification code: %s', code)
            return False
    else:
        err = TypeError('invalid type for parameter: code')
        sys_logger.error(err.message)
        raise err

    duration = time.time() - start

    if duration > limit:
        del VRFCODE_POOL[code]
        return False
    return True


def new_vrfurl(email):
    '''generate new confirm verification email url'''
    serializer = URLSafeTimedSerializer(grimm.config['SECRET_KEY'])
    token = serializer.dumps(email, salt=grimm.config['SECURITY_PASSWORD_SALT'])
    vrfurl = PROTOCOL + '://' + str(HOST) + ':' + str(PORT) + '/confrim-email/' + token
    return vrfurl


def parse_vrftoken(token):
    '''confirm email token with certain expiration time'''
    serializer = URLSafeTimedSerializer(grimm.config['SECRET_KEY'])
    try:
        addr = serializer.loads(
            token,
            salt=grimm.config['SECURITY_PASSWORD_SALT'])
    except:
        return None
    return addr
