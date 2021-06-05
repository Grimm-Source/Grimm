#!/bin/bash
basedir=$(dirname $0)
app_home=$(cd $basedir && pwd -L) || exit 1

[[ -d ${basedir}/logs ]] || {
    mkdir -p ${basedir}/logs
    echo "Create log directory, done."
}

# for logs backup
dir_name=$(date +%Y-%m-%d-%H-%M-%S)
log_backup_dir=../logs_backup/${dir_name}
mkdir -p ${log_backup_dir}
cp -ri ${basedir}/logs ${log_backup_dir}

rm -f ${basedir}/logs/*

echo "Start grimm gunicorn ..."

gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --backlog 64 \
         --worker-class gevent \
         --max-requests 500 \
         --timeout 900 \
         --access-logfile logs/access_log \
         --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s' \
         --error-log logs/error_log \
         --pid logs/grimm.pid \
         --capture-output \
          manage:app

echo " Has done."
