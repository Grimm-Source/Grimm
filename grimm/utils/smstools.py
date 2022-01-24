from tencentcloud.common import credential
from tencentcloud.sms.v20210111 import sms_client, models
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from config import GrimmConfig
from grimm import logger
from grimm.utils import constants


def send_short_message(phone_number_list, template_id, **kwargs):
    """ kwargs must contains 'phone_number_list', 'template_id', and other template_params """
    cred = credential.Credential(GrimmConfig.TENCENT_SECRET_ID, GrimmConfig.TENCENT_SECRET_KEY)
    http_profile = HttpProfile()
    http_profile.reqMethod = "POST"
    http_profile.reqTimeout = 30
    http_profile.endpoint = "sms.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.signMethod = "TC3-HMAC-SHA256"
    client_profile.language = "en-US"
    client_profile.httpProfile = http_profile
    client = sms_client.SmsClient(cred, "ap-shanghai", client_profile)
    req = models.SendSmsRequest()
    req.SmsSdkAppId = GrimmConfig.TENCENT_SDK_APP_ID
    req.SignName = constants.TENCENT_SMS_SIGNATURE
    req.ExtendCode = ""
    req.SessionContext = ""
    req.SenderId = ""
    req.PhoneNumberSet = ['+86%s' % n for n in phone_number_list]
    req.TemplateId = template_id
    if template_id == constants.TEMPLATE_CODES['VOLUNTEER_PICKUP']:
        req.TemplateParamSet = [
            kwargs.get('impaired_name'),
            kwargs.get('volunteer_name'),
            kwargs.get('volunteer_phone')
        ]
    elif template_id == constants.TEMPLATE_CODES['VOLUNTEER_CANCEL_PICKUP']:
        req.TemplateParamSet = [
            kwargs.get('impaired_name'),
            kwargs.get('volunteer_name'),
            kwargs.get('volunteer_phone')
        ]
    elif template_id == constants.TEMPLATE_CODES['IMPAIRED_CANCEL_ACTIVITY']:
        req.TemplateParamSet = [
            kwargs.get('volunteer_name'),
            kwargs.get('impaired_name'),
            kwargs.get('impaired_phone')
        ]
    elif template_id == constants.TEMPLATE_CODES['VOLUNTEER_CANCEL_ACTIVITY']:
        req.TemplateParamSet = [
            kwargs.get('impaired_name'),
            kwargs.get('volunteer_name'),
            kwargs.get('volunteer_phone')
        ]
    resp = client.SendSms(req)
    resp_str = resp.to_json_string(indent=2)
    logger.info(resp_str)
