#!/bin/bash
#File: debug.sh
#Author: lxw
#Time: 2015-03-31
#Usage: DEUBUG-Execute "python /home/lxw/Project/monitorURL/monitrURLs.py"

#kill the PROCESSes that are not wanted to be alive.
ps aux|grep "monitorURLs.py"|awk '{print $2}'|xargs kill

#run the monitor.
cd /home/lxw/monitorURL

#use criterion &  criterion_new
touch accessErrorURLs
[ -d Intermedia ] || exit 0
[ -d Intermedia_new ] || exit 0

#Monitor:
python ./monitorURLs.py "debug" >> ./monitorLog
