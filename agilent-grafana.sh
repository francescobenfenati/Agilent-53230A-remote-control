#!/bin/bash

script_dir=

mkdir $script_dir/data
mkdir $script_dir/logs



/usr/bin/python3 $script_dir/pyvisa_agilent.py
sleep 1
FILENAME=$script_dir/data/*
echo Copied $FILENAME
sleep 1
/usr/bin/python3 $script_dir/csv-to-influxdb_UTC_RP.py --dbname pps_monitoring --create --user km3net --password pyrosoma --server 172.16.65.46:8087 --input $FILENAME --fieldcolumns delay(s) -tc time -tf "%Y-%m-%d %H:%M:%S"
sleep 1
rm -f $FILENAME
echo Removed csv
