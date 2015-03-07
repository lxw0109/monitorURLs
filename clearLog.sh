#!/bin/bash
#File: clearLog.sh
#Author: lxw
#Time: 2015-03-07
#Usage: Run this script to clear the log data every day. 

#cd /home/lxw/Project/monitorURL
cd /home/liuxiaowei/Documents/monitorURLs && > monitorLog; > criterion; > accessErrorURLs; echo -e "$(date) --- Clear Log OK\n" >> monitorLog|| echo -e "$(date) --- Clear Log ERROR\n" >> monitorLog; exit
