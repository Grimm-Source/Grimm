# Python 3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from datetime import timedelta

def parseCsv(f):
    with open(f, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return lines

def importUser(f, r):
    vols = parseCsv(f)
    
    cols = len(vols[0].split(','))
    print(cols)
    vol_users = []
    for v in vols[1:]:
        vs = v.strip().split(',')
        if not len(vs) == cols:
            print(v)
        v_user = {};
        name = vs[0]
        if '+' in name:
            continue
        if '(' in name:
            name = name.split('(')[0].strip()
        v_user['name'] = name
        phone = vs[1].strip().strip('"')
        if '、' in phone:
            phone = phone.split('、')[0]
        v_user['phone'] = phone
        idcard = vs[2]
        if not len(vs[2]) == 18:
            idcard = ''
        v_user['idcard'] = idcard
        v_user['gender'] = 0
        act_joined = vs[3]
        if not vs[3].isnumeric():
            act_joined = 0
            if not vs[3] == '':
                print(v)
        else:
            act_joined = int(vs[3])
        v_user['act_joined'] = act_joined
        v_user['remark'] = vs[9]
        reg_date = vs[10]
        if '年' in reg_date:
            reg_date = reg_date.split('年')[0]
        if reg_date.isnumeric():
            reg_date = datetime(int(reg_date), 1, 1).strftime('%Y-%m-%d')
        else:
            reg_date = datetime.strptime(reg_date, '%m/%d/%Y').strftime('%Y-%m-%d')
        v_user['reg_date'] = reg_date
        v_user['role'] = r
        v_user['audit_status'] = 2
        vol_users.append(v_user)
    return vol_users
