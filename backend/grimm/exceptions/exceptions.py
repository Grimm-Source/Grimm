#
# File: exceptions.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# ------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: define all exception classes and exception handler for this project.
#
# To-Dos:
#   1. make other supplements if needed.
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#   1. 2019/08/13, Ming, create first revision.
#

import sys
import inspect
# import pymysql.err


GRIMM_EXCEPTION_CLS = None


GRIMM_EXCEPTION_CODE = {
    'InternalError': 0,
    'UserError': 1,
    'UserNotFound': 2,
    'AppLoginFailed': 3,
    'UserRegisterFailed': 4,
    'UserLoginFailed': 5,
    'UserUpdateInfoFailed': 6,
    'UserExpiredPassword': 7,
    'UserInvalidPassword': 8,
    'UserEmailError': 9,
    'UserPhoneError': 10,
    }


__all__ = list(GRIMM_EXCEPTION_CODE.keys()) + ['exception_handler']


# invoking this function will trigger a general exception handler produdre.
# if specified error is not a pre-defined error, it will raise.
# if there is a private handler function in specified error, it will invoke.
# if no private handler function, it will update the msg_obj which stands
# for message object for front-end communication.
def exception_handler(e, msg_obj=None):
    '''handle all kinds of exception obj of Grimm.'''
    global GRIMM_EXCEPTION_CLS
    if GRIMM_EXCEPTION_CLS is None:
        exception_module = sys.modules[__name__]
        GRIMM_EXCEPTION_CLS = [cls for name,cls in inspect.getmembers(exception_module) if inspect.isclass(cls)]

    if e.__class__ in GRIMM_EXCEPTION_CLS:
        if msg_obj is None and not hasattr(e, 'handler'):
            print('No available handler process')
            raise e

        if hasattr(e, 'handler'):
            return e.handler()

        if 'error' in msg_obj:
            msg_obj['error'].append((e.ecode, e.emsg))
        else:
            msg_obj['error'] = [(e.ecode, e.msg), ]

    print('Unknown Exception Class')
    raise e


# define base exception classes to form the error tree.
class InternalError(Exception):
    '''
    Base Exception class for internal errors.
    '''
    def __init__(self):
        super().__init__()
        self.ecode = GRIMM_EXCEPTION_CODE['InternalError']
        self.emsg = 'Some internal error encountered'


class ExternalError(Exception):
    '''
    Base Exception class for external errors.
    '''
    def __init__(self):
        super().__init__()

"""
class DBError(DatabaseError.Error):
    '''
    Sub-base Exception class for database related errors.
    '''
    pass
"""


class UserError(ExternalError):
    '''
    Sub-base Exception class for user related errors.
    '''
    def __init__(self):
        super().__init__()
        self.ecode = GRIMM_EXCEPTION_CODE['UserError']
        self.emsg = 'Some user related error encountered'

"""
# define specific error types.
class PyVersionNotSupported(InternalError):
    '''
    this python version is not supported currently.
    '''
    def __init__(self, version):
        super().__init__()
        self.emsg = f'{version} is not supported, upgrade to 3.65 or later'
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__


class PkgNotInstalled(InternalError):
    '''
    some dependencies pkgs are not installed.
    '''
    def __init__(self, pkg=None):
        super().__init__()
        if pkg is None:
            self.emsg = f'required package not installed, check dependency'
        else:
            self.emsg = f'Package: {pkg} is required to run this system'
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__
"""


class UserNotFound(UserError):
    '''
    some user is not found in db.
    '''
    def __init__(self, user=None):
        super().__init__()
        if user is None:
            self.emsg = f'Current user not found'
        else:
            self.emsg = f'User {user} not found'
        self.ecode = GRIMM_EXCEPTION_CODE['UserNotFound']
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__


class AppLoginFailed(ExternalError):
    '''
    wechat app authentication failed.
    '''
    def __init__(self, reason=None):
        super().__init__()
        if reason is None:
            self.emsg = f'App login failed.'
        else:
            self.emsg = f'App login failed out of reason: {reason}'
        self.ecode = GRIMM_EXCEPTION_CODE['AppLoginFailed']
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__


class UserRegisterFailed(UserError):
    '''
    new user register failed for some reason.
    '''
    def __init__(self, user=None, reason=None):
        super().__init__()
        if user is None and reason is None:
            self.emsg = f'Current user registers failed'
        elif user is None and reason is not None:
            self.emsg = f'Current user registers failed out of reason: {reason}'
        elif reason is None and user is not None:
            self.emsg = f'User {user} registers failed'
        else:
            self.emsg = f'User {user} registers failed out of reason: {reason}'
        self.ecode = GRIMM_EXCEPTION_CODE['UserRegisterFailed']
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__


class UserLoginFailed(UserError):
    '''
    user login failed for some reason.
    '''
    def __init__(self, user=None, reason=None):
        super().__init__()
        if user is None and reason is None:
            self.emsg = f'Current user login failed'
        elif user is None and reason is not None:
            self.emsg = f'Current user login failed out of reason: {reason}'
        elif reason is None and user is not None:
            self.emsg = f'User {user} login failed'
        else:
            self.emsg = f'User {user} login failed out of reason: {reason}'
        self.ecode = GRIMM_EXCEPTION_CODE['UserLoginFailed']
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__


class UserUpdateInfoFailed(UserError):
    '''
    user update info failed for some reason.
    '''
    def __init__(self, info_key, user=None, reason=None):
        super().__init__()
        if user is None and reason is None:
            self.emsg = f'Current user update {info_key} failed'
        elif user is None and reason is not None:
            self.emsg = f'Current user update {info_key} failed out of reason: {reason}'
        elif reason is None and user is not None:
            self.emsg = f'User {user} update {info_key} failed'
        else:
            self.emsg = f'User {user} update {info_key} failed out of reason: {reason}'
        self.ecode = GRIMM_EXCEPTION_CODE['UserUpdateInfoFailed']
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__


class UserExpiredPassword(UserError):
    '''
    user password is expired, need to update new password.
    '''
    def __init__(self, user=None):
        super().__init__()
        if user is None:
            self.emsg = f'Current user\'s password expired, needs update'
        else:
            self.emsg = f'User {user} password expired, needs update'
        self.ecode = GRIMM_EXCEPTION_CODE['UserExpiredPassword']
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__


class UserInvalidPassword(UserError):
    '''
    password string inputtd from user is invalid, need to reinput.
    '''
    def __init__(self, reason, user=None):
        super().__init__()
        if user is None:
            self.emsg = f'Current input password is invalid, reason: {reason}'
        else:
            self.emsg = f'User {user} input password is invalid. reason: {reason}'
        self.ecode = GRIMM_EXCEPTION_CODE['UserInvalidPassword']
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__


class UserEmailError(UserError):
    """
    something goes wrong with user email process.
    """
    def __init__(self, reason, user=None):
        super().__init__()
        if user is None:
            self.emsg = f'User email process failed, reason: {reason}'
        else:
            self.emsg = f'User {user} email process failed, reason: {reason}'
        self.ecode = GRIMM_EXCEPTION_CODE['UserEmailError']
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__


class UserPhoneError(UserError):
    """
    something goes wrong with user phone process.
    """
    def __init__(self, reason, user=None):
        super().__init__()
        if user is None:
            self.emsg = f'User phone process failed, reason: {reason}'
        else:
            self.emsg = f'User {user} phone process failed, reason: {reason}'
        self.ecode = GRIMM_EXCEPTION_CODE['UserPhoneError']
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__


class SQLValueError(InternalError):
    '''
    bad SQL transaction syntax.
    '''
    def __init__(self, operation, msg=None):
        super().__init__()
        if msg is None:
            self.emsg = f'SQL syntax error found at process {operation}'
        else:
            self.emsg = f'SQL syntax error found at process {operation}, {msg}'
        self.ecode = GRIMM_EXCEPTION_CODE['InternalError']
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__


class SQLConnectionError(InternalError):
    '''
    uninitialized or expired database connection.
    '''
    def __init__(self, reason=None):
        super().__init__()
        if reason is None:
            self.emsg = f'database connection is uninitialized or invalid'
        else:
            self.emsg = f'database connection is uninitialized or invalid, reason: {reason}'
        self.ecode = GRIMM_EXCEPTION_CODE['InternalError']
        self.args = (self.ecode, self.emsg)

    def __str__(self):
        return '({0}, {1})'.format(self.ecode, self.emsg)
    __repr__ = __str__
