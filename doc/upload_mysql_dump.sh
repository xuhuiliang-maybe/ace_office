#!/bin/bash

year=$1
month=$2
start=$3
stop=$4

if [ $month -lt 10 ];then
month=0$month
fi

for start in `seq $stop`
do

if [ $start -lt 10 ];then
start=0$start
fi

path="${year}_${month}_$start"
if [ -d $path ];then
files=$(ls $path)
for filename in $files
do
/var/www/html/bpcs_uploader/bpcs_uploader.php upload $path/$filename bangtai_db_backup/$path/$filename
done
fi
done