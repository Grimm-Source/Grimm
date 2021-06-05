#
# File: email_verify.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: do email related jobs.
#
# To-Dos:
#   1. make other supplements if needed.
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#   1. 2019/08/19, Ming, create first revision.
#

import os
import re
import smtplib
import ssl
import dns.resolver
import email
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from flask import abort

import grimm.utils.vrfcode as vrfcode
from grimm import logger, db, GrimmConfig
from grimm.exceptions.exceptions import UserEmailError
from grimm.models.admin import Admin
from grimm.utils.misctools import get_pardir
from grimm.utils.constants import DEFAULT_PROTOCOL, EMAIL_REGEX as REGEX


sender = None
smtp_domain = None
smtp_port = None
passcode = None

if passcode is None:
    sender = GrimmConfig.SMTP_ADDRESS
    smtp_domain = GrimmConfig.SMTP_SERVER
    smtp_port = GrimmConfig.SMTP_PORT
    passcode = GrimmConfig.SMTP_PASSWORD

SMTP_CONNECTION = None
EMAIL_TOKEN_POOL = {}


def append_token(token):
    """append token to be verified in token queue"""
    global EMAIL_TOKEN_POOL
    if token.addr not in EMAIL_TOKEN_POOL:
        EMAIL_TOKEN_POOL[token.addr] = token


def fetch_token(addr):
    """fetch token with user email address"""
    return None if addr not in EMAIL_TOKEN_POOL else EMAIL_TOKEN_POOL[addr]


def drop_token(addr):
    """drop token that has been verified in token queue"""
    global EMAIL_TOKEN_POOL
    token = fetch_token(addr)
    if token is not None and \
            (token.expired or not token.valid):
        del EMAIL_TOKEN_POOL[token.addr]


def check_email_addr(addr, verify_exists=False):
    """verify if a email address exists with server domain"""
    if re.match(REGEX, addr.lower()) is None:
        err = UserEmailError('invalid email address')
        logger.error(err.emsg)
        return False
    if verify_exists:
        domain = addr.split('@')[1]
        records = dns.resolver.query(domain, 'MX')
        mxrecord = str(records[0].exchange)
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mxrecord)
        server.helo(server.local_hostname)
        server.mail(sender)
        code, msg = server.rcpt(addr)
        server.quit()
        if code != 250:
            err = UserEmailError(msg)
            logger.error(err.emsg)
            return False

    return True


def smtp_connection_status():
    """get global smtp connection status, True is connected, otherwise False"""
    if SMTP_CONNECTION is not None:
        try:
            status = SMTP_CONNECTION.noop()[0]
        except:
            status = -1

        if status == 250:
            return True

    return False


def send(email_sample, receiver, subject, plain, replacement, attachment_file=None):
    """send verification email to new user"""
    global SMTP_CONNECTION
    path = get_pardir(os.path.abspath(__file__))
    # check global smtp connection status and reconnect if necessary
    if not smtp_connection_status():
        context = ssl.create_default_context()
        SMTP_CONNECTION = smtplib.SMTP_SSL(smtp_domain, smtp_port, context=context, timeout=3600)
        response = SMTP_CONNECTION.login(sender, passcode)
        if response[0] != 235:
            err = UserEmailError('Local smtp service connection failed: %s', response[1].decode('utf8'))
            logger.error(err.emsg)
            raise err
    # create MIME format email
    message = MIMEMultipart('related')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = receiver
    message.preamble = 'This is a multi-part message in MIME format.'
    # create alternative content
    content = MIMEMultipart('alternative')
    content['Subject'] = subject
    content['From'] = sender
    content['To'] = receiver
    message.attach(content)

    ## add attachment file
    file_name = os.path.basename(attachment_file)
    with open(attachment_file, "rb") as attachment:
        part = MIMEApplication(attachment.read(),
                               Name=file_name)

    part['Content-Disposition'] = 'attachment; filename="%s"' % file_name

    # Add attachment to message
    message.attach(part)

    # add html part
    fp_email = open(path + '/' + email_sample, mode='r')
    html_src = email.message_from_file(fp_email).as_string()
    fp_email.close()
    html = html_src.replace("SUBSTITUTION", replacement)
    part1 = MIMEText(html, "html", "utf-8")
    content.attach(part1)
    # attach plain text part
    text = plain + replacement
    part2 = MIMEText(text, "plain", "utf-8")
    content.attach(part2)
    # attach images resources
    fp_image1 = open(path + '/email_resource/images/grimm-logo1.png', mode='rb')
    image1 = MIMEImage(fp_image1.read())
    fp_image1.close()
    image1.add_header('Content-ID', '<image1>')
    message.attach(image1)
    fp_image2 = open(path + '/email_resource/images/grimm-logo2.png', mode='rb')
    image2 = MIMEImage(fp_image2.read())
    fp_image2.close()
    image2.add_header('Content-ID', '<image2>')
    message.attach(image2)
    # connect smtp server and send email
    status = SMTP_CONNECTION.sendmail(sender, receiver, message.as_string())
    if status:
        err = UserEmailError('send email to address %s failed: %s', receiver, status)
        logger.error(err.emsg)
    return status


def send_confirm(receiver, vrfurl, email_sample='email_resource/confirm-admin.html'):
    """send confirm email to admin user"""
    subject = 'Grimm Verify New Email Address'
    plain = """\
    您好，欢迎注册使用视障人士志愿者平台，请点击下方链接完成邮箱认证:
     """
    if DEFAULT_PROTOCOL not in vrfurl:
        url = DEFAULT_PROTOCOL + '://' + vrfurl.strip()
    else:
        url = vrfurl.strip()

    return send(email_sample=email_sample,
                receiver=receiver,
                plain=plain,
                subject=subject,
                replacement=url)


def send_reset(receiver, email_sample='email_resource/reset-admin.html'):
    """send reset email to admin user"""
    subject = 'Grimm Reset User Password'
    plain = """\
    请使用新密码登录账户:
     """
    new_pass = vrfcode.new_serial_number(8)

    return send(email_sample=email_sample,
                receiver=receiver,
                plain=plain,
                subject=subject,
                replacement=new_pass), new_pass


class EmailVerifyToken(object):
    """email verification token class"""
    def __init__(self, addr, expiry=3600):
        """initialize email verification token objects"""
        if isinstance(addr, str) and isinstance(expiry, int):
            # validate receiver email format
            if check_email_addr(addr):
                self.__addr = addr
                self.__expiry = expiry
                self.__vrfurl = vrfcode.new_vrfurl(addr)
                self.__send_time = None
                self.__valid = True
                self.smtp_response = None
                self.__email_sample = 'email_resource/confirm-admin.html'
            else:
                err = UserEmailError('invalid receiver email: %s', addr)
                logger.error(err.emsg)
                raise err
        else:
            raise TypeError('invalid parameter type to initialize email token')

    @property
    def vrfurl(self):
        """get email token verification url"""
        return self.__vrfurl

    @property
    def addr(self):
        """get email verification token receiver address"""
        return self.__addr

    @property
    def duration(self):
        """get email verification token instant duration"""
        if self.__send_time is not None:
            return time.time() - self.__send_time.timestamp()
        return 0.0

    @property
    def expiry(self):
        """get email verification token expiry seconds const"""
        return self.__expiry

    @expiry.setter
    def expiry(self, new_expiry):
        """set new expiry time seconds"""
        if not isinstance(new_expiry, int) and new_expiry > self.expiry:
            self.__expiry = new_expiry

    @property
    def expired(self):
        """get email verification token expiration status, True if expired else False"""
        if self.__send_time is not None:
            return True if self.duration > self.expiry else False
        return False

    @property
    def valid(self):
        """get email verification token validation status, True if valid else False"""
        return self.__valid

    @valid.setter
    def valid(self, value):
        """set token valid status when validating token"""
        if isinstance(value, bool):
            self.__valid == value

    @property
    def email_sample(self):
        """get email sample file name in relative path format"""
        return self.__email_sample

    def send_email(self):
        """send verification email to receiver"""
        if self.valid and not self.expired:
            response = send_confirm(email_sample=self.email_sample,
                                    receiver=self.addr,
                                    vrfurl=self.vrfurl)
            logger.info('send verification email to address: %s', self.addr)
            if response:
                err = UserEmailError('Failed to send email to: %s, %s',
                                     self.addr,
                                     response)
                logger.error(err.emsg)
                return False
            self.__send_time = datetime.now()
            return True

        logger.error('Try to send email to %s with invalid or expired token', self.addr)
        return False

#    def resend(self, force=True):
#        """refresh verification email and resend"""
#        if self.valid:
#            if force or self.expired:
#                self.__vrfurl = vrfcode.new_vrfurl(self.addr)
#                return self.send_email()
#            return True
#
#        logger.error('Try to send verification email to address %s with invalid or expired token', self.vrftoken)
#        raise RuntimeError('invalid or expired token')
#
#    def validate(self, token):
#        """confirm email verification"""
#        if isinstance(token, bytes):
#            token = token.decode('utf8')
#        if not isinstance(token, str):
#            raise TypeError('invalied argument for email token')
#
#        if not self.valid:
#            return 'Failed: 无效验证请求'
#
#        if self.expired:
#            return 'Failed: 过期验证链接'
#
#        if vrfcode.verify_vrftoken(self.addr, token):
#            self.__valid = False
#            return True
#
#        return 'Failed: 验证邮箱失败'


def validate_email(token):
    """validate confirm email verification"""
    if isinstance(token, bytes):
        token = token.decode('utf8')
    if not isinstance(token, str):
        logger.warning('email_verify.validate_email: invalid argument for email token')
        return False

    addr = vrfcode.parse_vrftoken(token)

    if addr is not None:
        token = fetch_token(addr)
        admin_info = db.session.query(Admin).filter(Admin.email == addr).first()
        if token is not None and admin_info:
            if token.valid and not token.expired:
                try:
                    admin_info.email_verified = 1
                    db.session.commit()
                    token.valid = False
                    # redirect(url_for('admin_login'))
                    return True
                except:
                    pass
        drop_token(addr)
    abort(404)
    return False
