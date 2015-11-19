#!/bin/bash
#File: run.sh
#Author: lxw
#Time: 2015-02-07
#Usage: Execute "python /home/cnnic/Project/monitorURL/monitrURLs.py"
#HOW TO USE THIS FILE: add one command into file /etc/crontab

#kill the PROCESSes that are not wanted to be alive.
ps aux|grep "monitorURLs.py"|awk '{print $2}'|xargs kill

#run th monitor.
cd /home/cnnic/monitorURL

#Preparation:
#update/create the following File/Dir.
touch criterion_new
cp criterion_new criterion
touch accessErrorURLs
[ -d Intermedia ] || mkdir Intermedia
[ -d Intermedia_new ] || mkdir Intermedia_new
[ -d .Data ] || mkdir .Data
touch receive.conf

cd ./Intermedia/
rm ./*
cd .. 
mv ./Intermedia_new/* ./Intermedia/

#Monitor:
python ./monitorURLs.py >> ./monitorLog
