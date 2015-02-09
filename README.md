####Specification:
To run the program correctly, Python is needed.
The version of Python should be newer than **Python 2.6**.

####Usage of each file:
1. emails:<br>
email addresses that we want to send warning emails to.

2. urls:<br>
urls(websites) that we want to monitor.

3. monitorLog:<br>
Error Log File.

4. **abandoned**_initialize.sh:<br>
Create corresponding directories(each url owns one directory) for urls._

5. getCriterion.py:<br>
Collect the criterion data that we will use to compare with.

6. monitorURLs.py:<br>
monitor urls: compare the newest data with criterion and offer warnings if necessary.
