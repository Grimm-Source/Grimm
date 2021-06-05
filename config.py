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
    config.read(BASE_DIR + '/grimm-dev.ini')  # switch env here if needed

    # for wei xin setting
    WX_APP_ID = config.get('WX', 'WX_APP_ID')
    WX_APP_SECRET = config.get('WX', 'WX_APP_SECRET')

    # for db setting
    SQLALCHEMY_DATABASE_URI = config.get('DB', 'SQLALCHEMY_DATABASE_URI')

    # for sms setting
    SMS_ACCESS_KEY_ID = config.get('SMS', 'SMS_ACCESS_KEY_ID')
    SMS_ACCESS_KEY_SECRET = config.get('SMS', 'SMS_ACCESS_KEY_SECRET')

    # for smtp setting
    SMTP_ADDRESS = config.get('SMTP', 'SMTP_ADDRESS')
    SMTP_PORT = config.get('SMTP', 'SMTP_PORT')
    SMTP_SERVER = config.get('SMTP', 'SMTP_SERVER')
    SMTP_PASSWORD = config.get('SMTP', 'SMTP_PASSWORD')
