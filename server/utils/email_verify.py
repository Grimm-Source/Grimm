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




import smtplib
import ssl
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import urllib3

from itsdangerous import URLSafeTimedSerializer



sender = '497802561@qq.com'
smtp_server = 'smtp.qq.com'
smtp_port = 465
passcode = 'tgpaibcvklzabiah'


def send(receiver, verify_url):
    '''send email which contains verification url link'''
    root_msg = MIMEMultipart('related')
    root_msg['Subject'] = 'Verify New Email Address'
    root_msg['From'] = sender
    root_msg['To'] = receiver
    root_msg.preamble = 'This is a multi-part message in MIME format.'
