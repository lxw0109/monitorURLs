#!/usr/bin/python2.7
#coding:utf-8
#如果想有中文注释就必须得有上面的语句
#File: monitorUrgentURLs.py
#Author: lxw
#Time: 2015-02-06
#Usage: Monitor the website specified in the "urls" file.

import urllib2
import time
import threading
import datetime
from MyThread.myThread import MyThread
import urgentMyUtils
import sys
import traceback

#Element format: url:length, md5)
oldUrlObjDic = {}
newUrlObjDic = {}
aeSubject = "【网站故障通知★】"    #The email subject of te  "accessError" url.
aeContent = ""
aeCount = 0
uwSubject = "【网站更新通知】"     #The email subject of te  "updateWarning" url.
uwContent = ""
uwCount = 0
#updateURLs = []     #the URLs that have updated when monitored last time.
aeURLs = []     #the URLs that have access errors when monitored last time.

#RLock
aeLock = threading.RLock()   # Access Error: Email Subject/Content RLock.
uwLock = threading.RLock()   # Update Warning: Email Subject/Content RLock.
nuodLock = threading.RLock()    # newUrlObjDic assignment RLock.

THREADS_NUM = 100   # limit the number of threads

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
    def setLength(self, length):
        self.length = length
    def setMD5Str(self, md5Str):
        self.md5Str = md5Str


def monitor(url):
    """
    monitor each url.
    """
    global aeLock, aeSubject, aeContent, uwLock, uwSubject, uwContent
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
            if url not in aeURLs:
                aeLock.acquire()
                if aeCount < 2:
                    aeSubject += " " + url
                elif aeCount < 5:
                    aeSubject += "."
                aeCount += 1
                aeContent += "URL: {0}\n监测时间: {1}\n监测结果:监测到网站访问故障，请查看.\n\n".format(url, checkTime)
                #with open("./accessErrorURLs", "a") as f:
                #    f.write(url + "\n")
                aeURLs.append(url)
                aeLock.release()
        else:
            length, md5Str = urgentMyUtils.getLengthMd5(sourceCode)
            nuodLock.acquire()
            newUrlObjDic[url] = URL(length, md5Str)
            nuodLock.release()
            content = urgentMyUtils.getEmailContent(url, length, md5Str, checkTime, oldUrlObjDic, sourceCode, aeURLs)
            if content:
                uwLock.acquire()
                if uwCount < 2:
                    uwSubject += " " + url
                elif uwCount < 5:
                    uwSubject += "."
                uwCount += 1
                uwContent += content
                uwLock.release()
            urgentMyUtils.recordInFile(url, sourceCode)
    except Exception, e:
        if url not in aeURLs:
            aeLock.acquire()
            if aeCount < 2:
                aeSubject += " " + url
            elif aeCount < 5:
                aeSubject += "."
            aeCount += 1
            aeContent += "URL: {0}\n监测时间: {1}\n监测结果:监测到网站访问故障，请查看.\n\n".format(url, checkTime)
            aeURLs.append(url)
            aeLock.release()
    else:
        length, md5Str = urgentMyUtils.getLengthMd5(sourceCode)
        nuodLock.acquire()
        newUrlObjDic[url] = URL(length, md5Str)
        nuodLock.release()
        content = urgentMyUtils.getEmailContent(url, length, md5Str, checkTime, oldUrlObjDic, sourceCode, aeURLs)
        if content:
            uwLock.acquire()
            if uwCount < 2:
                uwSubject += " " + url
            elif uwCount < 5:
                uwSubject += "."
            uwCount += 1
            uwContent += content
            uwLock.release()
        urgentMyUtils.recordInFile(url, sourceCode)

def process_stale(url):
    """
    change from monitor()
    diff website source code using history data in Intermedia/ and Intermedia_new/.
    Primarily use this method to reproduce the same dealing process TO DEBUG.
    """
    global aeLock, uwLock, uwSubject, uwContent, uwCount
    checkTime = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time()))
    #lxw_NOTE:getEmailContent_stale() "thread safe"?
    try:
        content = urgentMyUtils.getEmailContent_stale(url, oldUrlObjDic[url], newUrlObjDic[url])
        if content:
            uwLock.acquire()
            if uwCount < 2:
                uwSubject += " " + url
            elif uwCount < 5:
                uwSubject += "."
            uwCount += 1
            uwContent += content
            uwLock.release()
    except KeyError, ke:
        content = "URL: {0}\n检测时间: {1}\n检测结果: 网站恢复访问(上次检测时网站不可访问).\n\n".format(url, checkTime)
        string1 = "[Quite Normal, url recovery.] lxw_KeyError"
        string2 = url
        string3 = ""
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        urgentMyUtils.writeLog(string1, string2, string3)
        if url in aeURLs:
            aeLock.acquire()
            aeURLs.remove(url)
            aeLock.release()
    except Exception, e:
        string1 = "lxw_Exception."
        string2 = ""
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        urgentMyUtils.writeLog(string1, string2, string3)


def main_fresh(dbOrNot):
    """
    Monitor URLs using fresh data.
    """
    # set value for oldUrlObjDic dict.
    f = open("./urgentCriterion_new")
    while 1:
        string = f.readline().strip()
        if not string:
            break
        arr = string.split(",")
        #URL Object Format: URL(length, md5)
        oldUrlObjDic[arr[0]] = URL(int(arr[1]), arr[2])
    f.close()

    f = open("./urgentAccessErrorURLs")
    while 1:
        string= f.readline().strip()
        if not string:
            break
        aeURLs.append(string)
    f.close()

    threadingNum = threading.Semaphore(THREADS_NUM)
    threads = []
    urlCount = 0
    # monitor each url in .urls file
    f = open("./.urgentURLS")
    while 1:
        url = f.readline().strip()
        if not url:
            break
        #Multiple Thread: Deal with "one url by one single thread".
        mt = MyThread(monitor, (url,), threadingNum)
        #mt.start()
        threads.append(mt)
        urlCount += 1
    f.close()
    for thread in threads:
        thread.start()

    while 1:
        over = True
        for thread in threads:
            if thread.isAlive():
                if not thread.isTimedOut():     # not "Timed Out".
                    over = False
                else:
                    urgentMyUtils.writeLog("lxw_Timed Out", thread.getURL(), "")
        if over:
            break

    if aeCount > 0:
        allContent = "本次共监测网站{0}个, 其中有{1}个网站访问异常, 详细信息如下:\n\n{2}".format(urlCount, aeCount, aeContent)
        urgentMyUtils.sendEmail(aeSubject, allContent)
    if uwCount >0:
        allContent = "本次共监测网站{0}个, 其中有{1}个网站监测到有更新, 详细信息如下:\n\n{2}".format(urlCount, uwCount, uwContent)
        urgentMyUtils.sendEmail(uwSubject, allContent)

    #Update Criterion file.
    f = open("./urgentCriterion_new", "w")
    for url in newUrlObjDic.keys():
        f.write("{0},{1},{2}\n".format(url, newUrlObjDic[url].length, newUrlObjDic[url].getMD5Str()))
    f.close()

    dbOrNot = False
    if dbOrNot:
        #update criterion in database
        urgentMyUtils.updateCriterion(newUrlObjDic)

    #Update accessErrorURLs file.
    f = open("./urgentAccessErrorURLs", "w")
    for url in aeURLs:
        f.write(url + "\n")
    f.close()

def main_stale(dbOrNot):
    """
    Monitor URLs using stale data(history data).
    Primarily use this method to reproduce the same dealing process TO DEBUG.
    """
    try:
        # set value for oldUrlObjDic dict.
        f = open("./urgentCriterion")
        while 1:
            string = f.readline().strip()
            if not string:
                break
            arr = string.split(",")
            #URL Object Format: URL(length, md5)
            oldUrlObjDic[arr[0]] = URL(int(arr[1]), arr[2])
        f.close()

        # set value for newUrlObjDic dict.
        f = open("./urgentCriterion_new")
        while 1:
            string = f.readline().strip()
            if not string:
                break
            arr = string.split(",")
            #URL Object Format: URL(length, md5)
            newUrlObjDic[arr[0]] = URL(int(arr[1]), arr[2])
        f.close()
    except IOError, ioe:
        string1 = "lxw_IOError."
        string2 = ""
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        urgentMyUtils.writeLog(string1, string2, string3)
    except Exception, e:
        string1 = "lxw_Exception."
        string2 = ""
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        urgentMyUtils.writeLog(string1, string2, string3)

    threadingNum = threading.Semaphore(THREADS_NUM)
    threads = []

    for url in newUrlObjDic.keys():
        try:
            #Multiple Thread: Deal with "one url by one single thread".
            mt = MyThread(process_stale, (url,), threadingNum)
            threads.append(mt)
        except Exception, e:
            string1 = ""
            string2 = ""
            string3 = "Being imported as a module."
            string4 = "\n" + "------"*13 + "\n"
            string3 += string4
            urgentMyUtils.writeLog(string1, string2, string3)

    for thread in threads:
        thread.start()

    while 1:
        over = True
        for thread in threads:
            if thread.isAlive():
                if not thread.isTimedOut():     # not "Timed Out".
                    over = False
                else:
                    urgentMyUtils.writeLog("lxw_Timed Out", thread.getURL(), "")
        if over:
            break

    for thread in threads:
        thread.join()

    urlCount = len(newUrlObjDic)
    if aeCount > 0:
        allContent = "本次共监测网站{0}个, 其中有{1}个网站访问异常, 详细信息如下:\n\n{2}".format(urlCount, aeCount, aeContent)
        urgentMyUtils.sendEmail(aeSubject, allContent)
    if uwCount >0:
        allContent = "本次共监测网站{0}个, 其中有{1}个网站监测到有更新, 详细信息如下:\n\n{2}".format(urlCount, uwCount, uwContent)
        urgentMyUtils.sendEmail(uwSubject, allContent)

def getDbOrNot():
    try:
        f = open("./dbOrFiles")
        dbFlag = False
        while 1:
            line = f.readline()
            if not line:
                break
            if "0" not in line:
                if "1" not in line:
                    dbFlag = False
                else:
                    dbFlag = True
            else:
                dbFlag = False
        return dbFlag
    except Exception, e:
        string1 = "lxw_No such file."
        string2 = "./dbOrFiles"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        urgentMyUtils.writeLog(string1, string2, string3)
        return False

if __name__ == '__main__':
    start = datetime.datetime.now()
    dbOrNot = getDbOrNot()
    if len(sys.argv) < 2:
        main_fresh(dbOrNot)
        #urgentMyUtils.writeData("len<2\t{0}\n".format(sys.argv))
    elif sys.argv[1] == "debug":
        main_stale(dbOrNot)
        #urgentMyUtils.writeData("len>=2\tlen:{0}\t{1}\n".format(len(sys.argv), sys.argv))

    end = datetime.datetime.now()

    urgentMyUtils.writeData("Monitor Finished.   Monitor Time: {0}.   Time Cost: {1}'{2}\"\n{3}\n\n{3}\n".format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time())), (end-start).seconds//60, (end - start).seconds%60, "------"*13))
else:
    string1 = ""
    string2 = ""
    string3 = "Being imported as a module."
    string4 = "\n" + "------"*13 + "\n"
    string3 += string4
    urgentMyUtils.writeLog(string1, string2, string3)
