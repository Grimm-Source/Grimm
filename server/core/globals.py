#
# File: globals.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: contains all global const definitions.
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
import os.path as path
import uuid
import logging
from server.utils.misc import pardir

from server import TOP_DIR


# regexs
EMAIL_REGEX = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
# HOSTNAME_REGEX = r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$'
# IPADDR_REGEX = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'

# database configs
DB_CONFIG_FILE = path.join(TOP_DIR, 'config/db.cfg')

# database datatypes which needs check quotes
DB_QUOTED_TYPES = ('char', 'varchar', 'datetime', 'date',
                   'timestamp', 'text', 'binary', 'time')

# database write/read timeout
DB_WRITE_TIMEOUT = 10
DB_READ_TIMEOUT = 10

# expiry time
SMS_VRF_EXPIRY = 300
EMAIL_VRF_EXPIRY = 7200

# root admin password
ROOT_PASSWORD = 'Cisco123456.'

# Flask app configs
APP_DEBUG_MODE = False       # app debug mode
APP_TESTING_MODE = False    # app testing mode
APP_SECRET_KEY = os.urandom(24) # app secret key
APP_SECURITY_PASSWORD_SALT = uuid.uuid4().hex # app security password salt
APP_TRAP_HTTP_EXCEPTIONS = False    # app trap http exceptions
APP_TRAP_BAD_REQUEST_ERRORS = True  # app trap BadRequest errors
APP_CONFIG_FILE = path.join(TOP_DIR, 'config/flaskapp.cfg') # app json config file
APP_TEMPLATE_PATH = path.join(TOP_DIR, 'templates') # templates folder
APP_STATIC_PATH = path.join(TOP_DIR, 'static') # static resouce folder
del pardir

# config when starting back-end
HOST = None
PORT = None
DAEMON_LOAD = False
SESSION_LOG_FILE = None

# send sms config
VRF_SIGNATURE = '视障人士志愿者平台验证'
COM_SIGNATURE = '华晓信息'
TEMPLATE_CODES = {
    'AUTHENTICATE_ID': 'SMS_134125051',
    'CONFIRM_LOGIN': 'SMS_134125050',
    'REGISTER_USER': 'SMS_134125048',
    'NOTIFY_APPROVED': 'SMS_176405562',
    'NOTIFY_REJECTED': 'SMS_176405555'
    }

# misc consts
DEFAULT_SERIAL_NO_BYTES = 32
DEFAULT_VRFCODE_BYTES = 6
DEFAULT_PROTOCOL = 'http' # need to update to https

# default password salt
DEFAULT_PASSWORD_SALT = 5

# local machine information
HOST_IP = '0.0.0.0'
PLATFORM = None

# Carousel information
CAROUSEL_LIST = [
    {'url': 'https://mp.weixin.qq.com/s/-uvqSpe7eZcF6X0pVXgjEA', 'title': '志愿者证书 申请流程', 'photo_url': 'https://s.zhiyuanyun.com/www.chinavolunteer.cn/cms/201901/18/5c41a6d2488b7.jpg'},
    {'url': 'https://mp.weixin.qq.com/s/VG8UXhK9P-_XUJfK5wu4vQ', 'title': '引导视障者的方式方法及需注意事项', 'photo_url': 'https://s.zhiyuanyun.com/www.chinavolunteer.cn/cms/202002/11/5e41ff79263f6.jpg'}
    ]

# Tag information
TAG_LIST = ['运动', '学习', '分享', '文娱', '保健', '其它']

# Email config file
EMAIL_CONFIG_FILE = path.join(TOP_DIR, 'config/email.cfg')

# wxapp config file
WX_JSAPI_URL = 'https://api.weixin.qq.com/sns/jscode2session'
WX_CONFIG_FILE = path.join(TOP_DIR, 'config/wxapp.cfg')

# log files
SYS_LOG_FILE = path.join(TOP_DIR, 'log/sys.log')
SYS_LOGGING_LEVEL = logging.DEBUG
ADMIN_LOG_FILE = path.join(TOP_DIR, 'log/admin.log')
ADMIN_LOGGING_LEVEL = logging.DEBUG
DB_LOG_FILE = path.join(TOP_DIR, 'log/db.log')
DB_LOGGING_LEVEL = logging.DEBUG
USER_LOG_FILE = path.join(TOP_DIR, 'log/user.log')
USER_LOGGING_LEVEL = logging.DEBUG
APP_LOG_FILE = path.join(TOP_DIR, 'log/app.log')
APP_LOGGING_LEVEL = logging.INFO
