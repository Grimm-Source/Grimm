#
# File: const.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: contains all const definitions.
#
# To-Dos:
#   1. make other supplements if needed.
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#   1. 2019/08/12, Ming, create first revision.
#

import os
import sys
from server.utils.misctools import get_pardir

# regex
EMAIL_REGEX = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
HOSTNAME_REGEX = r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$'
IPADDR_REGEX = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'

# database configs
pardir = get_pardir(get_pardir(os.path.abspath(__file__)))
DB_CONFIG_FILE = pardir + '/config/db.config'

# db logger configs
DB_LOGGER_FILE = pardir + '/log/db.log'

del pardir

# database datatypes which needs check quotes
DB_QUOTED_TYPES = ('char', 'varchar', 'datetime', 'date',
                   'timestamp', 'text', 'binary', 'time')

# expiry time
SMS_VRF_EXPIRY = 300
EMAIL_VRF_EXPIRY = 7200

# root admin password
ROOT_PASSWORD = 'Cisco123456.'

# configuration when loading back-end
HOST = None
PORT = None
FORCE_LOAD = None

# send sms configuration
VRF_SIGNATURE = '视障人士志愿者平台验证'
COM_SIGNATURE = '阿里云短信测试专用'
TEMPLATE_CODES = {
    'AUTHENTICATE_ID': 'SMS_134125051',
    'CONFIRM_LOGIN': 'SMS_134125050',
    'REGISTER_USER': 'SMS_134125048',
    'NOTIFY_APPROVED': 'SMS_175400063',
    'NOTIFY_REJECTED': 'SMS_175405604'
    }

# misc consts
DEFAULT_SERIAL_NO_BYTES = 32
DEFAULT_VRFCODE_BYTES = 6
DEFAULT_PROTOCOL = 'http'


# default password salt
DEFAULT_PASSWORD_SALT = 5
