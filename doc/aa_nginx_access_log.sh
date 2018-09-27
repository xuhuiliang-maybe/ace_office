#!/bin/bash

source /etc/profile
logs_path="/usr/local/nginx/logs/"
DATE=`date +%Y-%m-%d`

mv ${logs_path}error.log ${logs_path}error_${DATE}.log
mv ${logs_path}host.access.log ${logs_path}host.access_${DATE}.log
mv ${logs_path}uwsgi.access.log ${logs_path}uwsgi.access_${DATE}.log

#killall -s USR1 nginx
service nginx restart


sourcelogpath="${logs_path}uwsgi.log"            #log源地址
touchfile="${logs_path}.touchforlogrotate"       #需要touch的文件
destlogpath="${logs_path}uwsgi_${DATE}.log"     #重命名后的文件
mv ${sourcelogpath} ${destlogpath}
touch ${touchfile}                             # 更新文件时间戳

find ${logs_path} -mtime +7 -name "*20[1-9][0-9]*.log" | xargs rm -f

exit 0
