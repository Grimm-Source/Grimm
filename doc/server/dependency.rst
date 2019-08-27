..
 File: dependency.rst
 Copyright: Grimm Project, Ren Pin NGO, all rights reserved.
 License: MIT
 -------------------------------------------------------------------------
 Authors:  Ming Li(adagio.ming@gmail.com)

 Description: list all necessary third-party python dependency packages that are required for server-end.

 To-Dos:
   1. make other supplements if needed.

 Issues:
   No issue so far.

 Revision History (Date, Editor, Description):
   1. 2019/08/15, Ming, create first revision.
..

==========
Before use
==========
Use pip to install all required python packages.
.. code-block:: bash
    $ pip3 install -r server/config/requirement.txt

=============
Package List
=============
- Flask (flask)
    - Click
    - itsdangerous
    - Werkzeug
    - Jinja2

- urllib3
- PyMySQL (pymysql)
- bcrypt
- email
- getpass
- logging
- inspect
- re
- json
