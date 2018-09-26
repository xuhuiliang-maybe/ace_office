#!/bin/bash

source /etc/profile
#日期格式
file=`date +%Y_%m_%d_%H_%M_%S`
file_path=`date +%Y_%m_%d`
#文件目录
filedir=/root/mysqlautobackup/$file_path/

if [ ! -d "$filedir" ]; then
  mkdir $filedir
fi

#记录开始时间
start=`date +%Y-%m-%d_%H:%M:%S`
echo -e "开始执行备份：$start" >> $filedir/auto_backup.log

#数据库信息
name="root"
pawd="RootPass123!!!"
#执行备份
/usr/bin/mysqldump -u$name -p$pawd --databases aces > $filedir/mysql$file.sql

if [ $? -eq 0 ]
then

#记录结束时间
end=`date +%Y-%m-%d_%H:%M:%S`
echo -e "结束执行备份：$end mysql$file.sql\n" >> $filedir/auto_backup.log

#备份到百度云盘
#/usr/local/bin/bypy mkdir bangtai_db_backup/$file_path
#/usr/local/bin/bypy upload $filedir/mysql$file.sql bangtai_db_backup/$file_path -v
#/usr/local/bin/bypy upload $filedir/auto_backup.log bangtai_db_backup/$file_path -v

# bpcs_uploader 备份到百度云盘
/var/www/html/bpcs_uploader/bpcs_uploader.php upload $filedir/mysql$file.sql bangtai_db_backup/$file_path/mysql$file.sql
/var/www/html/bpcs_uploader/bpcs_uploader.php upload $filedir/auto_backup.log bangtai_db_backup/$file_path/auto_backup.log

fi

