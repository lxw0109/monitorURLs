#!/usr/bin/python2.7
#coding:utf-8
#如果想有中文注释就必须得有上面的语句
#!/usr/bin/python2.7
# FileName: crawl.py
# Author: lxw
# Date: 2016-02-18

import urllib2
import time
import threading
import datetime
from MyThread.myThread import MyThread
import sys
import traceback

aeLock = threading.RLock()   # Access Error: RLock.
#fileLock = threading.RLock()
THREADS_NUM = 100   # limit the number of threads

aeURLs = []

def monitor(url):
    """
    monitor each url.
    """
    global aeLock
    checkTime = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time()))
    try:
        #NOTE: some websites do not allow us to access them by this method, they check the userAgent information, so we forge it.
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'};
        req = urllib2.Request(url=url, headers=headers)
        sourceCode  = urllib2.urlopen(req).read()
    except Exception, e:
        aeLock.acquire()
        aeURLs.append(url)
        aeLock.release()
    else:
        fileName = "./tempDir/" + url.replace("/", "-")
        with open(fileName, "w") as f:
            f.write(sourceCode)


def main():
    """
    Monitor URLs
    """
    threadingNum = threading.Semaphore(THREADS_NUM)
    threads = []
    urlCount = 0
    # monitor each url in .urls file
    f = open("./urls")
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

if __name__ == '__main__':
    main()

