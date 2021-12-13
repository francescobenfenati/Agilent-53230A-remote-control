#!/bin/bash
script_dir=
script_path=
file_path=""

/usr/bin/python3 $script_path
sleep 1
FILENAME=$file_path/*
echo Copied $FILENAME
sleep 1
/usr/bin/python3 $script_dir/csv-to-influxdb_UTC_RP.py --dbname pps_monitoring --create --user km3net --password pyrosoma --server 172.16.65.46:8087 --input $FILENAME --fieldcolumns delay(s) -tc time -tf "%Y-%m-%d %H:%M:%S"
sleep 1
rm -f $FILENAME
echo Removed csv
