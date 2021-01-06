# Python 3
# -*- coding: utf-8 -*-

import sys
import os
import csv
import argparse
from datetime import datetime
# jump out to upper directory, then `server` becomes a pure python package.
# must be placed ahead of other imports !!!
if '..' not in sys.path:
    sys.path.append('..')

# load services
import server
import server.core.db as db
import server.utils.db_utils as db_utils
import server.utils.import_user as imptuser
import server.utils.misctools as misc

from server.core.const import ROOT_PASSWORD, HOST, PORT, FORCE_LOAD, DAEMON_LOAD, SESSION_LOG

def initialize():
    parser = argparse.ArgumentParser(
        prog='grimm_backup',
        description='backup or restore Grimm database',
        add_help=False)
    parser.add_argument('-r', '--restore', dest='restore',action='store_true',
        help='restore the database saved data in csv file located in ./dbbk/.')
    parser.add_argument('-t', '--task', dest='task', 
        help='string to tell what task to do.')
    parser.add_argument('-h', '--help', action='help',
        help='Show this help message and exit.')
    cmdargs = parser.parse_args()
    return cmdargs

def get_db_backup_dir():
    return os.path.join(misc.get_pardir(os.path.abspath(__file__)), 'dbbk')

def export_table(tbl, f):
    print('exporting %s to %s' % (tbl, f))
    columns = db.query("""
        SELECT column_name from information_schema.columns where table_name = '%s' and table_schema  = '%s'
        """ % (tbl, db.DB_NAME))
    expdata = tuple([tuple([x for x, in columns])])
    data = db.query("""SELECT * from %s""" % tbl)
    expdata += data
    with open(f, 'wt', encoding='utf-8') as bkf:
       csv_out = csv.writer(bkf)
       csv_out.writerows(expdata)

def export_all_tables():
    dbbkdir = get_db_backup_dir()
    if not os.path.isdir(dbbkdir):
        os.mkdir(dbbkdir)
    db.init_connection(force=FORCE_LOAD)
    tables = db.query("""
        SELECT table_name from information_schema.tables where table_schema = '%s'
        """ % db.DB_NAME)
    for tbl, in tables:
        export_table(tbl, os.path.join(dbbkdir, tbl + '.bk.csv'))

def import_table(f, tbl, existing_rows='update'):
    if not db.exist_table(tbl):
        print('table: %s not exists, by pass %s' % (tbl, f))
        return
    if not os.path.isfile(f):
        print('file: %s not exists, can not import to table %s' % (f, tbl))
        return
    
    print('importing to table: %s from file: %s' % (tbl, f))
    primaryKeys = db.query("""
        SELECT column_name from information_schema.columns where table_name = '%s' and table_schema  = '%s' and column_key = 'PRI'
        """ % (tbl, db.DB_NAME))
    primaryKeys = [k for k, in primaryKeys]
    col_names = []
    data_insert = []
    update_clause = ''
    data_update = []
    with open(f, 'rt', encoding='utf-8') as bkf:
        csv_reader = csv.reader(bkf)
        priKeyIndex = []
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                col_names = row
                priKeyIndex = [ [k, col_names.index(k)] for k in primaryKeys]
                line_count += 1
            else:
                clause = ''
                pri_vals = []
                for [k, i] in priKeyIndex:
                    clause += str(k) + '= \'' + str(row[i]) + '\' and '
                    update_clause += str(k) + '= %s and '
                    pri_vals.append(row[i])
                clause += ' 1=1 '
                update_clause += ' 1=1 '
                # not restore fakeids while importing user.
                if tbl == 'user' and 'fakeid_' in row[0]:
                    continue
                if db.exist_row(tbl, clauses = clause):
                    if existing_rows == 'update':
                        data_update.append(row + pri_vals)
                else:
                    data_insert.append(row)
    
    cursor = db.session_connection.cursor()
    db.execute('SET FOREIGN_KEY_CHECKS=0')
    if len(data_insert) > 0:
        _sql = """
        INSERT into %s (%s)
        VALUES (%s)
        """ % (tbl, ','.join(col_names), ','.join(['%s' for c in col_names]))
        for i in range(0, len(data_insert), 20000):
            cursor.executemany(_sql, data_insert[i: i+20000])
            db.session_connection.commit()

    if len(data_update) > 0:
        _sql = """
        UPDATE %s 
        SET %s 
        WHERE %s
        """ % (tbl, ','.join([f'{c} = %s' for c in col_names]), update_clause)
        for i in range(0, len(data_update), 20000):
            cursor.executemany(_sql, data_update[i: i+20000])
            db.session_connection.commit()
    db.execute('SET FOREIGN_KEY_CHECKS=1')


def import_all_tables():
    dbbkdir = get_db_backup_dir()
    db.init_connection(force=FORCE_LOAD)
    for p,d,fs in os.walk(dbbkdir):
        for f in fs:
            tbl = f[0: f.find('.bk.csv')]
            import_table(os.path.join(p, f), tbl, existing_rows='ignore')

def import_all_users():
    cur_dir = misc.get_pardir(os.path.abspath(__file__))
    vol_file = cur_dir + "/volunteer.csv"
    imp_file = cur_dir + "/impaired.csv"
    users = imptuser.importUser(vol_file, 0) + imptuser.importUser(imp_file, 1)
    db.init_connection(force=FORCE_LOAD)
    fake_id = 0
    for u in users:
        userinfo = {}
        userinfo["openid"] = "fakeid_" + str(fake_id)
        openid = userinfo["openid"]
        if db.exist_row("user", openid=openid):
            continue
        userinfo['role'] = u['role']
        userinfo['idcard'] = 'fake_idcard_' + str(fake_id) if u['idcard'] == '' else u['idcard']
        userinfo['idcard_verified'] = 0
        if userinfo['role'] == 1:
            userinfo['disabled_id'] = 'fake_disable_id_' + str(fake_id)
            userinfo['disabled_id_verified'] = 0
        userinfo["birth"] = datetime.now().strftime("%Y-%m-%d")
        userinfo['remark'] = u['remark']
        # userinfo["gender"] = u["gender"]
        # userinfo["address"] = u["linkaddress"]
        # userinfo['contact'] = u['linktel']
        userinfo["name"] = u["name"]
        userinfo["audit_status"] = u["audit_status"]
        userinfo["registration_date"] = u['reg_date']
        userinfo["phone"] = 'fake_phone_' + str(fake_id) if u['phone'] == '' else u['phone']
        if db.exist_row('user', phone=userinfo['phone']):
            userinfo['phone'] = 'fake_phone_' + str(fake_id)
            userinfo['remark'] += ' 重复电话: ' + u['phone']
        userinfo["phone_verified"] = 0
        userinfo["email"] = 'fake_email_' + str(fake_id)
        userinfo["email_verified"] = 0
        userinfo['activities_joined'] = u['act_joined']
        userinfo['activities_absence'] = u['act_absence']
        fake_id += 1
        try:
            if db.expr_insert("user", userinfo) != 1:
                print(openid, " user registration failed")
                continue
        except:
            print(openid, " user registration failed")
            continue

if __name__ == '__main__':
    cmd = initialize()
    if cmd.task is not None:
        if cmd.task == 'import_user':
            import_all_users()
    elif cmd.restore is not None and cmd.restore:
        # print('import_all_tables')
        import_all_tables()
    else:
        # print('export_all_tables')
        export_all_tables()
