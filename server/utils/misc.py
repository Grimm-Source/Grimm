#
# File: server/utils/misc.py
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
import io
import re
import json
import werkzeug
import socket
import datetime
import contextlib
from pathlib import Path
from flask import jsonify


# get parent directory
def pardir(dirname):
    '''get parent directory path'''
    return str(Path(dirname).parent)


# load json data from flask request
def json_load_request(request, keys=None):
    '''load request json data object from front-end'''
    info_dict = None
    if isinstance(request, werkzeug.local.LocalProxy):
        data = request.get_data().decode('utf8')
        if data:
            info_dict = json.loads(data)

    if keys is not None:
        # get item as dict if keys is specified as dict
        if isinstance(keys, (tuple, list)):
            return {k: info_dict[k] for k in keys if k in info_dict}
        # get item as value if keys is specified as string key
        return info_dict[keys] if keys in info_dict else None

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


# feedback success response
def request_success(**kwargs):
    if kwargs:
        response = dict(kwargs)
        if 'status' not in response:
            response['status'] = 'success'
        return jsonify(response)

    return jsonify({'status': 'success'})


# feedback failure response
def request_fail(msg=None, **kwargs):
    if kwargs:
        response = dict(kwargs)
        if 'status' not in response:
            response['status'] = 'failure'
    else:
        response = {'status': 'failure'}
    if msg is not None:
        response['message'] = msg

    return jsonify(response)


# UNIX tty input to avoid EOFError of built-in input function for subprocess method
def tty_input(prompt=""):
    with contextlib.ExitStack() as stack:
        try:
            fd = os.open('/dev/tty', os.O_RDWR|os.O_NOCTTY)
            tty = io.FileIO(fd, 'w+')
            stack.enter_context(tty)    # register context callback
            stream = io.TextIOWrapper(tty)
            stack.enter_context(stream)
        except OSError as e:
            # if tty dev is unavailable, raise
            stack.close()
            raise

        prompt = str(prompt)
        if prompt:
            try:
                stream.write(prompt)
            except UnicodeEncodeError:
                prompt = prompt.encode(stream.encoding, 'replace')
                prompt = prompt.decode(stream.encoding)
                stream.write(prompt)
            stream.flush()

        line = stream.readline()
        if not line:
            raise EOFError
        if line[-1] == '\n':
            line = line[:-1]

        stream.flush()
        return line
