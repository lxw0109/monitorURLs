#!/bin/bash
#File: run.sh
#Author: lxw
#Time: 2015-02-07
#Usage: Execute "python /home/lxw/Project/monitorURL/monitrURLs.py"
#HOW TO USE THIS FILE: add one command into file /etc/crontab
#


#kill the PROCESSes that are not wanted to be alive.
ps aux|grep "monitorURLs.py"|awk '{print $2}'|xargs kill

#run th monitor.
cd /home/lxw/Project/monitorURL

#Preparation:
#update/create the following File/Dir.
touch criterion
touch accessErrorURLs
[ -d Intermedia ] || mkdir Intermedia

#Monitor:
python ./monitorURLs.py >> ./monitorLog
