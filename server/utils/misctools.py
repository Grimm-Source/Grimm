#
# File: misctool.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: contains misc tool functions.
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


import os
import re
import json
import werkzeug
import socket
import datetime


# get parent directory
def get_pardir(_dir):
    '''truncate path to get parent directory path'''
    if _dir[-1] is os.path.sep:
        _dir = _dir.rstrip(os.path.sep)
    d = _dir.split(os.path.sep)
    d.pop()
    pd = os.path.sep.join(d)

    return pd


# dump json data as response
def json_dump_http_response(data):
    '''dump http response json data object to front-end'''
    return data


# load json data from flask request
def json_load_http_request(request, keys=None):
    '''load http request json data object from front-end'''
    if isinstance(request, werkzeug.local.LocalProxy):
        data = request.get_data().decode('utf8')
        info_dict = json.loads(data) if data else {}

    if keys is not None:
        # get item as value if keys is specified as string key
        if isinstance(keys, str):
            return info_dict[keys] if keys in info_dict else None
        # get item as dict if keys is specified as dict
        if isinstance(keys, (tuple, list)):
            return {k: info_dict[k] for k in keys if k in info_dict}

    return info_dict


# get local host IP
def get_host_ip(hostname=None):
    '''get local host IP with socket DNS connection'''
    if hostname is None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip_str = sock.getsockname()[0]
        sock.close()
    else:
        local_ip_str = socket.gethostbyname(hostname)
    return local_ip_str.strip()


# check host name format
def is_hostname(hostname):
    '''check if some string is hostname or not'''
    if len(hostname) > 255:
        return False
    if hostname[-1] == '.':
        hostname = hostname[:-1]

    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


# check host ip format
def is_ipv4_addr(ip_str):
    '''check if some string is ipv4 address or not'''
    try:
        socket.inet_aton(ip_str)
        return True
    except:
        return False


# validate some hostname with socket connection
def validate_hostname(hostname):
    '''validate some string with socket to check if it's online host'''
    try:
        socket.gethostbyname(hostname)
        return True
    except:
        return False


# calc time duration
def calc_duration(start, end):
    '''calculate time duration, return dict'''
    if isinstance(start, datetime.datetime) and isinstance(end, datetime.datetime):
        delta = end - start
        if delta.total_seconds() > 0:
            days = delta.days
            hours = int(delta.seconds / 3600)
            minites = int((delta.seconds % 3600) / 60)
            seconds = (delta.seconds % 3600) % 60
            return {'day': days, 'hour': hours, 'min': minites, 'sec': seconds}
    return {}
