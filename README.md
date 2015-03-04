####What this Program used for:
Monitor a specific list of url to check whether they have updated(legitimately or maliciously). If the website(url) updated, then send an notification email to a specific list of recipients.<br>
**What's more, if the website(url) cannot be accessed, an an notification email will be sent as well. _Actually This is the main purpose of this program._**<<br>

####Prerequisites:
To run the program correctly, Python is needed.<br>
The version of Python should be newer than **Python 2.6**. Python 2.7 is recommended.

####Usage of each file:
1. criterion:<br>
intermedia file, contains the md5 value of each url.

2. emails:<br>
email addresses that we want to send warning emails to.

3. urls:<br>
urls(websites) that we want to monitor.

4. monitorLog:<br>
Log File(monitor Log & Error Log).

5. **myUtils.py**:<br>
Utils for monitorURLs.py & Collect the INITIAL criterion data.

6. **monitorURLs.py**:<br>
monitor urls: compare the newest data with criterion and offer warnings(emails) if necessary.

7. run.sh:<br>
the interface to run the whole program. run(manually & crontab) it like this:<br>
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
1. Need 3 files: Criterion, Update URLs, AccessError URLs.
2. Give diff content.
