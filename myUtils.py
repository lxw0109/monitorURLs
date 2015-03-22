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
import os.path


fileLock = threading.RLock()
logLock = threading.RLock()

aeLock = threading.RLock()

def writeLog(tag, url, log):
    """
    Write into Error Log.
    """
    with open("./monitorLog", "a") as f:
        logLock.acquire()
        f.write("{0}: {1}\t{2}\n{3}\n".format(tag, url, time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time())), log))
        f.flush()
        logLock.release()


def writeDate(content):
    """
    Write date into Log.
    """
    with open("./monitorLog", "a") as f:
        logLock.acquire()
        f.write(content)
        f.flush()
        logLock.release()


def writeFile(url, length, md5Str):
    """
    Write into criterion File.
    """
    with open("./criterion", "a") as f:
        fileLock.acquire()
        f.write("{0},{1},{2}\n".format(url, length, md5Str))
        f.flush()
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
        toAddrs = ["lxwin@foxmail.com", "liuxiaowei@cnnic.cn"]
        #ccAddrs = ["gengguanggang@cnnic.cn", "yanzhiwei@cnnic.cn"]
        ccAddrs = ["lxwin@foxmail.com"]

        message = Message()
        message["Subject"] = subject
        message["From"] = fromAddr
        message["To"] = ";".join(toAddrs)
        #Copy to
        #message["CC"] is only for display, to send the email we must specify it in the method "SMTP.sendmail".
        message["CC"] = "gengguanggang@cnnic.cn;yanzhiwei@cnnic.cn"
        message.set_payload(content)
        message.set_charset("utf-8")
        msg = message.as_string()

        sm = smtplib.SMTP(smtpServer)
        sm.set_debuglevel(0)    #sm.set_debuglevel(1)
        sm.ehlo()
        sm.starttls()
        sm.ehlo()
        sm.login(userName, password)

        sm.sendmail(fromAddr, toAddrs+ccAddrs, msg)
        time.sleep(5)
        sm.quit()
    except Exception, e:
        #start = content.index("\n") + 2
        #end = content[start:].index("\n") + 2
        #writeLog("EMAIL SENDING ERROR", content[:end], str(e))
        writeLog("EMAIL SENDING ERROR", "", traceback.format_exc())
    else:
        writeLog("EMAIL SENDING SUCCESS", "", "")


def getEmailContent(url, length, md5Str, checkTime, urlObjDic, sourceCode, aeURLs):
    """
    Already GET THE CONTENT OF THE URL. Now to get the Email content if URL updates, or nothing if not.
    length is the new length.
    urlObjDic is the old one.
    """
    content = ""
    filename = "./Intermedia/" + url.replace("/", "_")
    #filename_new = "./Intermedia_new/" + url.replace("/", "_")
    try:
        if length < urlObjDic[url].getLength():
            #writeLog("length <(lt)", url, "")
            conList = diff2Str(filename, sourceCode)
            if conList != []:
                content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息减少(上次检测{2},本次检测{3})，具体差异如下:\n".format(url, checkTime, stdSize(urlObjDic[url].getLength()), stdSize(length))
                #content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息减少(上次检测{2},本次检测{3})，具体差异如下:\n".format(url, checkTime, getSize(filename), getSize(filename_new))
                for item in conList:
                    content += item + "\n"
                content += "\n"
        elif length > urlObjDic[url].getLength():
            #writeLog("length >(gt)", url, "")
            conList = diff2Str(filename, sourceCode)
            if conList != []:
                content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息增加(上次检测{2},本次检测{3})，具体差异如下:\n".format(url, checkTime, stdSize(urlObjDic[url].getLength()), stdSize(length))
                #content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息增加(上次检测{2},本次检测{3})，具体差异如下:\n".format(url, checkTime, getSize(filename), getSize(filename_new))
                for item in conList:
                    content += item + "\n"
                content += "\n"
        elif md5Str != urlObjDic[url].getMD5Str():
            #writeLog("md5 not equal", url, "")
            conList = diff2Str(filename, sourceCode)
            if conList != []:
                content = "URL: {0}\n检测时间: {1}\n检测结果: 检测到网站首页信息更新，具体差异如下:\n".format(url, checkTime)
                for item in conList:
                    content += item + "\n"
                content += "\n"
        #else:
        #    writeLog("equals", url, "")

    except KeyError, ke:
        content = "URL: {0}\n检测时间: {1}\n检测结果: 网站恢复访问(上次检测时网站不可访问).\n\n".format(url, checkTime)
        #This function will be invoked by multi threads, so rLLock is essential here.
        #NOTE: lxw  Does this rLLock belong to one single thread or all threads share it? If the former situation, it doesn't work for mutex.
        #I think it's the latter situation. I need to CONFIRM THIS.
        aeLock.acquire()
        writeLog("[Quite Normal, url recovery.] lxw_KeyError", url, "")
        if url in aeURLs:
            aeURLs.remove(url)
        aeLock.release()

    return content


#NO_USE
def getSize(absPath):
    """
    caculate the normal size of the specified file.
    """
    try:
        size = os.path.getsize(absPath)     # type(size): long
        ksize = size / 1000.0
        if ksize >= 1:
            res = str(ksize) + "K"
        else:
            res = str(size) + "B"
    except Exception, e:
        writeLog("lxw_error", "", traceback.format_exc())

    return res


def stdSize(length):
    """
    standardize the size of the specified file.
    """
    stdLength = length / 1000.0
    if stdLength >= 1:
        return "{0:.2f}K".format(stdLength)
    else:
        return "{0}B".format(length)


def diff2Str(filename, sourceCode):
    """
    diff the content of "filename" between the latest 2 monitorings.
    """
    try:
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

        #Both methods below are OK.
        #1:
        #d = difflib.Differ()
        #res = list(d.compare(list1, list2))
        #2:
        res = list(difflib.ndiff(list1, list2))

        resList = []

        #remove the duplicate elements in res.
        #The reason to remove the duplicates is that sometimes the same content is represented by more than one objects.
        #For example, the same piece of news is represented by both a link and a img and a text string.
        #So, In this case we don't need to notify all of these differences, we just need to pick any one of them.
        [resList.append(item) for item in res if not item in resList]

        length = len(resList)
        finList = []

        #Filter the lines that are identical and meaningless.
        for index in xrange(length):
            if resList[index].startswith(" "):      # ignore the lines that are identical.
                pass
            elif resList[index].startswith("?"):    # ignore the lines that start with "?"
                pass
            elif len(resList[index].strip()) < 1:   # delete the lines that is meaningless
                pass
            else:
                finList.append(resList[index])

        #Sort the result:
        #The content removed shows at front, content added follows behind.
        return sortList(finList)

    except IOError, e:
        writeLog("lxw_IOERROR Occurred(File not found, url revives now.)", "", traceback.format_exc())
        return []

    except Exception, e:
        writeLog("lxw_ERROR", "", traceback.format_exc())
        return []


def filter(aList):
    """
    filter aList to ignore the information that's not important.
    """
    resList = []
    try:
        for item in aList:
            index1 = item.find("title=\"")
            index3 = item.find("title='")
            if index1 > 0:  #contain
                index2 = item[index1+7:].find("\"")
                string = item[index1+7:index1+7+index2]
                if string != "":
                    resList.append(string)
            elif index3 > 0:
                index4 = item[index3+7:].find("'")
                string = item[index3+7:index3+7+index4]
                if string != "":
                    resList.append(string)
    except Exception, e:
        writeLog("lxw_filter ERROR", "", traceback.format_exc())

    return resList


def sortList(aList):
    """
    Sort the result:
    The content removed shows at front, content added follows behind.
    """
    return sorted(aList)


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

    #Clear the whole content of the 2 files.
    with open("./criterion", "w") as f:
        with open("./monitorLog", "w") as f1:
            pass

    with open("./urls") as f:
        while 1:
            url = f.readline().strip()
            if not url:
                break
            #Multiple Thread: Deal with "each url by one single thread".
            mt = MyThread(eachCriterion, (url,))
            mt.start()
            threads.append(mt)

    for thread in threads:
        thread.join()


def test():
    """
    Test each function in this file.
    """
    pass


if __name__ == '__main__':
    start = datetime.datetime.now()
    initCriterion()
    end = datetime.datetime.now()
    writeLog("Method initCriterion() finishes. Time cost: ", "", str(end-start) + " seconds.")
