####Open for Suggestions & Feedback:
lxw.ucas@gmail.com


####What this Program used for:
Monitor a specific list of url to check whether they have updated(legitimately or maliciously). If the website(url) updated, then send an notification email to a specific list of recipients.<br>
**What's more, if the website(url) cannot be accessed, an an notification email will be sent as well. _Actually This is the main purpose of this program._**<<br>

####Prerequisites:
To run the program correctly, Python is needed.<br>
The version of Python should be newer than **Python 2.6**. Python 2.7 is recommended.

####Usage of each file:
1. criterion:<br>
This file is the intermedia file, contains the md5 value of each url.

2. emails:<br>
This file contains the email addresses that we want to send warning emails to.

3. urls:<br>
This file contains the urls(websites) that we want to monitor.

4. monitorLog:<br>
Log File(monitor Log & Error Log).

5. **myUtils.py**:<br>
Utils for monitorURLs.py & Collect the INITIAL criterion data.

6. **monitorURLs.py**:<br>
Monitor urls: compare the newest data with criterion and offer warnings(emails) if necessary.

7. run.sh:<br>
This script file is the interface to run the whole program. run(manually & crontab) it like this:<br>
**manually**:<br>
 ```
 bash run.sh
 ```
**crontab**:<br>
edit the /etc/crontab file:<br>
 ```
 sudo vim /etc/crontab
 ```
append the configuration like this(you can modify it as you wish):<br>
 ```
 0 9 * * * lxw bash /home/lxw/monitorURL/run.sh > /dev/null
 ```

8. clearLog.sh:<br>
This script file is the interface to clear the Log information and to reinitialize the corresponding files. run(manually & crontab) it like this:<br>
**manually**:<br>
 ```
 bash clearLog.sh
 ```
**crontab**:<br>
edit the /etc/crontab file:<br>
 ```
 sudo vim /etc/crontab
 ```
append the configuration like this(you can modify it as you wish):<br>
 ```
 0 0 * * 0 lxw bash /home/lxw/monitorURL/clearLog.sh > /dev/null
 ```

9. accessErrorURLs:
This file contains the URLs that were found to have access errors when monitored last time.


###Todos:
1. myUtils.py
reviveList is to update the accessErrorURLs, when url revive.
_**The code update accessErrorURLs has not been offered yet.**_

###Bugs:
1. **_There is a SERIOUS bug_**:
I modify one url_file manually(e.g. ./Intermedia_new/http:__blog.dnspod.cn_), it can be monitored. However, the **problem** is that not all files modification can be monitored(e.g. ./Intermedia_new/http:__www.unbound.net_).
2. **_The 2nd bug may have sth to do with the 1st one._**:
I modify one url_file manually(e.g. ./Intermedia_new/http:__blog.dnspod.cn_), it can be monitored. _However, not all contents that are modified can be monitored._
