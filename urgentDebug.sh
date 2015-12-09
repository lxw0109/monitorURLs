#!/bin/bash
#File: urgentDebug.sh
#Author: lxw
#Time: 2015-07-30
#Usage: Execute "python /home/cnnic/monitorURL/monitrUrgentURLs.py"
#HOW TO USE THIS FILE: add one command into file /etc/crontab

#kill the PROCESSes that are not wanted to be alive.
ps aux|grep "monitorUrgentURLs.py"|awk '{print $2}'|xargs kill

#run th monitor.
cd /home/cnnic/monitorURL

#Monitor:
python ./monitorUrgentURLs.py "debug" >> ./urgentMonitorLog
