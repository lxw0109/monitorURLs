#!/bin/bash
#File: urgentRun.sh
#Author: lxw
#Time: 2015-07-30
#Usage: Execute "python /home/cnnic/Project/monitorURL/monitrURLs.py"
#HOW TO USE THIS FILE: add one command into file /etc/crontab

#kill the PROCESSes that are not wanted to be alive.
ps aux|grep "monitorUrgentURLs.py"|awk '{print $2}'|xargs kill

#run th monitor.
cd /home/cnnic/monitorURL

#Preparation:
#update/create the following File/Dir.
touch urgentCriterion_new
cp urgentCriterion_new urgentCriterion
touch urgentAccessErrorURLs
[ -d urgentIntermedia ] || mkdir urgentIntermedia
[ -d urgentIntermedia_new ] || mkdir urgentIntermedia_new
[ -d .Data ] || mkdir .Data
touch urgentReceive.conf

#cd ./urgentIntermedia/
#now=$(date)
#mkdir "$now"    #" is essential.
#mv http* "$now"    #" is essential.
#cd .. 

mv ./urgentIntermedia_new/* ./urgentIntermedia/

#Monitor:
python ./monitorUrgentURLs.py >> ./urgentMonitorLog
