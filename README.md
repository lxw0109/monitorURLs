####What this Program used for:
Monitor a specific list of url to check whether they have updated(legitimately or maliciously).<br>
If the website(url) updated, then send an notification email to a specific list of recipients.<br>
**What's more, if the website(url) cannot be accessed, an an notification email will be sent as well.**<br>
_Actually This is the main purpose of this program._<br>

####Prerequisites:
To run the program correctly, Python is needed.
The version of Python should be newer than **Python 2.6**. Python 2.7 is recommended.

####Usage of each file:
1. emails:<br>
email addresses that we want to send warning emails to.

2. urls:<br>
urls(websites) that we want to monitor.

3. monitorLog:<br>
Error Log File.

4. myUtils.py:<br>
Utils for monitorURLs.py & Collect the INITIAL criterion data.

5. monitorURLs.py:<br>
monitor urls: compare the newest data with criterion and offer warnings(emails) if necessary.

####Functionality Wanted:
1. Give diff content.

####Existing Bugs:
1. encoding problems
