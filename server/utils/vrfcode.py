#
# File: id_code.py
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

from server import sys_logger


VRFCODES = {}
SERIAL_BYTES = 32
VRFCODE_BYTES = 6


def new_serial_number(_bytes=SERIAL_BYTES):
    '''generate new serial number'''
    return uuid.uuid1().hex[0:_bytes]


def new_vrfcode(_bytes=VRFCODE_BYTES):
    '''generate new verification code'''
    global VRFCODES
    code = ''.join(random.choices(string.digits, k=_bytes))
    if code in VRFCODES:
        return new_vrfcode()
    else:
        start = int(time.time())
        VRFCODES[code] = start
    return code


def check_vrfcode_expiry(code, limit=600):
    '''check code expiry, return True if not expired, otherwise False'''
    global VRFCODES
    if isinstance(code, bytes):
        code = code.decode('utf8')
    if isinstance(code, int):
        code = '%06d' % (code)
    if isinstance(code, str):
        if code in VRFCODES:
            start = VRFCODES[code]
        else:
            sys_logger.error('invalid verification code: %s', code)
            return False
    else:
        e = TypeError('invalid type for parameter: code')
        sys_logger.error(e.message)
        raise e

    duration = time.time() - start

    if duration > limit:
        del VRFCODES[code]
        return False
    return True


def new_vrflink():
    '''generate new verification email link'''
    pass
