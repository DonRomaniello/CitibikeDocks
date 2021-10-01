#!/bin/sh

tar=/usr/bin/tar
xz=/usr/bin/xz


cd /home/ec2-user/citibike/scrapes

sleep 20

tar --remove-files -cJf /home/ec2-user/citibike/tars/pack$(date +%Y-%m-%d_%H-%M-%S).tar.xz *


