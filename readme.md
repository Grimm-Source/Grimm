# Grimm-backend

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


## Changelog

Detailed changes for each release are documented in the [release notes](https://github.com/SincerelyUnique/grimm-backend/releases).


## Online Demo

[Preview](http://104.243.21.35:5000/)


## License
[MIT](https://github.com/SincerelyUnique/grimm-backend/blob/main/license)

Copyright (c) 2017-present Grimm

## Features Usage

### - flask_migrate

```bash
$ set FLASK_APP=manage.py
$ flask db init  # Just execute it at the first time
$ flask db migrate -m "Initial migration."
$ flask db upgrade
```

reference doc:

[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)

[Alembic autogenerate documentation](http://alembic.zzzcomputing.com/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)

Attentions: the migration script needs to be reviewed and edited.

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
@admin.expect(AdminDto.login, validate=True)
def post(self):
    pass
```

There are many other methods that can be used in project, for more info, please visit to [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/) or [Github](https://github.com/python-restx/flask-restx)
