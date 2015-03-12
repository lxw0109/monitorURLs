#!/usr/bin/python2.7
#coding:utf-8
#如果想有中文注释就必须得有上面的语句
#File: myUtils.py
#Author: lxw
#Time: 2015-02-09
#Usage: Utils & Collect the criterion data that we will use to compare with.

import datetime
import urllib2
import hashlib
import time
from MyThread.myThread import MyThread
import threading
import smtplib
import base64
from email.message import Message
import difflib
import traceback

fileLock = threading.RLock()
logLock = threading.RLock()

reviveList = []
rLLock = threading.RLock()   # reviveList Lock.
#reviveList is to update the accessErrorURLs, when url revive.

def writeLog(tag, url, log):
    """
    Write into Error Log.
    """
    with open("./monitorLog", "a") as f:
        logLock.acquire()
        f.write("{0}: {1}\t{2}\n{3}\n".format(tag, url, time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time())), log))
        logLock.release()


def writeFile(url, length, md5Str):
    """
    Write into criterion File.
    """
    with open("./criterion", "a") as f:
        fileLock.acquire()
        f.write("{0},{1},{2}\n".format(url, length, md5Str))
        fileLock.release()


def sendEmail(subject, content):
    """
    Send Email.
    """
    writeLog("EMAIL SENDING", "", "")
    try:
        #smtpServer = "smtp.qq.com" #"smtp.cnnic.cn"
        smtpServer = "smtp.cnnic.cn"
        #userName = "monitorURL@foxmail.com"#"liuxiaowei@cnnic.cn"
        userName = "liuxiaowei@cnnic.cn"
        #password = "Python1"
        password = "8885741a"

        #fromAddr = "monitorURL@foxmail.com"
        fromAddr = "liuxiaowei@cnnic.cn"
        #toAddrs = ["chenyong@cnnic.cn", "lab_student@cnnic.cn"]
        #toAddrs = ["chenyong@cnnic.cn", "liuxiaowei@cnnic.cn"]
        toAddrs = ["lxwin@foxmail.com", "liuxiaowei@cnnic.cn"]

        message = Message()
        message["Subject"] = subject
        message["From"] = fromAddr
        message["To"] = ";".join(toAddrs)
        #抄送
        #message["Cc"] = ccAddr
        message.set_payload(content)
        message.set_charset("utf-8")
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
        #start = content.index("\n") + 2
        #end = content[start:].index("\n") + 2
        #writeLog("EMAIL SENDING ERROR", content[:end], str(e))
        writeLog("EMAIL SENDING ERROR", "", traceback.format_exc())
    else:
        writeLog("EMAIL SENDING SUCCESS", "", "")

def getEmailContent(url, length, md5Str, checkTime, urlObjDic, sourceCode):
    """
    Already GET THE CONTENT OF THE URL. Now to get the Email content if URL updates, or nothing if not.
    length is the new length.
    urlObjDic is the old one.
    """
    content = ""
    filename = "./Intermedia/" + url.replace("/", "_")
    try:
        conList = diff2Str(filename, sourceCode)
        if conList != []:
            if length < urlObjDic[url].getLength():
                content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息减少(原来{2}B,现在{3}B)，具体的差异如下:\n".format(url, checkTime, urlObjDic[url].getLength(), length)
                for item in conList:
                    content += item + "\n"
                content += "\n"
            elif length > urlObjDic[url].getLength():
                content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息增加(原来{2}B,现在{3}B)，具体的差异如下:\n".format(url, checkTime, urlObjDic[url].getLength(), length)
                for item in conList:
                    content += item + "\n"
                content += "\n"
            elif md5Str != urlObjDic[url].getMD5Str():
                content = "URL: {0}\n检测时间: {1}\n检测结果: 检测到网站首页信息更新，具体的差异如下:\n".format(url, checkTime)
                for item in conList:
                    content += item + "\n"
                content += "\n"
    except KeyError, ke:
        #writeLog("-" * 20 + "\nThis can be avoided.\n KeyError", url, str(ke) + "\n" + "-" * 20)
        content = "URL: {0}\n检测时间: {1}\n检测结果: 网站恢复访问(上次检测时网站不可访问).\n\n".format(url, checkTime)
        #This function will be invoked by multi threads.
        rLLock.acquire()
        reviveList.append(url)
        rLLock.release()
    return content


def diff2Str(filename, sourceCode):
    """
    diff the content of "filename" between the latest 2 monitorings.
    """
    try:
        global flag
        list1 = []
        with open(filename) as f:
            while 1:
                string = f.readline()
                if not string:
                    break
                #NOTE: the rstrip() in the following line is essential.
                list1.append(string.strip())

        list2 = sourceCode.splitlines()
        length = len(list2)
        for index in xrange(length):
            list2[index] = list2[index].strip()
        list1 = filter(list1)
        list2 = filter(list2)

        d = difflib.Differ()
        resList = list(d.compare(list1, list2))
        length = len(resList)
        finList = []

        #NOTE: the following code has serious problems.
        """
        # Problems: index out of boundary.
        for index in xrange(length):
            if resList[index].startswith(" "):    # ignore the lines that are identical.
                del resList[index]
            elif len(resList[index]) < 5: # delete the lines ht is maningless
                del resList[index]
        """

        for index in xrange(length):
            #print("\n--------------------\n" + resList[index][0] + "\n--------------------\n")
            if resList[index].startswith(" "):      # ignore the lines that are identical.
                pass
            elif resList[index].startswith("?"):    # ignore the lines that start with "?"
                pass
            elif len(resList[index].strip()) < 5:            # delete the lines that is meaningless
                pass
            else:
                finList.append(resList[index])

        return finList
        #filter finList to ignore the information that's not important.
        #return filter(finList)
        #Actually, we should filter both of the 2 lists in advance.
    except IOError, e:
        writeLog("IOERROR Occurred", "", traceback.format_exc())
    except Exception, e:
        writeLog("ERROR", "", traceback.format_exc())
        return []


def filter(aList):
    """
    filter aList to ignore the information that's not important.
    """
    resList = []
    try:
        for item in aList:
            index1 = item.find("title=\"")
            if index1 > 0:  #contain
                index2 = item[index1+7:].find("\"")
                resList.append(item[0] + item[index1+7:index1+7+index2])
    except Exception, e:
        writeLog("ERROR", "", traceback.format_exc())

    return resList


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
            writeLog("**Never show because never call.**Access Error", url, traceback.format_exc())
        else:
            length, md5Str = getLengthMd5(sourceCode)
            writeFile(url, length, md5Str)

    except Exception, e:
        writeLog("**Never show because never call.**Access Error", url, traceback.format_exc())
    else:
        length, md5Str = getLengthMd5(sourceCode)
        writeFile(url, length, md5Str)


def recordInFile(url, sourceCode):
    """
    record he sourceCode of the url into the specific file.
    """
    url = url.replace("/", "_")

    filename = "./Intermedia_new/" + url
    with open(filename, "w") as f:
        f.write(sourceCode + "\n")


def getLengthMd5(sourceCode):
    """
    retun tuple of len(sourceCode) & md5 value of sourceCode.
    """
    length = len(sourceCode)
    #calculate the md5 value of sourceCode string.(32bits).
    hash = hashlib.md5()
    hash.update(sourceCode)
    md5Str = hash.hexdigest()
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
