#
# File: sql.py
# Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
# License: MIT
# -------------------------------------------------------------------------
# Authors:  Ming Li(adagio.ming@gmail.com)
#
# Description: server backend code template.
#
# To-Dos:
#   1. make other supplements if needed.
#
# Issues:
#   No issue so far.
#
# Revision History (Date, Editor, Description):
#   1. 2019/08/12, Ming, create first revision.
#

import os
import json
import signal
import getpass

import logging
import pymysql
from pymysql import Error
from exceptions import SQLValueError


__all__ = ['expr_query', 'expr_update', 'expr_insert', 'expr_delete',
           'query', 'update', 'delete', 'insert',
           'session_connection', 'execute']


# db configs
DB_CONFIG_FILE = '../config/db.config'
DB_NAME = None

# db logger configs
DB_LOGGER_FILE = '../../log/db.log'
DB_LOGGER_NAME = 'db-transaction-logger'
db_logger = None

# SQL datatypes which need check quotes
SQL_QUOTED_TYPES = ('char', 'varchar', 'datetime', 'date',
                    'timestamp', 'text', 'binary')

# db session connection
session_connection = None


# get parent directory
def get_pardir(_dir):
    '''truncate path to get parent directory path'''
    if _dir[-1] is os.path.sep:
        _dir = _dir.rstrip(os.path.sep)
    d = _dir.split(os.path.sep)
    d.pop()
    pd = os.path.sep.join(d)

    return pd


# define and register signals handler
def close_connection(signalnum=None, frame=None):
    '''quit everything when termination signal received to kill the process'''
    if session_connection is not None and session_connection.open:
        session_connection.close()
    if db_logger is not None:
        db_logger.disabled = True
#        logging.shutdown()


signal.signal(signal.SIGINT, close_connection)
signal.signal(signal.SIGQUIT, close_connection)
# signal.signal(9, close_connection)
signal.signal(signal.SIGTERM, close_connection)


# initialize database connection
def init_connection(need_init_config=False):
    '''initialize database connection of server process'''
    global DB_NAME, session_connection, db_logger
    db_config_items = ['Host', 'Port', 'DB', 'Charset', 'User']

    def collect_db_userinfo(usr=None):
        if usr is not None:
            print('{:^10}: '.format('User'), usr)
        return getpass.getpass(prompt='%10s: ' % ('Password'))

    def collect_db_config():
        '''for user to input database configs, and dump configs as file'''
        print('\nConfigure MySQL connection >>>\n')
        config = {}
        for item in db_config_items:
            _input = input('{:^10}: '.format(item)).strip()
            _input = int(_input) if item == 'Port' else _input
            config[item] = _input

        config_dir = get_pardir(DB_CONFIG_FILE)
        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)
        with open(DB_CONFIG_FILE, "w") as fp:
            json.dump(obj=config, fp=fp, ensure_ascii=False, indent=4)

        config['Password'] = collect_db_userinfo()

        print('\nDone!')
        return config

    # initialize database logger
    if db_logger is None:
        db_logger = logging.getLogger(DB_LOGGER_NAME)
        # set logging level as default DEBUG level.
        db_logger.setLevel(logging.DEBUG)
        log_dir = get_pardir(DB_LOGGER_FILE)
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)
        # create logging file handler.
        fh = logging.FileHandler(DB_LOGGER_FILE, mode='a', encoding='utf8')
        # format
        fmt = '%(asctime)s %(name)s %(levelname)1s %(message)s'
        fmter = logging.Formatter(fmt)
        fh.setFormatter(fmter)
        # add file handler
        db_logger.addHandler(fh)

    # create and initialize db connection
    if session_connection is None:
        if need_init_config is True:
            db_config = collect_db_config()
        else:
            if os.path.isfile(DB_CONFIG_FILE):
                try:
                    with open(DB_CONFIG_FILE, 'r') as fp:
                        db_config = json.load(fp=fp, encoding='utf8')
                    print('\nMySQL Login >>>\n')
                    db_config['Password'] = collect_db_userinfo(usr=db_config['User'])
                except Exception as e:
                    db_logger.error('load json config failed: (%d, %s)', e.args[0], e.args[1])
                    db_config = collect_db_config()

                for k, v in db_config.items():
                    if k == 'Password':
                        continue
                    if v is None or k not in db_config_items:
                        print('\nCorrupt config file, need input config >>>')
                        db_config = collect_db_config()
                        break
            else:
                db_config = collect_db_config()
        DB_NAME = db_config['DB']

        # initialize db connection
        retry = 3
        while retry > 0:
            try:
                session_connection = pymysql.connect(host=db_config['Host'],
                                                     port=db_config['Port'],
                                                     user=db_config['User'],
                                                     password=db_config['Password'],
                                                     database=db_config['DB'],
                                                     charset=db_config['Charset'],
                                                     read_timeout=10,
                                                     write_timeout=10)
            except Exception as e:
                db_logger.error('%dth connect DB failed: %s', 3-retry, e.args[0])
                if e.args[0] == 'cryptography is required for sha256_password or caching_sha2_password':
                    print('\nProbably, a wrong password caused invalid connection!\n')
                    db_config['Password'] = collect_db_userinfo()
                connection_error = e
                retry -= 1
                continue

            if session_connection is not None:
                break
        if retry == 0:
            os.remove(DB_CONFIG_FILE)
            db_logger.error('connect DB failed after %d times trying', 3)
            raise connection_error

        # logging
        if session_connection is not None:
            print('\nConnected to DB: %s!' % (DB_NAME))
            db_logger.info('Database Connected, Host: %s, Port: %d, User: %s, DB_Name: %s',
                           db_config['Host'], db_config['Port'], db_config['User'], DB_NAME)

    elif session_connection.open is False:
        session_connection.ping(reconnect=True)
        if session_connection.open is True:
            print('Session Reconnected')
            db_logger.info('Database Reconnected successfully')
        else:
            print('Session Reconnected failed')
            db_logger.info('Database Reconnected failed')


#
# MySQL execute API:
#
def execute(_execute):
    '''standard SQL API for executing SQL script line'''
    # check SQL connection status
    if session_connection is None or session_connection.open is False:
        init_connection()

    if isinstance(_execute, bytes):
        _execute.decode('utf8')
    if not isinstance(_execute, str):
        raise SQLValueError('execution', 'invalid executed script')

    cursor = session_connection.cursor()
    try:
        cursor.execute(_execute)
        cursor.close()
        session_connection.commit()
    except Error as e:
        raise e

    return cursor


# data record formatter
def formatter(record):
    '''format records fetched from database'''
    if isinstance(record, bytes):
        record = record.strip(b'\0').decode('utf8')
    if isinstance(record, str):
        record = record.strip()
    return record


# get all table column names
def query_tbl_columns(tbl):
    '''fetch all column names into a tuple of given table'''
    if session_connection is None or session_connection.open is False:
        init_connection()

    if isinstance(tbl, bytes):
        tbl = tbl.decode('utf8')
    if not isinstance(tbl, (str, tuple, list)):
        e = SQLValueError('query column names', 'invalid table name')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e
    if isinstance(tbl, (tuple, list)):
        if len(tbl) > 1:
            db_logger.warning('query multiple table columns: %s', ','.join(tbl))
        table = str(tbl[0]) if not isinstance(tbl[0], str) else tbl[0].strip()
    else:
        table = tbl.strip('\'" ')
    if not table:
        e = SQLValueError('query column names', 'null table')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e

    _query = f"SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` \
        WHERE `TABLE_SCHEMA` = '{DB_NAME}' AND `TABLE_NAME` = '{table}'"
    db_logger.info('SQL table columns querying: %s', _query)
    cursor = session_connection.cursor()
    try:
        cursor.execute(_query)
        cursor.close()
        session_connection.commit()
    except Error as e:
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.args[0], e.args[1])
        raise e

    records = cursor.fetchall()
    query_cols = [str(row[0]) if not isinstance(row[0], str) else row[0] for row in records]

    return tuple(query_cols)


# get table columns data type
def query_tbl_columns_datatype(tbl, cols='*'):
    if session_connection is None or session_connection.open is False:
        init_connection()

    if isinstance(tbl, bytes):
        tbl = tbl.decode('utf8')
    if not isinstance(tbl, (str, tuple, list)):
        e = SQLValueError('query columns datatype', 'invalid table name')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e
    if isinstance(tbl, (tuple, list)):
        if len(tbl) > 1:
            db_logger.warning('query multiple tables column datatype: %s', ','.join(tbl))
        table = str(tbl[0]) if not isinstance(tbl[0], str) else tbl[0].strip()
    else:
        table = tbl.strip('\'" ')
    if not table:
        e = SQLValueError('query columns datatype', 'null table')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e

    if isinstance(cols, bytes):
        cols = cols.decode('utf8')
    if not isinstance(cols, (str, tuple, list)):
        e = SQLValueError('query columns datatype', 'invalid query column names')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e
    if cols == '*':
        cols = query_tbl_columns(tbl)
        columns = cols
        opcode = 'IN'
    elif isinstance(cols, str):
        cols = cols.strip()
        columns = cols if cols[0] in '\'"' else f"'{cols}'"
        opcode = '='
    else:
        columns = tuple([c.strip('\'"') if isinstance(c, str) else str(c) for c in cols])
        opcode = 'IN'

    _query = f"SELECT `COLUMN_NAME`,`DATA_TYPE` FROM `INFORMATION_SCHEMA`.`COLUMNS` \
                WHERE `TABLE_NAME` = '{table}' AND `COLUMN_NAME` {opcode} {columns}"
    db_logger.info('SQL columns datatype querying: %s', _query)
    cursor = session_connection.cursor()
    try:
        cursor.execute(_query)
        cursor.close()
        session_connection.commit()
    except Error as e:
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.args[0], e.args[1])
        raise e

    records = cursor.fetchall()
    db_cols = [str(row[0]) if not isinstance(row[0], str) else row[0] for row in records]
    db_typeinfo = [str(row[1]) if not isinstance(row[1], str) else row[1] for row in records]

    return dict(zip(db_cols, db_typeinfo))


# connect exprs where clause exprs list
def join_exprs_clause(clauses):
    if isinstance(clauses, bytes):
        clauses.decode('utf8')
    if not isinstance(clauses, (str, tuple, list)):
        e = SQLValueError('expression query', 'invalid where clause')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e
    if isinstance(clauses, (tuple, list)):
        clauses = ' '.join(clauses)
    return clauses


# parse **kwargs where clauses
def parse_kwargs_clause(tbls, cols='*', **kwargs):
    expr_operator = '='
    expr_connector = 'and'
    where_clause = ''

    if isinstance(tbls, bytes):
        tbls = tbls.decode('utf8')
    if isinstance(tbls, str):
        table_count = 1
    elif isinstance(tbls, (tuple, list)):
        table_count = len(tbls)
    else:
        table_count = 0
    if table_count > 0:
        if table_count == 1:
            typeinfo = query_tbl_columns_datatype(tbls, cols)
        for k, v in kwargs.items():
            if isinstance(v, bytes):
                v = v.decode('utf8')
            # add quotes for words
            if isinstance(v, str) and v.strip()[0] not in '\'"':
                if table_count == 1 and typeinfo[k] not in SQL_QUOTED_TYPES:
                    v = v.strip()
                else:
                    v = f"'{v.strip()}'"

            expr = f'{k} {expr_operator} {v}'
            where_clause = f'{where_clause} {expr_connector} {expr}' if where_clause else expr

    return where_clause


#
# MySQL expr_query API: query with expressions instead of SQL line.
#     1. tbls: table names, query in what tables.
#
#     2. cols: column names, query what columns, '*' by default.
#
#     3. clauses: string or tuple which provides whole `where clause` info.
#       1) string.
#           a line, which should contain all needed `where clause` info to
#           specify explicit conditions, keyword `where` must be excluded.
#           eg: clauses = "age = 30 and passwd = 'password'"
#           means: "where age = 30 and passwd = 'password'"
#       2) tuple/list.
#           an ordered expression string sequence which will form the whole
#           'where clause' info, all items will be linked from first to end,
#           so the order is very important, keyword `where` is excluded.
#           eg1: ("age = 30 or gender = 'male'", )
#           means: "where age = 30 or gender = 'male'"
#           eg2: ("age = 30", "or", "gender = 'male'")
#           means same with the above one.
#           DON'T OMIT THE EXPRESSION CONNECTORS.
#           DON'T FORGET THE QUOTES FOR VALUES IN MYSQL EXPRS!!!
#        Note:
#           If this arguement is provided, **kwargs will be omitted.
#
#     4. **kwargs: specify `where clause` info, expression operator is '=',
#        expression connector is 'and' only.
#           eg: expr_query(..., age=40, gender='male')
#           which means: "where age=40 and gender='male'"
#        Note:
#           This is for simple cases, for complicated cases, use arguement
#           `clauses` as above instead.
#
def expr_query(tbls, cols='*', clauses=None, **kwargs):
    '''standard SQL API for database query operation using expressions'''
    # check SQL connection status
    if session_connection is None or session_connection.open is False:
        init_connection()

    # default expr connector is 'and', expr operator is '=' for **kwargs
    where_clause = ''

    # concatenate target tables
    if isinstance(tbls, bytes):
        tbls = tbls.decode('utf8')
    if not isinstance(tbls, (str, tuple, list)):
        e = SQLValueError('expression query', 'invalid table names')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e
    if isinstance(tbls, (tuple, list)):
        tables = ','.join([str(tbl) if not isinstance(tbl, str) else tbl.strip() for tbl in tbls])
        table_count = len(tbls)
    else:
        tables = tbls.strip('\'" ')
        table_count = 1
    if not tables:
        e = SQLValueError('expression query', 'null table')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e

    # special case, no querying * from multiple tables
    if table_count > 1 and cols == '*':
        e = SQLValueError('expression query', 'select * from multiple tables')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e

    # concatenate query columns
    if isinstance(cols, bytes):
        cols = cols.decode('utf8')
    if not isinstance(cols, (str, tuple, list)):
        e = SQLValueError('expression query', 'invalid column names')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e
    if cols == '*':
        cols = query_tbl_columns(tbls)
        columns = ','.join(cols)
    elif isinstance(cols, str):
        columns = cols.strip('\'" ')
    else:
        cols = [str(c) if not isinstance(c, str) else c.strip('\'" ') for c in cols]
        columns = ','.join(cols)

    # parse clause, including kwargs clause & dictionary clause
    # function arguement clause
    if clauses is not None:
        where_clause = join_exprs_clause(clauses)
        kwargs = None

    # **kwargs arguement clause
    if kwargs is not None:
        where_clause = parse_kwargs_clause(tbls=tbls, cols=cols, **kwargs)

    # do query
    if where_clause:
        _query = f"select {columns} from {tables} where {where_clause}"
    else:
        _query = f"select {columns} from {tables}"
    print('expression query: ', _query)
    db_logger.info('SQL expression querying: %s', _query)
    cursor = session_connection.cursor()
    try:
        cursor.execute(_query)
        cursor.close()
        session_connection.commit()
    except Error as e:
        db_logger.error('SQL expression query execution error: (%d, %s)', e.args[0], e.args[1])
        raise e

    # orgnize fetched records
    records = cursor.fetchall()
    row_count = cursor.rowcount
    if row_count == 0:
        db_logger.warning('Empty query record, SQL: %s', _query)
        return None
    elif row_count == 1:
        new_records = [formatter(x) for x in records[0]]
        data = dict(zip((columns,), new_records)) if isinstance(cols, str) else dict(zip(cols, new_records))
        return (data, )
    else:
        new_records = [[formatter(x) for x in row] for row in records]
        data = [dict(zip((columns,), record)) if isinstance(cols, str) else dict(zip(cols, record)) for record in new_records]
        return tuple(data)


#
# MySQL expr_update API:
#     1. tbl: table name, update what table, one table only.
#     2. pairs: dict, contains what column is updated with what value.
#       eg: {'age' : 30} means 'set age = 30'
#     3. clauses: see `MySQL expr_query API`.
#     4. **kwargs: see `MySQL expr_query API`.
#
#     Notes:
#       Also see `MySQL expr_query API`
#
def expr_update(tbl, pairs, clauses=None, **kwargs):
    '''standard SQL API for database update operation using expressions'''
    # check SQL connection status
    if session_connection is None or session_connection.open is False:
        init_connection()

    where_clause = ''
    update_exprs = []

    if isinstance(tbl, bytes):
        tbl = tbl.decode('utf8')
    if not isinstance(tbl, (str, tuple, list)):
        e = SQLValueError('expression update', 'invalid table name')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e
    if isinstance(tbl, (tuple, list)):
        if len(tbl) > 1:
            db_logger.warning('expression update multiple tables: %s', ','.join(tbl))
        table = str(tbl[0]) if not isinstance(tbl[0], str) else tbl[0].strip()
    else:
        table = tbl.strip('\'" ')
    if not table:
        e = SQLValueError('expression update', 'null table')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e

    if not isinstance(pairs, dict) or len(pairs) == 0:
        e = SQLValueError('expression update', 'invalid new pairs')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e

    # parse clause, including kwargs clause & dictionary clause
    # function arguement clause
    if clauses is None and not kwargs:
        e = SQLValueError('expression update', 'need to specify where clause')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e
    if clauses is not None:
        where_clause = join_exprs_clause(clauses)
        kwargs = None

    # **kwargs arguement clause
    typeinfo = query_tbl_columns_datatype(table, '*')
    if kwargs is not None:
        where_clause = parse_kwargs_clause(tbls=tbl, **kwargs)

    # parse update pairs
    for k, v in pairs.items():
        k = k.strip('\'" ') if isinstance(k, str) else k
        if isinstance(v, bytes):
            v = v.decode('utf8')
        # add quotes for words
        if isinstance(v, str) and v.strip()[0] not in '\'"':
            print('value %s not quoted' %(v))
            if typeinfo[k] in SQL_QUOTED_TYPES:
                v = f"'{v.strip()}'"
            else:
                v = v.strip()

        update_exprs += [f'{k}={v}']
    print('update_exprs:', update_exprs)
    update_pairs = ','.join(update_exprs)

    # do update
    if where_clause:
        _update = f'update {table} set {update_pairs} where {where_clause}'
    else:
        _update = f'update {table} set {update_pairs}'
    print('expression update: ', _update)
    db_logger.info('SQL expression updating: %s', _update)
    cursor = session_connection.cursor()
    try:
        result = cursor.execute(_update)
        cursor.close()
        session_connection.commit()
    except Error as e:
        db_logger.error('SQL expression update execution error: (%d, %s)', e.args[0], e.args[1])
        raise e

    return result


#
# MySQL expr_insert API:
#     1. tbl: table name, insert to what table, one table only.
#     2. vals: dict/list/tuple, contains values to be inserted.
#       1) dict
#           eg: {'age':20, 'status':0}
#           means: insert into table(age, status) values(20, 0)
#       2) list/tuple
#           eg: (ming, 25, boy)
#           means: insert into table values (ming, 25, boy)
#       The second form requires values order corresponds to
#       the columns order in database table.
#     3. **kwargs: specify column-value pairs to be inserted.
#        Works the same way with arguement `vals`'s dict form.
#
#     Note:
#       If `vals` arguement is provided, **kwargs will be omitted.
#
def expr_insert(tbl, vals=None, **kwargs):
    '''standard SQL API for database insert operation using expressions'''
    # check SQL connection status
    if session_connection is None or session_connection.open is False:
        init_connection()

    insert_values = insert_columns = ''

    if isinstance(tbl, bytes):
        tbl = tbl.decode('utf8')
    if not isinstance(tbl, (str, tuple, list)):
        e = SQLValueError('expression insert', 'invalid table name')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e
    if isinstance(tbl, (tuple, list)):
        if len(tbl) > 1:
            db_logger.warning('expression insert multiple tables: %s', ','.join(tbl))
        table = str(tbl[0]) if not isinstance(tbl[0], str) else tbl[0].strip()
    else:
        table = tbl.strip('\'" ')
    if not table:
        e = SQLValueError('expression insert', 'null table')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e

    if vals is not None:
        if not isinstance(vals, (dict, list, tuple)) or len(vals) == 0:
            e = SQLValueError('expression insert', 'invalid values')
            db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
            raise e

        if isinstance(vals, dict):
            columns = [k.strip('\'"') for k in vals.keys()]
            insert_columns = f"({','.join(columns)})"
            values = [v.decode('utf8') if isinstance(v, bytes) else v for v in vals.values()]
        else:
            values = [v.decode('utf8') if isinstance(v, bytes) else v for v in vals]
        insert_values = f'{tuple(values)}'
        kwargs = None

    if kwargs is not None:
        columns = [k.strip('\'"') for k in kwargs.keys()]
        insert_columns = f"({','.join(columns)})"
        values = [v.decode('utf8') if isinstance(v, bytes) else v for v in kwargs.values()]
        insert_values = f'{tuple(values)}'

    # do insert
    if insert_columns:
        _insert = f'insert into {table} {insert_columns} values {insert_values}'
    else:
        _insert = f'insert into {table} values {insert_values}'
    print('expression insert: ', _insert)
    db_logger.info('SQL expression inserting: %s', _insert)
    cursor = session_connection.cursor()
    try:
        result = cursor.execute(_insert)
        cursor.close()
        session_connection.commit()
    except Error as e:
        db_logger.error('SQL expression insert execution error: (%d, %s)', e.args[0], e.args[1])
        raise e

    return result


#
# MySQL expr_delete API:
#     1. tbl: table name, delete rows from what table, one table only.
#     2. clauses: string or tuple which provides whole `where clause` info.
#       1) string.
#           a line, which should contain all needed `where clause` info to
#           specify explicit conditions, keyword `where` must be excluded.
#           eg: clauses = "age = 30 and passwd = 'password'"
#           means: "where age = 30 and passwd = 'password'"
#       2) tuple/list.
#           an ordered expression string sequence which will form the whole
#           'where clause' info, all items will be linked from first to end,
#           so the order is very important, keyword `where` is excluded.
#           eg1: ("age = 30 or gender = 'male'", )
#           means: "where age = 30 or gender = 'male'"
#           eg2: ("age = 30", "or", "gender = 'male'")
#           means same with the above one.
#           DON'T OMIT THE EXPRESSION CONNECTORS.
#           DON'T FORGET THE QUOTES FOR VALUES IN MYSQL EXPRS!!!
#        Note:
#           If this arguement is provided, **kwargs will be omitted.
#
#     3. **kwargs: specify `where clause` info, expression operator is '=',
#        expression connector is 'and' only.
#     Note:
#       If `clauses` arguement is provided, **kwargs will be omitted.
#
def expr_delete(tbl, clauses=None, **kwargs):
    '''standard SQL API for database delete operation using expressions'''
    # check SQL connection status
    if session_connection is None or session_connection.open is False:
        init_connection()

    where_clause = ''

    if isinstance(tbl, bytes):
        tbl = tbl.decode('utf8')
    if not isinstance(tbl, (str, tuple, list)):
        e = SQLValueError('expression delete', 'invalid table name')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e
    if isinstance(tbl, (tuple, list)):
        if len(tbl) > 1:
            db_logger.warning('expression delete multiple tables: %s', ','.join(tbl))
        table = str(tbl[0]) if not isinstance(tbl[0], str) else tbl[0].strip()
    else:
        table = tbl.strip('\'" ')
    if not table:
        e = SQLValueError('expression delete', 'null table')
        db_logger.error('%s: (%d, %s)', e.__class__.__name__, e.ecode, e.emsg)
        raise e

    # parse clause, including kwargs clause & dictionary clause
    # function arguement clause
    if clauses is not None:
        where_clause = join_exprs_clause(clauses)
        kwargs = None

    # **kwargs arguement clause
    if kwargs is not None:
        where_clause = parse_kwargs_clause(tbls=tbl, **kwargs)

    if where_clause:
        _delete = f'delete from {table} where {where_clause}'
    else:
        _delete = f'delete from {table}'
    print('expression delete: ', _delete)
    db_logger.info('SQL deleting: %s', _delete)
    cursor = session_connection.cursor()
    try:
        result = cursor.execute(_delete)
        cursor.close()
        session_connection.commit()
    except Error as e:
        db_logger.error('SQL delete execution error: (%d, %s)', e.args[0], e.args[1])
        raise e

    return result


#
# MySQL query API:
#     1. query: SQL query script.
#
def query(_query):
    '''standard SQL API for database query operation using SQL script'''
    print('script query: ', _query)
    db_logger.info('SQL script querying: %s', _query)

    try:
        cursor = execute(_query)
    except Exception as e:
        db_logger.error('SQL script query execution error: (%d, %s)', e.args[0], e.args[1])
        raise e

    # orgnize fetched records
    records = cursor.fetchall()
    row_count = cursor.rowcount
    if row_count == 0:
        db_logger.warning('Empty fetched record, query: %s', _query)
        result = records
    elif row_count == 1:
        result = tuple([formatter(x) for x in records[0]])
    else:
        result = tuple([tuple([formatter(x) for x in row]) for row in records])

    return result


#
# MySQL update API:
#     1. update: SQL update script.
#
def update(_update):
    '''standard SQL API for database update operation using SQL script'''
    print('script update: ', _update)
    db_logger.info('SQL script updating: %s', _update)

    try:
        cursor = execute(_update)
    except Exception as e:
        db_logger.error('SQL script update execution error: (%d, %s)', e.args[0], e.args[1])
        raise e

    return cursor.rowcount


#
# MySQL insert API:
#     1. insert: SQL insert script.
#
def insert(_insert):
    '''standard SQL API for database insert operation using SQL script'''
    print('script insert: ', _insert)
    db_logger.info('SQL script inserting: %s', _insert)

    try:
        cursor = execute(_insert)
    except Exception as e:
        db_logger.error('SQL script insert execution error: (%d, %s)', e.args[0], e.args[1])
        raise e

    return cursor.rowcount


#
# MySQL delete API:
#     1. delete: SQL delete script.
#
def delete(_delete):
    '''standard SQL API for database delete operation using SQL script'''
    print('script delete: ', _delete)
    db_logger.info('SQL script deleting: %s', _delete)

    try:
        cursor = execute(_delete)
    except Exception as e:
        db_logger.error('SQL script delete execution error: (%d, %s)', e.args[0], e.args[1])
        raise e

    return cursor.rowcount
