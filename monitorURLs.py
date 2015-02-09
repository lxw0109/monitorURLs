#!/usr/bin/python2.7
#coding:utf-8
#如果想有中文注释就必须得有上面的语句
#File: monitorURLs.py
#Author: lxw
#Time: 2015-02-06
#Usage: Monitor the website specified in the "urls" file.

import urllib2
import time
import md5
import smtplib
import base64
from email.message import Message
import threading
import datetime
from MyThread.myThread import MyThread

#Element format: "url:URL obj"
urlObjDic = {}
logLock = threading.RLock()
aeSubject = "【网站故障通知★】"    #The email subject of te  "accessError" url.
aeContent = ""
aeCount = 0
uwSubject = "【网站更新通知】"     #The email subject of te  "updateWarning" url.
uwContent = ""
uwCount = 0

#RLock
aeSubLock = threading.RLock()   # Access Error Email Subject RLock.
aeConLock = threading.RLock()   # Access Error Email Content RLock.
uwSubLock = threading.RLock()   # Update Warning Email Content RLock.
uwConLock = threading.RLock()   # Update Warning Error Email Content RLock.

class URL(object):
    """
    URL: The object(length & md5) corresponding to the url.
    each line in urls file stands for one single object.
    """

    def __init__(self, length, md5Str):
        self.length = length
        self.md5Str = md5Str

    def getLength(self):
        return self.length

    def getMD5Str(self):
        return self.md5Str


def sendEmail(subject, content):
    try:
        smtpServer = "smtp.qq.com" #"smtp.cnnic.cn"
        userName = "554188913@qq.com"#"liuxiaowei@cnnic.cn"
        password = "Python1"

        fromAddr = "554188913@qq.com"
        #toAddrs = ["lxwin@foxmail.com", "lab_student@cnnic.cn"]
        toAddrs = ["chenyong@cnnic.cn", "liuxiaowei@cnnic.cn", "lxwin@foxmail.com"]

        message = Message()
        message["Subject"] = subject
        message["From"] = fromAddr
        message["To"] = ";".join(toAddrs)
        #抄送
        #message["Cc"] = ccAddr
        message.set_payload(content)
        msg = message.as_string()

        sm = smtplib.SMTP(smtpServer)
        #sm.set_debuglevel(1)
        sm.ehlo()
        sm.starttls()
        sm.ehlo()
        sm.login(userName, password)

        sm.sendmail(fromAddr, toAddrs, msg)
        time.sleep(5)
        sm.quit()
    except Exception, e:
        end = content.index("\n")
        writeLog("EMAIL SENDING ERROR", content[:end]+"\n", str(e))


def writeLog(tag, url, log):
    """
    Write into Error Log.
    """
    #with open("./monitorLog", "a") as f:
    f = open("./monitorLog", "a")
    logLock.acquire()
    f.write("{0}: {1}\t{2}\n{3}\n\n".format(tag, url, time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time())), log))
    logLock.release()


def monitor(url):
    """
    monitor each url.
    """
    global aeSubLock, aeConLock, aeSubject, aeContent, uwSubLock, uwConLock, uwSubject, uwContent
    global aeCount, uwCount
    checkTime = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time()))
    try:
        sourceCode = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        try:
            #NOTE: some websites do not allow us to access them by this method, they check the userAgent information, so we forge it.
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'};
            req = urllib2.Request(url=url, headers=headers)
            sourceCode  = urllib2.urlopen(req).read()
        except Exception, e:
            aeSubLock.acquire()
            if aeCount < 2:
                aeSubject += " " + url
            else:
                aeSubject += "."
            aeCount += 1
            aeSubLock.release()

            aeConLock.acquire()
            aeContent += "URL: {0}\n检测时间: {1}\n检测结果:检测到网站访问故障，请查看.\n\n".format(url, checkTime)
            aeConLock.release()
        else:
            content = getEmailContent(url, sourceCode, checkTime)
            if content:
                uwSubLock.acquire()
                if uwCount < 2:
                    uwSubject += " " + url
                else:
                    uwSubject += "."
                uwCount += 1
                uwSubLock.release()

                uwConLock.acquire()
                uwContent += content
                uwConLock.release()
    except Exception, e:
        aeSubLock.acquire()
        if aeCount < 2:
            aeSubject += " " + url
        else:
            aeSubject += "."
        aeCount += 1
        aeSubLock.release()

        aeConLock.acquire()
        aeContent += "URL: {0}\n检测时间: {1}\n检测结果:检测到网站访问故障，请查看.\n\n".format(url, checkTime)
        aeConLock.release()
    else:
        content = getEmailContent(url, sourceCode, checkTime)
        if content:
            uwSubLock.acquire()
            if uwCount < 2:
                uwSubject += " " + url
            else:
                uwSubject += "."
            uwCount += 1
            uwSubLock.release()

            uwConLock.acquire()
            uwContent += content
            uwConLock.release()


def getEmailContent(url, sourceCode, checkTime):
    """
    Already GET THE CONTENT OF THE URL. Now to get the Email content if URL updates, or nothing if not.
    """
    length = len(sourceCode)
    content = ""
    if length < urlObjDic[url].getLength():
        content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息减少(原来{2}B,现在{3}B)，请查看.\n\n".format(url, checkTime, urlObjDic[url].getLength(), length)
    elif length > urlObjDic[url].getLength():
        content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息增加(原来{2}B,现在{3}B)，请查看.\n\n".format(url, checkTime, urlObjDic[url].getLength(), length)
    else:
        #calculate the md5 value of sourceCode string.(32bits).
        md = md5.new()
        md.update(sourceCode)
        md5Str = md.hexdigest()
        if md5Str != urlObjDic[url].getMD5Str():
            content = "URL: {0}\n检测时间: {1}\n检测结果: 检测到网站首页信息更新，请查看.\n\n".format(url, checkTime)
    return content


def main():
    global uwCount, aeCount
    # set value for urlObjDic dict.
    with open("./criterion") as f:
        while 1:
            string = f.readline().strip()
            if not string:
                break
            arr = string.split(",")
            #URL Object Format: URL(length, md5)
            urlObjDic[arr[0]] = URL(int(arr[1]), arr[2])

    #Just to calculate time, not for thred pool NOW.
    threads = []
    # monitor each url in urls file
    with open("./urls") as f:
        while 1:
            url = f.readline().strip()
            if not url:
                break
            #Multiple Thread: Deal with "one url by one single thread".
            mt = MyThread(monitor, (url,))
            mt.start()
            threads.append(mt)

    for thread in threads:
        thread.join()

    if aeCount > 0:
        allContent = "本次共检测到{0}个网站访问异常, 详细信息如下:\n\n{1}".format(aeCount, aeContent)
        sendEmail(aeSubject, allContent)
    if uwCount >0:
        allContent = "本次共检测到{0}个网站有更新, 详细信息如下:\n\n{1}".format(uwCount, uwContent)
        sendEmail(uwSubject, allContent)


if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print(end - start)
else:
    print("Being imported as a module.")
