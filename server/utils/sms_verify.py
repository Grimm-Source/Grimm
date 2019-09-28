#
# File: sms.py
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


import sys
import json
import time
from dysms.aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
import dysms.const as const
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT


import vrfcode as vrf_code
from server import sys_logger


SIGNATURE = '视障人士志愿者平台'
TEMPLATE_CODES = {
     'ID_AUTHENTICATION': 'SMS_134125051',
    'USER_LOGIN_CONFIRM': 'SMS_134125050',
     'USER_REGISTRATION': 'SMS_134125048',
       'CHANGE_PASSWORD': 'SMS_134125047',
           'UPDATE_INFO': 'SMS_134125046'
    }

ACS_CLIENT = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, const.REGION)
region_provider.add_endpoint(const.PRODUCT_NAME, const.REGION, const.DOMAIN)


SENT_VRFCODE_PAIRS = {}


def send(phone_numbers, sign_name, template_code, template_param=None):
    '''send sms message to phone numbers'''
    serial_id = vrf_code.new_serial_number()
    smsRequest = SendSmsRequest.SendSmsRequest()
    smsRequest.set_TemplateCode(template_code)
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)
    smsRequest.set_OutId(serial_id)
    smsRequest.set_SignName(sign_name)
    # 数据提交方式
    # smsRequest.set_method(MT.POST)
    # 数据提交格式
    # smsRequest.set_accept_format(FT.JSON)
    smsRequest.set_PhoneNumbers(phone_numbers)
    smsResponse = ACS_CLIENT.do_action_with_exception(smsRequest)

    return smsResponse


class VRF_Token(object):
    '''verification token class'''
    def __init__(self, phone_number, expiry=120,
                 access_id=const.ACCESS_KEY_ID,
                 access_secret=const.ACCESS_KEY_SECRET,
                 signature=SIGNATURE,
                 template_code=TEMPLATE_CODES['ID_AUTHENTICATION']):
        '''initialize verification token objects'''
        if isinstance(phone_number, str) and isinstance(expiry, int):
            self.__phone_number = phone_number
            self.__expiry = expiry
            self.__vrfcode = vrf_code.new_vrfcode()
            self.__access_id = access_id
            self.__access_secret = access_secret
            self.__signature = signature
            self.__template_code = template_code
            self.__start_time = int(time.time())
            self.sms_reponse = None
            self.__valid = True
        else:
            raise TypeError('invalid value type to initializing a token')

    @property
    def vrfcode(self):
        '''get token verification code'''
        return self.__vrfcode

    @property
    def phone_number(self):
        '''get token phone number'''
        return self.__phone_number

    @property
    def template_code(self):
        '''get current token template code'''
        return self.__template_code

    @template_code.setter
    def template_code(self, new_template_code):
        '''set new token template code'''
        if new_template_code in TEMPLATE_CODES.values():
            self.__template_code = new_template_code
        else:
            raise ValueError('invalid template code')

    @property
    def expired(self):
        '''get verification token status, reture True if expired, otherwise False'''
        duration = time.time() - self.__start_time
        return True if duration > self.__expiry else False

    @property
    def expiry(self):
        '''get verification token expiry seconds value'''
        return self.__expiry

    @expiry.setter
    def expiry(self, new_expiry):
        '''set new expiry time'''
        if not isinstance(new_expiry, int):
            raise TypeError('set expiry with number of seconds')
        if new_expiry > self.expiry:
            self.__expiry = new_expiry

    def send_sms(self):
        '''send sms message'''
        if self.__valid and not self.expired:
            out = send(self.phone_number,
                       self.__signature,
                       self.__template_code,
                       '{"code": "%s"}' % (self.vrfcode))
            sys_logger.info('send verification code %s to phone %s', self.vrfcode, self.phone_number)
            response = json.loads(out)

            if response['Code'] == 'OK':
                return True
            err_msg = 'Failed to send verification code %s to phone %s: %s' % (self.vrfcode,
                                                                               self.phone_number,
                                                                               out.decode('utf8'))
            sys_logger.error(err_msg)
            print(err_msg)
            raise RuntimeError(err_msg)
        else:
            sys_logger.error('Try to send sms to phone %s with invalid or expired token', self.phone_number)
            raise ValueError('invalid or expired token')

    def refresh(self, force=False):
        '''refresh token verification code'''
        if self.__valid:
            if force or self.expired:
                if self.vrfcode in vrf_code.VRFCODES:
                    del vrf_code.VRFCODES[self.vrfcode]
                self.__vrfcode = vrf_code.new_vrfcode()
                self.__start_time = int(time.time())
                return self.send_sms()

            return True
        else:
            sys_logger.error('Try to send sms to phone %s with invalid or expired token', self.phone_number)
            raise ValueError('invalid or expired token')

    def validate(self, phone_number, vrfcode):
        '''validate verification code'''
        if not isinstance(vrfcode, (str, int)):
            raise TypeError('invalied value type for vrfcode')
        if isinstance(vrfcode, int):
            vrfcode = '%06d' % (vrfcode)

        if not self.__valid:
            return 'Failed: token validated already'

        if phone_number != self.phone_number:
            return 'Failed: wrong phone number: ' + phone_number

        if vrfcode != self.vrfcode:
            return 'Failed: wrong verification code: ' + vrfcode

        if self.expired:
            return 'Failed: expired verification code'

        self.__valid = False
        return 'Success: OK'


# def send_vrfcode(phone_numbers, vrfcode=None):
#     '''send verification codes to phone numbers'''
#     global SENT_VRFCODE_PAIRS
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
#         sys_logger.error(e.message)
#         raise e
#
#     if vrfcode is not None:
#         if isinstance(phone_numbers, str) and isinstance(vrfcode, str):
#             out = send(phone_numbers, SIGNATURE, TEMPLATE_CODES['ID_AUTHENTICATION'], '{"code": "%s"}' %(vrfcode))
#             sys_logger.info('Send verification code %s to phone %s', vrfcode, phone_numbers)
#             response = json.loads(out)
#             if response['Code'] != 'OK':
#                 sys_logger.error('Failed sending verification code %s to phone %s: %s',
#                                  vrfcode, phone_numbers, out.decode('utf8'))
#                 print(out.decode('utf8'))
#                 raise RuntimeError('Sending verification code failed')
#
#             SENT_VRFCODE_PAIRS[phone_numbers] = vrfcode
#             return ({phone_numbers: 'OK'},)
#
#         if isinstance(phone_numbers, (tuple, list)) and \
#                 isinstance(vrfcode, (tuple, list)) and \
#                 len(phone_numbers) == len(vrfcode):
#             pairs = dict(zip(phone_numbers, vrfcode))
#             for phone, code in pairs.items():
#                 out = send(phone, SIGNATURE, TEMPLATE_CODES['ID_AUTHENTICATION'], '{"code": "%s"}' %(code))
#                 sys_logger.info('Send verification code %s to phone %s', code, phone)
#                 response = json.loads(out)
#                 response_queue.append({phone: response['Code']})
#                 if response['Code'] == 'OK':
#                     SENT_VRFCODE_PAIRS[phone] = code
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
#         out = send(phone, SIGNATURE, TEMPLATE_CODES('ID_AUTHENTICATION'), '{"code": "%s"}' %(code))
#         sys_logger.info('Send verification code %s to phone %s', code, phone)
#         response = json.loads(out)
#         response_queue.append({phone: response['Code']})
#         if response['Code'] == 'OK':
#             SENT_VRFCODE_PAIRS[phone] = code
#
#     return tuple(response_queue)
#
#
# def fetch_vrfcode(phone_number):
#     '''fetch sent verification code by giving phone_number'''
#     return SENT_VRFCODE_PAIRS[phone_number] if phone_number in SENT_VRFCODE_PAIRS else None
#
#
# def validate_vrfcode(phone_number, vrfcode):
#     '''validate verification code with phone number'''
#     global SENT_VRFCODE_PAIRS
#
#     if vrfcode in vrf_code.VRFCODES:
#         step1 = True
#     else:
#         step1 = False
#         msg1 = 'invalid verification code'
#
#     if phone_number in SENT_VRFCODE_PAIRS:
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
#     if SENT_VRFCODE_PAIRS[phone_number] == vrfcode:
#         step4 = True
#     else:
#         step4 = False
#         msg4 = 'validation failed'
#
#     if step1 and step2 and step3 and step4:
#         del vrf_code.VRFCODES[vrfcode]
#         del SENT_VRFCODE_PAIRS[phone_number]
#         return 'OK'
#
#     return 'Failed: %s, %s, %s, %s' % (msg1, msg2, msg3, msg4)
#
#
# def check_phone_vrfcode_expiry(phone_number):
#     '''check vrfcode expiry with phone number'''
#
#     if phone_number not in SENT_VRFCODE_PAIRS:
#         return False
#
#     vrfcode = SENT_VRFCODE_PAIRS[phone_number]
#
#     return vrf_code.check_vrfcode_expiry(vrfcode)
