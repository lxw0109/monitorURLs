#!/bin/bash
#File: killThreads.sh
#Author: lxw
#Time: 2015-03-22
#Usage: There are some specific urls(e.g. http://www.denic.de/en/homepage.html. so far, only this one) that cost a rather long time to access, ignore these urls.

ps aux | grep "bash urgentRun.sh" | grep -v "grep"| awk '{print $2}' | xargs kill
ps aux | grep "python ./monitorUrgentURLs" | grep -v "grep"| awk '{print $2}' | xargs kill
