import configparser
import os
import uuid

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    JSON_SORT_KEYS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    SECURITY_PASSWORD_SALT = uuid.uuid4().hex


class GrimmConfig(Config):
    config = configparser.RawConfigParser()
    env = os.environ.get('FLASK_ENV')
    if env == 'production':
        config.read(BASE_DIR + '/grimm-prod.ini')
    elif env == 'testing':
        config.read(BASE_DIR + '/grimm-test.ini')
    else:
        config.read(BASE_DIR + '/grimm-dev.ini')

    # for wei xin setting
    WX_APP_ID = config.get('WX', 'WX_APP_ID')
    WX_APP_SECRET = config.get('WX', 'WX_APP_SECRET')

    # for db setting
    SQLALCHEMY_DATABASE_URI = config.get('DB', 'SQLALCHEMY_DATABASE_URI')

    # for sms setting
    SMS_ACCESS_KEY_ID = config.get('SMS', 'SMS_ACCESS_KEY_ID')
    SMS_ACCESS_KEY_SECRET = config.get('SMS', 'SMS_ACCESS_KEY_SECRET')
    TENCENT_SECRET_ID = config.get('SMS', 'TENCENT_SECRET_ID')
    TENCENT_SECRET_KEY = config.get('SMS', 'TENCENT_SECRET_KEY')
    TENCENT_SDK_APP_ID = config.get('SMS', 'TENCENT_SDK_APP_ID')

    # for smtp setting
    SMTP_ADDRESS = config.get('SMTP', 'SMTP_ADDRESS')
    SMTP_PORT = config.get('SMTP', 'SMTP_PORT')
    SMTP_SERVER = config.get('SMTP', 'SMTP_SERVER')
    SMTP_PASSWORD = config.get('SMTP', 'SMTP_PASSWORD')

    # for api
    TENCENT_LOCATION_SERVICE_URL = config.get('API', 'TENCENT_LOCATION_SERVICE_URL')
    TENCENT_LOCATION_SERVICE_KEY = config.get('API', 'TENCENT_LOCATION_SERVICE_KEY')
    WECHAT_TOKEN_GET_URL = config.get('API', 'WECHAT_TOKEN_GET_URL')
    WECHAT_MESSAGE_SUBSCRIBE_URL = config.get('API', 'WECHAT_MESSAGE_SUBSCRIBE_URL')

    # for app
    GRIMM_EXCEPTION_MSG_ROOM = config.get('APP', 'GRIMM_EXCEPTION_MSG_ROOM')
    GRIMM_BOT_TOKEN = config.get('APP', 'GRIMM_BOT_TOKEN')
    GRIMM_BOT_MESSAGE_URL = config.get('APP', 'GRIMM_BOT_MESSAGE_URL')
    GRIMM_USER_DOCUMENT_UPLOAD_PATH = config.get('APP', 'GRIMM_USER_DOCUMENT_UPLOAD_PATH', fallback="./user-documents/")
    GRIMM_DISABLED_ID_UPLOAD_PATH = config.get('APP', 'GRIMM_DISABLED_ID_UPLOAD_PATH', fallback="./user-disabled-id/")
