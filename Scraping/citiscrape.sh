#!/bin/sh

wget=/usr/bin/wget

cd /home/ec2-user/citibike/scrapes/

wget -O station_status_on_$(date +%Y-%m-%d_%H:%M:%S).json https://gbfs.citibikenyc.com/gbfs/en/station_status.json
