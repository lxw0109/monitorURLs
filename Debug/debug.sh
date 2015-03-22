#!/bin/bash
#File: debug.sh
#Author: lxw
#Time: 2015-03-22
#Usage: DEUBUG-Execute "python /home/lxw/Project/monitorURL/monitrURLs.py"

#kill the PROCESSes that are not wanted to be alive.
ps aux|grep "monitorURLs.py"|awk '{print $2}'|xargs kill

#run th monitor.
cd /home/lxw/monitorURL

#Preparation:
#update/create the following File/Dir.
touch criterion
touch accessErrorURLs
[ -d Intermedia ] || mkdir Intermedia
[ -d Intermedia_new ] || mkdir Intermedia_new

cp ./Debug/criterion_debug criterion
rm ./Intermedia/*
cp ./Debug/new_debug/* ./Intermedia/

#Monitor:
python ./monitorURLs.py >> ./monitorLog
