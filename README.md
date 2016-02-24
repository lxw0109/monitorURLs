####Open for Suggestions & Feedback:
lxw.ucas@gmail.com

####What this Program used for:
Monitor a specific list of urls to check whether they have updated(legitimately or maliciously).<br>
If the website(url) updated, then send an notification email to a specific list of recipients.<br>
**What's more, if the website(url) cannot be accessed, an an notification email will be sent as well.** <br>
**_Actually this is the main purpose of this program._**<br>

####Prerequisites:
To run the program correctly, Python is needed.<br>
The version of Python should be newer than **Python 2.6**. Python 2.7 is recommended.

####Usage of each file:
1. criterion:<br>
This file is the intermedia file, contains the md5 value of each url.

2. emails:<br>
This file contains the recipients(email addresses) that we want to send warning emails to.

3. urls:<br>
This file contains the urls(websites) that we want to monitor.

4. monitorLog:<br>
Log File(monitor Log & Error Log).

5. **myUtils.py**:<br>
Utils for monitorURLs.py & Collect the INITIAL criterion data.

6. **monitorURLs.py**:<br>
Monitor urls: compare the newest data with criterion and offer warnings(emails) when necessary.

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

9. accessErrorURLs:<br>
This file contains the URLs that were found to have access errors when monitored last time.

###DATABASE:
1. create database:<br>
create database monitorURL character set utf8;<br>
2. create 3 tables:<br>
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
1. Give the diff content:<br>
Give the differences between the content of 2 monitoring urls.<br>

2. Update the accessErrorURLs:<br>
When url revives(access error ocurred last time, but recovered this time), remove it from the accessErrorURLs.<br>

3. Limit the number of threads<br>
Considering that the number of urls to be monitored may be LARGE, the program limits the number of threads to 100 which means less than 100 urls being monitored at each moment. It does matter the time cost of the program, but I think it's OK(not too slow).<br>

4. Support "debug" mode. Run the program in the following format:<br>
 ```
 python ./monitorURLs.py "debug" >> ./monitorLog
 ```
5. ["The entire Python program exits when no alive non-daemon threads are left"](https://docs.python.org/2.7/library/threading.html),
**So, I make the program could terminate in finite time by using setDaemon(True) method**.</br>
[Reference](http://www.cnblogs.com/jefferybest/archive/2011/10/09/2204050.html)

###Peformance:
1. Time cost:<br>
Monitor each url with one single thread. <br>
The program costs around 18s when running on the Server, while it costs less(less than 10s) on my local PC.<br>

###_*Special Cases_:
1. What do you think if you got the following information:<br>
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
If you want to check the sourcecode of the url, you can run:<br>
```
$ vimdiff Demos/dns_oarc_old Demos/dns_oarc_new
```
Notice the differences between them(especially the lines contain "title="), and you will understand that **"DISORDER" makes this**.<br>

2. If we run DIFF before PICK, the result maybe confusing:<br>
```
URL: http://www.denic.de/en/homepage.html
检测时间: 2015-03-31-23:48:53
检测结果:检测到网站首页信息减少(上次检测23.93K,本次检测23.83K)，具体差异如下:
-Sprunglink
+Sprunglink
-Opens internal link in current window
+Opens internal link in current window
```
REASON: the difference between the lines contains **title=""**, but the different part is not **title=""**. So when we pick out the title="", it seems weird.<br>

###HUGE BUGS in History:
1. The url `http://www.denic.de/en/homepage.html` always blocks the program.<br>
I CANNOT figure it out right now.<br>
Solutions:<br>
If one url costs too much time and does not stop before the time we can wait(1 minute). We will ignore this url and kill the running thread/process.
2. When access error occured, diff did not run. This may miss some updates.
Add diff when access error recovers.<br>
3. "no update information" bug<br>
Some guy in JD told me that maybe we just cared about the information appended instead of the information deleted(which may be pushed into the second pages).<br>
So I filtered the result of diff to remove the lines began with "-" on October 26. This means that all lines begin with "+" in the mail content.
So the "no update information" bug appeared, in pickFilter()[urgentMyUtils.py] I filtered all lines begin with "+" BY MISTAKE.<br>

###Todos:
0. Offer a function that we can **specify a few words** so that only the information contains the words shows.<br>
