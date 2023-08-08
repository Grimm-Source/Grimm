# Grimm-backend v2

> Technology makes tomorrow better.

## Introduction

This is a charitable projects, the purpose is to help visually impaired people, and this project is cloned from 

> git@github.com:Grimm-Source/Grimm.git

## Preparation

python 3.6+

mysql


## Getting started

```bash
$ sudo yum install python3
$ virtualenv -p /usr/bin/python3 venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
```


## Setup dev backend server

```bash
# execute in root path of this project
# (same path where this file is)

# please tag the Docker image as 'grimm:dev'
# this name will be used in start_dev_server.sh
$ docker build -f setup_dev/Dockerfile -t grimm:dev setup_dev/

# default publish port is 5000, can be changed in this file
$ setup_dev/start_dev_server.sh
```


## Changelog

Detailed changes for each release are documented in the [release notes](https://github.com/Grimm-Source/Grimm/releases).


## Online Demo

[Preview](http://104.243.21.35:5000/)


## License
[MIT](https://github.com/SincerelyUnique/grimm-backend/blob/main/license)

Copyright (c) 2017-present Grimm

## Features Usage

### - flask_migrate

```sql
create database grimmdb default character set utf8mb4 collate utf8mb4_unicode_ci;
```

```bash
$ set FLASK_APP=manage.py   # on centOS, use: export FLASK_APP=manage.py
$ flask db init  # Just execute it at the first time to generate migrations folder
$ flask db migrate -m "Initial migration."  # generate migration script(must check and edit)
$ flask db upgrade  # upgrade your db according to the scripts in migrations folder
```

reference doc:

[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)

[Alembic autogenerate documentation](http://alembic.zzzcomputing.com/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)

Attentions: the migration script needs to be reviewed and edited. and please do not use db.create_all()

If you are the first time to clone the project code, follow below steps to build your table structure:

(1)Create db with above sql

(2)Execute *set FLASK_APP=manage.py*  (on linux, the command is *export FLASK_APP=manage.py*)

(3)Finally, execute *flask db upgrade* to synchronize the table structure.

### - flask_restx

Use flask_restx to test your interface, just like postman, for example, we can write router like below and test.

```python
# For GET interface, usage like @main.route("/addAdmin")
@main.doc(params={"email": "input email", 'password': 'input password'})
def get(self):
    pass

# For POST interface, usage like @admin.route('/login', methods=['POST'])
@admin.doc(
    "Admin login test",
    responses={
        200: ("Logged in", AdminDto.login_success),
        400: "Validations failed.",
        403: "Incorrect password or incomplete credentials.",
        404: "Email does not match any account.",
        10086: "Email not verified."
    }
)
@admin.expect(AdminDto.login, validate=False)
def post(self):
    pass
```

There are many other methods that can be used in project, for more info, please visit to [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/) or [Github](https://github.com/python-restx/flask-restx)

### - flask_sqlalchemy

Below is the sqlalchemy usage demo script. 

```python
from datetime import datetime

import pandas as pd

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from grimm import engine
from grimm.models.activity import Activity, RegisteredActivity
from grimm.models.admin import Admin, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/grimmdb'
db = SQLAlchemy(app)


def raw_usage():
    """
    Execute raw sql expression directly use orm.
    The following operations do not depend on the web application context.
    Include: 1) sqlalchemy engine operations;
             2) pandas db operations;
    Advantages: 1) SQL-injection protect,
             ref: http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html
                  https://github.com/zzzeek/sqlalchemy
                  https://github.com/pallets/flask-sqlalchemy
                2) Easy to use and avoid writing sql everywhere in your code.
                3) Have some integration with other Flask extension like flask-migrate, etc.
    :return: None
    """
    # insert
    data = {
        'id': 1000,
        'registration_date': datetime.now(),
        'password': '123456',
        'name': 'test',
        'email': 'test@cisco.com',
        'email_verified': 0
    }
    df = pd.DataFrame([data])
    df.to_sql('admin', engine, if_exists='append', index=False)

    # select
    sql = "select * from admin"
    result1 = engine.execute(sql).fetchall()
    result2 = engine.execute(sql).fetchone()
    result3 = engine.execute(sql).first()
    print(result1)
    print(result2)
    print(result3)

    # select
    sql = "select * from admin where id=:admin_id"
    result = engine.execute(text(sql), admin_id=1000).first()
    print(result)

    # select
    sql = "select name, email from admin where id=:admin_id"
    df = pd.read_sql_query(text(sql), engine, params={'admin_id': 1000})
    print(df)

    # select
    sql = "select * from admin"
    df = pd.read_sql_query(sql, engine)
    print(df)

    # update
    sql = "update admin set name=:admin_name where ID=:admin_id "
    engine.execute(text(sql).execution_options(autocommit=True), admin_name='root', admin_id=1000)

    # delete
    sql = text("delete from admin where id=:admin_id")
    engine.execute(sql.execution_options(autocommit=True), admin_id=1000)


def orm_usage():
    """
    Execute with orm models.
    Attention, the following operations can not execute outside application.
    :return: None
    """
    # insert
    admin = Admin()
    admin.registration_date = datetime.now()
    admin.id = 1000
    admin.password = '123456'
    admin.name = 'test'
    admin.email = 'test@test.com'
    admin.email_verified = 1
    db.session.add(admin)
    db.session.commit()

    # select
    res = Admin.query.all()
    res = Admin.query.filter(Admin.id == 1000).first()
    res = db.session.query(Admin).all()
    res = db.session.query(Admin).filter(Admin.id == 1000).first()
    res = Admin.query.filter(Admin.id == 1000, Admin.name == 'test').first()
    res = db.session.query(User, RegisteredActivity).filter(User.openid == RegisteredActivity.user_openid).filter(User.openid == 'xxx').all()
    res = db.session.query(User.openid, RegisteredActivity.activity_id).filter(User.openid == RegisteredActivity.user_openid).filter(User.openid == 'xxx').all()

    # update
    db.session.query(Admin).filter(Admin.id == 1000).update({Admin.name: 'root'})
    db.session.commit()

    # delete
    db.session.delete(admin)
    db.session.commit()


@app.route('/test/raw')
def raw_test():
    raw_usage()
    return 'success'


@app.route('/test/orm')
def orm_test():
    orm_usage()
    return 'success'


if __name__ == '__main__':
    app.run(debug=True)
```


## Reference

### Binding SSL certificate with nginx

https://cloud.tencent.com/document/product/400/35244

### Tencent SMS doc

https://cloud.tencent.com/document/product/382/43196

