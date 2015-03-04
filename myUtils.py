#!/usr/bin/python2.7
#coding:utf-8
#如果想有中文注释就必须得有上面的语句
#File: myUtils.py
#Author: lxw
#Time: 2015-02-09
#Usage: Utils & Collect the criterion data that we will use to compare with.

import datetime
import urllib2
import md5
import time
from MyThread.myThread import MyThread
import threading
import smtplib
import base64
from email.message import Message

fileLock = threading.RLock()
logLock = threading.RLock()


def writeLog(tag, url, log):
    """
    Write into Error Log.
    """
    with open("./monitorLog", "a") as f:
        logLock.acquire()
        f.write("{0}: {1}\t{2}\n{3}\n\n".format(tag, url, time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time())), log))
        logLock.release()


def writeFile(url, length, md5Str):
    """
    Write into criterion File.
    """
    with open("./criterion", "a") as f:
        fileLock.acquire()
        f.write("{0},{1},{2}\n".format(url, length, md5Str))
        fileLock.release()

#def sendEmail(subject, content):
    print("Subject:{0}\nContent:{1}\n".format(subject, content))

def sendEmail(subject, content):
    try:
        smtpServer = "smtp.qq.com" #"smtp.cnnic.cn"
        userName = "monitorURL@foxmail.com"#"liuxiaowei@cnnic.cn"
        password = "Python1"

        fromAddr = "monitorURL@foxmail.com"
        toAddrs = ["lxwin@foxmail.com", "liuxiaowei@cnnic.cn"]

        message = Message()
        message["Subject"] = subject
        message["From"] = fromAddr
        message["To"] = ";".join(toAddrs)
        #抄送
        #message["Cc"] = ccAddr
        message.set_payload(content)
        msg = message.as_string()

        sm = smtplib.SMTP(smtpServer)
        sm.set_debuglevel(0)    #sm.set_debuglevel(1)
        sm.ehlo()
        sm.starttls()
        sm.ehlo()
        sm.login(userName, password)

        sm.sendmail(fromAddr, toAddrs, msg)
        time.sleep(5)
        sm.quit()
    except Exception, e:
        start = content.index("\n") + 2
        end = content[start:].index("\n") + 2
        writeLog("EMAIL SENDING ERROR", content[:end], str(e))


def getEmailContent(url, length, md5Str, checkTime, urlObjDic):
    """
    Already GET THE CONTENT OF THE URL. Now to get the Email content if URL updates, or nothing if not.
    length is the new length.
    urlObjDic is the old one.
    """
    content = ""
    try:
        if length < urlObjDic[url].getLength():
            content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息减少(原来{2}B,现在{3}B)，请查看.\n\n".format(url, checkTime, urlObjDic[url].getLength(), length)
        elif length > urlObjDic[url].getLength():
            content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息增加(原来{2}B,现在{3}B)，请查看.\n\n".format(url, checkTime, urlObjDic[url].getLength(), length)
        elif md5Str != urlObjDic[url].getMD5Str():
            content = "URL: {0}\n检测时间: {1}\n检测结果: 检测到网站首页信息更新，请查看.\n\n".format(url, checkTime)
    except KeyError, ke:
        writeLog("-" * 20 + "\nThis can be avoided.\n KeyError", url, str(ke) + "\n" + "-" * 20)
    return content


def eachCriterion(url):
    """
    Create the criterion file. File format: url,length,md5.
    """
    try:
        sourceCode  = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        try:
            #NOTE: some websites do not allow us to access them by this method, they check the userAgent information, so we forge it.
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'};
            req = urllib2.Request(url=url, headers=headers)
            sourceCode  = urllib2.urlopen(req).read()
        except Exception, e:
            writeLog("**Never show because never call.**Access Error", url, str(e))
        else:
            length, md5Str = getLengthMd5(sourceCode)
            writeFile(url, length, md5Str)

    except Exception, e:
        writeLog("**Never show because never call.**Access Error", url, str(e))
    else:
        length, md5Str = getLengthMd5(sourceCode)
        writeFile(url, length, md5Str)


def getLengthMd5(sourceCode):
    """
    retun tuple of len(sourceCode) & md5 value of sourceCode.
    """
    length = len(sourceCode)
    #calculate the md5 value of sourceCode string.(32bits).
    md = md5.new()
    md.update(sourceCode)
    md5Str = md.hexdigest()
    return (length, md5Str)


def initCriterion():
    """
    When first time to get criterion information of each url, call this method.
    """
    #Just to calculate time, not for thred pool NOW.
    threads = []
    with open("./criterion", "w") as f:
        with open("./monitorLog", "w") as f1:
            pass

    with open("./urls") as f:
        while 1:
            url = f.readline().strip()
            if not url:
                break
            #Multiple Thread: Deal with "one url by one single thread".
            mt = MyThread(eachCriterion, (url,))
            mt.start()
            threads.append(mt)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    start = datetime.datetime.now()
    initCriterion()
    end = datetime.datetime.now()
    writeLog("Method initCriterion() finishes. Time cost: ", "", str(end-start) + " seconds.")
