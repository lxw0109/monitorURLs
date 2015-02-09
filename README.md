####Specification:
To run the program correctly, Python is needed.
The version of Python should be newer than **Python 2.6**.

####Usage of each file:
1. emails:
email addresses that we want to send warning emails to.

2. urls:
urls(websites) that we want to monitor.

3. monitorLog:
Error Log File.

__4. initialize.sh:
Create corresponding directories(each url owns one directory) for urls.__

5. getCriterion.py:
Collect the criterion data that we will use to compare with.

6. monitorURLs.py:
monitor urls: compare the newest data with criterion and offer warnings if necessary.
