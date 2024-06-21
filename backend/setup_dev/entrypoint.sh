#!/bin/bash

/etc/init.d/mariadb start;

DATABASE=grimmdb_dev
if mysql -uroot -e "use ${DATABASE};" 2>/dev/null; then
    echo "Database ${DATABASE} exists, skip init"
else
    mysql -uroot -e 'CREATE DATABASE `'${DATABASE}'` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci';

    export FLASK_ENV=dev
    python setup_dev/initdb.py
fi

python manage.py runserver -h 0.0.0.0 -p 5000
