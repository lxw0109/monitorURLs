####What this Program used for:
Monitor a specific list of url to check whether they have updated(legitimately or maliciously). If the website(url) updated, then send an notification email to a specific list of recipients.<br>
**What's more, if the website(url) cannot be accessed, an an notification email will be sent as well. _Actually This is the main purpose of this program._**<<br>

####Prerequisites:
To run the program correctly, Python is needed.<br>
The version of Python should be newer than **Python 2.6**. Python 2.7 is recommended.

####Usage of each file:
0. criterion:<br>
intermedia file, contains the md5 value of each url.

1. emails:<br>
email addresses that we want to send warning emails to.

2. urls:<br>
urls(websites) that we want to monitor.

3. monitorLog:<br>
Log File(monitor Log & Error Log).

4. **myUtils.py**:<br>
Utils for monitorURLs.py & Collect the INITIAL criterion data.

5. **monitorURLs.py**:<br>
monitor urls: compare the newest data with criterion and offer warnings(emails) if necessary.

6. run.sh:<br>
the interface to run the whole program. run(manually & crontab) it like this:
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
*/3 * * * * lxw bash /home/lxw/Project/monitorURL/run.sh
```

####Functionality Wanted:
1. Give diff content.

####Existing Bugs:
1. encoding problems
