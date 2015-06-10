#!/bin/bash
#File: debug.sh
#Author: lxw
#Time: 2015-03-31
#Usage: DEUBUG-Execute "python /home/cnnic/Project/monitorURL/monitrURLs.py"

#kill the PROCESSes that are not wanted to be alive.
ps aux|grep "monitorURLs.py"|awk '{print $2}'|xargs kill

#run the monitor.
cd /home/cnnic/monitorURL

#use criterion &  criterion_new
touch accessErrorURLs
[ -d Intermedia ] || exit 0
[ -d Intermedia_new ] || exit 0
[ -d .Data ] || mkdir .Data
touch receive.conf

#Monitor:
#python ./monitorURLs.py "debug" >> ./monitorLog
python ./monitorURLs.py "debug" >> ./monitorLog
