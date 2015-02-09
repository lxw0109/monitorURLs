#!/usr/bin/python2.7
#File: getCriterion.py
#Author: lxw
#Time: 2015-02-07
#Usage: Collect the criterion data that we will use to compare with.

import datetime
import urllib2
import md5
import time
from MyThread.myThread import MyThread
import threading

myLock = threading.RLock()

def writeLog(url, log):
    """
    Write into Error Log.
    """
    with open("./monitorLog", "a") as f:
        myLock.acquire()
        f.write("Error: {0}\t{1}\n{2}\n\n".format(url, time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time())), log))
        myLock.release()


def writeFile(url, length, md5Str):
    """
    Write into criterion File.
    """
    with open("./criterion", "a") as f:
        myLock.acquire()
        f.write("{0},{1},{2}\n".format(url, length, md5Str))
        myLock.release()


#Create the criterion file. File format: url,length,md5.
def getCriterion(url):
    try:
        sourceCode  = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        try:
            #NOTE: some websites do not allow us to access them by this method, they check the userAgent information, so we forge it.
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'};
            req = urllib2.Request(url=url, headers=headers)
            sourceCode  = urllib2.urlopen(req).read()
        except Exception, e:
            writeLog(url, str(e))
        else:
            length = len(sourceCode)
            #calculate the md5 value of sourceCode string.(32bits).
            md = md5.new()
            md.update(sourceCode)
            md5Str = md.hexdigest()
            writeFile(url, str(length), md5Str)

    except Exception, e:
        writeLog(url, str(e))
    else:
        length = len(sourceCode)
        #calculate the md5 value of sourceCode string.(32bits).
        md = md5.new()
        md.update(sourceCode)
        md5Str = md.hexdigest()
        writeFile(url, str(length), md5Str)


def main():
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
            mt = MyThread(getCriterion, (url,))
            mt.start()
            threads.append(mt)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print(end - start)
else:
    print("Being imported as a module.")
