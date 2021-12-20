#!/bin/bash

script_dir="/home/tdcmon/Agilent-53230A-remote-control"

mkdir $script_dir/data
mkdir $script_dir/logs



/usr/bin/python3 $script_dir/pyvisa_agilent.py &

inotifywait --monitor -r -e close_write --format "%f" $script_dir/data | while read FILENAME
do
    echo Copied $FILENAME
    /usr/bin/python3 $script_dir/csv-to-influxdb_UTC_RP.py --dbname pps_monitoring --create --user km3net --password pyrosoma --server 172.16.65.46:8087 --input $script_dir/data/$FILENAME --fieldcolumns delay_s -tc time -tf "%Y-%m-%d %H:%M:%S"
    sleep 1
    rm -f $script_dir/data/$FILENAME
    echo Removed csv
done
