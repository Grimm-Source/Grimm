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

from itsdangerous import URLSafeTimedSerializer

from grimm import logger
from grimm import GrimmConfig
from grimm.utils.misctools import get_host_ip, is_ipv4_addr
from grimm.utils.constants import HOST, PORT
from grimm.utils.constants import DEFAULT_SERIAL_NO_BYTES, DEFAULT_VRFCODE_BYTES, DEFAULT_PROTOCOL

VRFCODE_POOL = {}


def new_serial_number(_bytes=DEFAULT_SERIAL_NO_BYTES):
    '''generate new serial number'''
    return uuid.uuid1().hex[0:_bytes]


def new_vrfcode(_bytes=DEFAULT_VRFCODE_BYTES):
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
            logger.error('invalid verification code: %s', code)
            return False
    else:
        err = TypeError('invalid type for parameter: code')
        logger.error(err.message)
        raise err

    duration = time.time() - start

    if duration > limit:
        del VRFCODE_POOL[code]
        return False
    return True


def new_vrfurl(email):
    '''generate new confirm verification email url'''
    serializer = URLSafeTimedSerializer(GrimmConfig.SECRET_KEY)
    token = serializer.dumps(email, salt=GrimmConfig.SECURITY_PASSWORD_SALT)
    server_port = PORT
    server_host = get_host_ip() if is_ipv4_addr(HOST) or HOST == 'localhost' else HOST

    vrfurl = DEFAULT_PROTOCOL + '://' + 'rp-i.net' + '/admin-email?verify_token=' + token
    return vrfurl


def parse_vrftoken(token):
    '''confirm email token with certain expiration time'''
    serializer = URLSafeTimedSerializer(GrimmConfig.SECRET_KEY)
    try:
        addr = serializer.loads(
            token,
            salt=GrimmConfig.SECURITY_PASSWORD_SALT)
    except:
        return None
    return addr
