#!/bin/bash
#File: run.sh
#Author: lxw
#Time: 2015-02-07
#Usage: Execute "python /home/lxw/Project/monitorURL/monitrURLs.py"

#kill the PROCESSes that are not wanted to be alive.
ps aux|grep "monitorURLs.py"|awk '{print $2}'|xargs kill 

#run th monitor.
cd /home/lxw/Project/monitorURL
python ./monitorURLs.py

