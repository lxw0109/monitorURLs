#!/bin/bash
#File: clearLog.sh
#Author: lxw
#Time: 2015-03-07
#Usage: Run this script to clear the log data every day. 

#cd /home/lxw/Project/monitorURL
#cd /home/lxw/Project/monitorURL && > monitorLog; > criterion; > accessErrorURLs; echo -e "$(date) --- Clear Log OK\n" >> monitorLog|| echo -e "$(date) --- Clear Log ERROR\n" >> monitorLog; exit
cd /home/cnnic/monitorURL && > monitorLog; > accessErrorURLs; echo -e "$(date) --- Clear Log OK\n" >> monitorLog|| echo -e "$(date) --- Clear Log ERROR\n" >> monitorLog; exit

cd /home/cnnic/monitorURL && > urgentMonitorLog; > urgentAccessErrorURLs; echo -e "$(date) --- Clear Log OK\n" >> urgentMonitorLog|| echo -e "$(date) --- Clear Log ERROR\n" >> urgentMonitorLog; exit
