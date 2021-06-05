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
from grimm.utils.misctools import get_pardir

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
FORCE_LOAD = False
DAEMON_LOAD = False
SESSION_LOG = None

# send sms configuration
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
DEFAULT_PROTOCOL = 'https'

# default password salt
DEFAULT_PASSWORD_SALT = 5

# local machine information
HOST_IP = '0.0.0.0'
PLATFORM = None

# Carousel information
CAROUSEL_LIST = [
    {'url': 'https://mp.weixin.qq.com/s/-uvqSpe7eZcF6X0pVXgjEA', 'title': '志愿者证书 申请流程', 'photo_url': 'https://7874-xtydtc01-1259619275.tcb.qcloud.la/grimm/carousel1.jpeg?sign=acf6a23ed0f57e97dcc2793302ac7d46&t=1599459574'},
    {'url': 'https://mp.weixin.qq.com/s/-uvqSpe7eZcF6X0pVXgjEA', 'title': '志愿者证书 申请流程', 'photo_url': 'https://7874-xtydtc01-1259619275.tcb.qcloud.la/grimm/carousel2.jpeg?sign=60ba325a07e07a14343fb366f92876af&t=1599459706'},
    {'url': 'https://mp.weixin.qq.com/s/VG8UXhK9P-_XUJfK5wu4vQ', 'title': '引导视障者的方式方法及需注意事项', 'photo_url':'https://7874-xtydtc01-1259619275.tcb.qcloud.la/grimm/carousel3.jpeg?sign=023ac732c7e9cdf0f15f66c4ef09a8fb&t=1599459763'}
    ]

# Tag information
TAG_LIST = ['运动', '学习', '分享', '文娱', '保健', '其它']
