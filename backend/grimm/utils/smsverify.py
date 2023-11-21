#
# File: sms_verify.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: do sms message related jobs.
#
# To-Dos:
#   1. make other supplements if needed.
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#   1. 2019/09/24, Ming, create first revision.
#


import json
import time
import re
from datetime import datetime

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider

from grimm.utils.dysms.aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from grimm.utils.dysms.aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from grimm.utils.dysms import const
from grimm.utils import vrfcode as vrf_code
from grimm import logger, GrimmConfig
from grimm.exceptions.exceptions import UserPhoneError
from grimm.utils.constants import VRF_SIGNATURE, COM_SIGNATURE, TEMPLATE_CODES


ACS_CLIENT = AcsClient(GrimmConfig.SMS_ACCESS_KEY_ID, GrimmConfig.SMS_ACCESS_KEY_SECRET, const.REGION)
region_provider.add_endpoint(const.PRODUCT_NAME, const.REGION, const.DOMAIN)


SMS_TOKEN_POOL = {}


def append_token(token):
    """append sms verification token to be verified in pool"""
    global SMS_TOKEN_POOL
    if token.phone_number not in SMS_TOKEN_POOL:
        SMS_TOKEN_POOL[token.phone_number] = token


def fetch_token(phone_number):
    """fetch token with user phone number"""
    return None if phone_number not in SMS_TOKEN_POOL else SMS_TOKEN_POOL[phone_number]


def drop_token(phone_number):
    """drop used token in pool"""
    global SMS_TOKEN_POOL
    token = fetch_token(phone_number)
    if token is not None and \
            (token.expired or not token.valid):
        if token.vrfcode in vrf_code.VRFCODE_POOL:
            del vrf_code.VRFCODE_POOL[token.vrfcode]
        del SMS_TOKEN_POOL[token.phone_number]


def verify_phone_number_regex(phone_number):
    """verify phone number regex format"""
    regex = r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$'
    if re.match(regex, phone_number) is None:
        err = UserPhoneError('invalid phone number')
        logger.error(err.emsg)
        return False

    return True


def send(serial_no, phone_numbers, sign_name, template_code, template_param=None):
    """send sms message to phone numbers"""
    serial_id = serial_no
    sms_request = SendSmsRequest.SendSmsRequest()
    sms_request.set_TemplateCode(template_code)
    if template_param is not None:
        sms_request.set_TemplateParam(template_param)
    sms_request.set_OutId(serial_id)
    sms_request.set_SignName(sign_name)
    # 数据提交方式
    # smsRequest.set_method(MT.POST)
    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)
    sms_request.set_PhoneNumbers(phone_numbers)
    return ACS_CLIENT.do_action_with_exception(sms_request)


class SMSVerifyToken(object):
    """sms verification token class"""
    def __init__(self, phone_number, expiry=120,
                 access_id=GrimmConfig.SMS_ACCESS_KEY_ID,
                 access_secret=GrimmConfig.SMS_ACCESS_KEY_SECRET,
                 signature=VRF_SIGNATURE,
                 template='AUTHENTICATE_ID'):
        """initialize sms verification token objects"""
        if isinstance(phone_number, str) and isinstance(expiry, int):
            if verify_phone_number_regex(phone_number):
                self.__phone_number = phone_number
            self.__expiry = expiry
            self.__vrfcode = vrf_code.new_vrfcode()
            self.__serial_no = vrf_code.new_serial_number()
            self.__access_id = access_id
            self.__access_secret = access_secret
            self.__signature = signature
            self.__template = template
            self.__template_code = TEMPLATE_CODES[template]
            self.sms_response = None
            self.__send_time = None
            self.__valid = True
        else:
            raise TypeError('invalid value type to initialize sms token')

    @property
    def vrfcode(self):
        """get sms token verification code"""
        return self.__vrfcode

    @vrfcode.setter
    def vrfcode(self, msg):
        """reset vrfcode as some other sms message"""
        if self.__template != 'AUTHENTICATE_ID':
            self.__vrfcode = msg

    @property
    def serial_no(self):
        """get sms token serial number"""
        return self.__serial_no

    @property
    def phone_number(self):
        """get sms token phone number"""
        return self.__phone_number

    @property
    def signature(self):
        """get sms token signature"""
        return self.__signature

    @signature.setter
    def signature(self, new_signature):
        """set new sms token signature"""
        if new_signature in (VRF_SIGNATURE, COM_SIGNATURE):
            self.__signature = new_signature

    @property
    def template(self):
        """get sms token template code"""
        return self.__template

    @template.setter
    def template(self, new_template):
        """set new sms token template code"""
        if new_template in TEMPLATE_CODES.keys():
            self.__template = new_template
            self.__template_code = TEMPLATE_CODES[new_template]

    @property
    def duration(self):
        """get sms verification token instant duration"""
        if self.__send_time is not None:
            return time.time() - self.__send_time.timestamp()
        return 0.0

    @property
    def expiry(self):
        """get sms verification token expiry seconds const"""
        return self.__expiry

    @expiry.setter
    def expiry(self, new_expiry):
        """set new expiry time"""
        if isinstance(new_expiry, int) and new_expiry > self.expiry:
            self.__expiry = new_expiry

    @property
    def expired(self):
        """get sms verification token expiration status, reture True if expired else False"""
        if self.__send_time is not None:
            return True if self.duration > self.expiry else False
        return False

    @property
    def valid(self):
        """get sms verification token validation status, return True if valid else False"""
        return self.__valid

    def send_sms(self):
        """send sms message"""
        if self.valid and not self.expired:
            out = send(self.serial_no,
                       self.phone_number,
                       self.__signature,
                       self.__template_code,
                       json.dumps({'code': self.vrfcode}, ensure_ascii=False, default=str) if self.vrfcode else None)
            message = f'SMS code {self.vrfcode}' if self.signature == 'AUTHENTICATE_ID' else 'notification message'
            logger.info('send %s to phone %s', message, self.phone_number)
            response = json.loads(out)

            self.sms_response = response
            if response['Code'] == 'OK':
                self.__send_time = datetime.now()
                return True

            message = f'SMS code {self.vrfcode}' if self.signature == 'AUTHENTICATE_ID' else 'notification message'
            err = UserPhoneError('Failed to send %s to %s: %s' % (message, self.phone_number, out.decode('utf8')))
            logger.error(err.emsg + f' SIGNATURE: {self.signature} ' + f'TEMPLATE: {self.template}')
        else:
            logger.error('Try to send sms to phone %s with invalid or expired token', self.phone_number)
        return False

#    def refresh(self, force=False):
#        """refresh sms token verification code"""
#        if self.valid:
#            if force or self.expired:
#                if self.vrfcode in vrf_code.VRFCODE_POOL:
#                    del vrf_code.VRFCODE_POOL[self.vrfcode]
#                self.__vrfcode = vrf_code.new_vrfcode()
#                return self.send_sms()
#            return True
#
#        logger.error('Try to send sms to phone %s with invalid or expired token', self.phone_number)
#        return False
#
    def validate(self, phone_number, vrfcode):
        """validate verification code"""
        logger.info('%s, %s: try to validate user sms code', phone_number, vrfcode)
        if not isinstance(vrfcode, (str, int)):
            return '错误代码格式'
        if isinstance(vrfcode, int):
            vrfcode = '%06d' % (vrfcode)

        if not self.valid:
            return '无效验证请求'

        if phone_number != self.phone_number:
            return '无效电话号码'

        if vrfcode != self.vrfcode:
            return '错误验证代码'

        if self.expired:
            return '过期验证代码'

        self.__valid = False
        logger.info('phone %s user sms validate success', self.phone_number)
        return True

    def query_sms(self, current_page=1, page_size=10):
        """query sms verification token sms sent status"""
        if self.__send_time is not None:
            query = QuerySendDetailsRequest.QuerySendDetailsRequest()
            query.set_PhoneNumber(self.phone_number)
            query.set_BizId(self.serial_no)
            query.set_SendDate(self.__send_time.strftime('%Y%m%d'))
            query.set_CurrentPage(current_page)
            query.set_PageSize(page_size)
            response = ACS_CLIENT.do_action_with_exception(query)

            return response


# def send_vrfcode(phone_numbers, vrfcode=None):
#     """send verification codes to phone numbers"""
#     global SMS_TOKEN_POOL
#     response_queue = []
#     vrfcodes = []
#
#     if isinstance(phone_numbers, bytes):
#         phone_numbers = phone_numbers.decode('utf8')
#
#     if isinstance(phone_numbers, str):
#         number = 1
#     elif isinstance(phone_numbers, (tuple, list)):
#         number = len(phone_numbers)
#     else:
#         e = TypeError('invalid type for parameter: phone_numbers')
#         logger.error(e.message)
#         raise e
#
#     if vrfcode is not None:
#         if isinstance(phone_numbers, str) and isinstance(vrfcode, str):
#             out = send(phone_numbers, VRF_SIGNATURE, TEMPLATE_CODES['AUTHENTICATE_ID'], '{"code": "%s"}' %(vrfcode))
#             logger.info('Send verification code %s to phone %s', vrfcode, phone_numbers)
#             response = json.loads(out)
#             if response['Code'] != 'OK':
#                 logger.error('Failed sending verification code %s to phone %s: %s',
#                                  vrfcode, phone_numbers, out.decode('utf8'))
#                 print(out.decode('utf8'))
#                 raise RuntimeError('Sending verification code failed')
#
#             SMS_TOKEN_POOL[phone_numbers] = vrfcode
#             return ({phone_numbers: 'OK'},)
#
#         if isinstance(phone_numbers, (tuple, list)) and \
#                 isinstance(vrfcode, (tuple, list)) and \
#                 len(phone_numbers) == len(vrfcode):
#             pairs = dict(zip(phone_numbers, vrfcode))
#             for phone, code in pairs.items():
#                 out = send(phone, VRF_SIGNATURE, TEMPLATE_CODES['AUTHENTICATE_ID'], '{"code": "%s"}' %(code))
#                 logger.info('Send verification code %s to phone %s', code, phone)
#                 response = json.loads(out)
#                 response_queue.append({phone: response['Code']})
#                 if response['Code'] == 'OK':
#                     SMS_TOKEN_POOL[phone] = code
#
#             return tuple(response_queue)
#
#     if number == 1:
#         phone_number = phone_numbers if isinstance(phone_numbers, str) else phone_numbers[0]
#         pairs = {phone_number: vrf_code.new_vrfcode}
#     else:
#         while number > 0:
#             vrfcodes.append(vrf_code.new_vrfcode())
#             number -= 1
#         pairs = dict(zip(phone_numbers, vrfcodes))
#
#     for phone, code in pairs.items():
#         out = send(phone, VRF_SIGNATURE, TEMPLATE_CODES('AUTHENTICATE_ID'), '{"code": "%s"}' %(code))
#         logger.info('Send verification code %s to phone %s', code, phone)
#         response = json.loads(out)
#         response_queue.append({phone: response['Code']})
#         if response['Code'] == 'OK':
#             SMS_TOKEN_POOL[phone] = code
#
#     return tuple(response_queue)
#
#
# def fetch_vrfcode(phone_number):
#     """fetch sent verification code by giving phone_number"""
#     return SMS_TOKEN_POOL[phone_number] if phone_number in SMS_TOKEN_POOL else None
#
#
# def validate_vrfcode(phone_number, vrfcode):
#     """validate verification code with phone number"""
#     global SMS_TOKEN_POOL
#
#     if vrfcode in vrf_code.VRFCODE_POOL:
#         step1 = True
#     else:
#         step1 = False
#         msg1 = 'invalid verification code'
#
#     if phone_number in SMS_TOKEN_POOL:
#         step2 = True
#     else:
#         step2 = False
#         msg2 = 'invalid phone number'
#
#     if vrf_code.check_vrfcode_expiry(vrfcode):
#         step3 = True
#     else:
#         step3 = False
#         msg3 = 'expired verification code'
#
#     if SMS_TOKEN_POOL[phone_number] == vrfcode:
#         step4 = True
#     else:
#         step4 = False
#         msg4 = 'validation failed'
#
#     if step1 and step2 and step3 and step4:
#         del vrf_code.VRFCODE_POOL[vrfcode]
#         del SMS_TOKEN_POOL[phone_number]
#         return 'OK'
#
#     return 'Failed: %s, %s, %s, %s' % (msg1, msg2, msg3, msg4)
#
#
# def check_phone_vrfcode_expiry(phone_number):
#     """check vrfcode expiry with phone number"""
#
#     if phone_number not in SMS_TOKEN_POOL:
#         return False
#
#     vrfcode = SMS_TOKEN_POOL[phone_number]
#
#     return vrf_code.check_vrfcode_expiry(vrfcode)
