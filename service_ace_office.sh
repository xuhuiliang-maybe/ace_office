#!/bin/bash

logs_path="/usr/local/nginx/logs/"
module_path="/var/www/html/ace_office/ace_office/"
uwsgi_path="/usr/local/bin/uwsgi"
uwsgi_name="ace_office_uwsgi"

start()
{
        echo -n $"Starting ace_office_uwsgi: "
        ${uwsgi_path} -x ${module_path}django.xml
        echo "[OK]"

        service nginx start
}
stop()
{
        echo -n $"Shutting down ace_office_uwsgi: "
        ps axuf|grep ${uwsgi_name} | grep -v grep | cut -c 9-14|xargs kill -s 9
        echo "[OK]"

        service nginx stop
}
case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  restart)
        stop
        sleep 3
        start
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart}"
        exit 1
esac
exit 0
