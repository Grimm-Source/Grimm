#!/bin/bash

/etc/init.d/mariadb start;

mysql -uroot -e 'CREATE DATABASE `grimmdb_dev` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci';

export FLASK_ENV=dev
python setup_dev/initdb.py

python manage.py runserver -h 0.0.0.0 -p 5000
