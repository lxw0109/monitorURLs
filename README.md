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

###DATABASE:
1. create database:
create database monitorURL character set utf8;
2. create 3 tables:
criterion:<br>
```
create table criterion
(
    url varchar(200) not null primary key,
    length int unsigned not null,
    md5Str varchar(100) no null
);
```
oldURLSC:<br>
```
create table oldURLSC
(
    url varchar(200) not null primary key,
    sourceCode mediumtext not null
);
```
newURLSC:<br>
```
create table newURLSC
(
    url varchar(200) not null primary key,
    sourceCode mediumtext not null
);
```


###Feature Functions:
1. Give the diff content:
Give the differences between the content of 2 monitoring.

2. Update the accessErrorURLs:
When url revives(access error ocurred last time, but not this time), remove it from the accessErrorURLs.<br>

3. Limit the number of threads
Considering that the number of urls to be monitored may be LARGE, the program limits the number of threads to 100 which means less than 100 urls being monitored at each moment. It does matter the time cost of the program, but I think it's OK(not too slow).


###Peformance:
1. Time cost:
Monitor each url with one single thread. <br>
The program costs around 26s when running on the Server, while it costs less on my local PC. **_So, it means that the performance of the server I use is not good at all._** :) 

###Negtive Factors:
1. The clock time on the server loses 4 minutes, which means that we receive the email a little later than expected.

###_*Special Cases_:
1. What do you think if you got the following information:
```
URL: https://www.dns-oarc.net/
检测时间: 2015-03-17-09:00:01
检测结果:检测到网站首页信息减少(原来29478B,现在29466B)，具体的差异如下:
+  Root Zone Archive
+ Public Stories, etc
+ Read the rest of Root Zone Archive.
-  Root Zone Archive
- Public Stories, etc
- Read the rest of Root Zone Archive.
```
At the first sight of these data, I think there may be something wrong with my program(or may be the diff function offered is not good and smart enough). However, when I checked the sourcecode of the url, I found that this output is rational.<br>
If you want to check the sourcecode of the url, you can run:
```
$ vimdiff Demos/old Demos/new
```
Notice the differences between them(especially the lines contain "title="), and you will understand that **"disorder" makes this**.


###HUGE BUGS:
1. The url `http://www.denic.de/en/homepage.html` always blocks the program.
I CANNOT figure it out right now.
Solutions:<br>
If one url costs too much time and does not stop before the time we can wait(1 minute). We will ignore this url and kill the running thread/process.


###Todos:
2. set a flag to control get the source code of the urls from the urlopen or from the Intermedia_new.
NOTE: you should control the criterion as the same time.
This means that I can compare the history datas(last 2 times), don't have to be the newest.
3. Add test code to each file.
4. Use database for data storage.
5. PySpider: 1. QuickStart&Command Line P2 jQuery to select elements to be extracted.
