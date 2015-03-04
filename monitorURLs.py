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
import threading
import datetime
from MyThread.myThread import MyThread
import myUtils

#Element format: "url:URL obj"
oldUrlObjDic = {}
newUrlObjDic = {}
aeSubject = "【网站故障通知★】"    #The email subject of te  "accessError" url.
aeContent = ""
aeCount = 0
uwSubject = "【网站更新通知】"     #The email subject of te  "updateWarning" url.
uwContent = ""
uwCount = 0

#RLock
aeLock = threading.RLock()   # Access Error: Email Subject/Content RLock.
uwLock = threading.RLock()   # Update Warning: Email Subject/Content RLock.
nuodLock = threading.RLock()    # newUrlObjDic assignment RLock.


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
            aeLock.acquire()
            if aeCount < 2:
                aeSubject += " " + url
            elif aeCount < 5:
                aeSubject += "."
            aeCount += 1
            aeContent += "URL: {0}\n检测时间: {1}\n检测结果:检测到网站访问故障，请查看.\n\n".format(url, checkTime)
            aeLock.release()
        else:
            length, md5Str = myUtils.getLengthMd5(sourceCode)
            nuodLock.acquire()
            newUrlObjDic[url] = URL(length, md5Str)
            nuodLock.release()

            content = myUtils.getEmailContent(url, length, md5Str, checkTime, oldUrlObjDic)
            if content:
                uwLock.acquire()
                if uwCount < 2:
                    uwSubject += " " + url
                elif uwCount < 5:
                    uwSubject += "."
                uwCount += 1
                uwContent += content
                uwLock.release()
    except Exception, e:
        aeLock.acquire()
        if aeCount < 2:
            aeSubject += " " + url
        elif aeCount < 5:
            aeSubject += "."
        aeCount += 1
        aeContent += "URL: {0}\n检测时间: {1}\n检测结果:检测到网站访问故障，请查看.\n\n".format(url, checkTime)
        aeLock.release()
    else:
        length, md5Str = myUtils.getLengthMd5(sourceCode)
        nuodLock.acquire()
        newUrlObjDic[url] = URL(length, md5Str)
        nuodLock.release()

        content = myUtils.getEmailContent(url, length, md5Str, checkTime, oldUrlObjDic)
        if content:
            uwLock.acquire()
            if uwCount < 2:
                uwSubject += " " + url
            elif uwCount < 5:
                uwSubject += "."
            uwCount += 1
            uwContent += content
            uwLock.release()


def main():
    """
    Monitor URLs.
    """
    # set value for oldUrlObjDic dict.
    with open("./criterion") as f:
        while 1:
            string = f.readline().strip()
            if not string:
                break
            arr = string.split(",")
            #URL Object Format: URL(length, md5)
            oldUrlObjDic[arr[0]] = URL(int(arr[1]), arr[2])

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
        myUtils.sendEmail(aeSubject, allContent)
    if uwCount >0:
        allContent = "本次共检测到{0}个网站有更新, 详细信息如下:\n\n{1}".format(uwCount, uwContent)
        myUtils.sendEmail(uwSubject, allContent)

    #Update Criterion file.
    with open("./criterion", "w") as f:
        for url in newUrlObjDic.keys():
            f.write("{0},{1},{2}\n".format(url, newUrlObjDic[url].length, newUrlObjDic[url].getMD5Str()))


if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print(end - start)
else:
    print("Being imported as a module.")
