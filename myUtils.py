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
THREADS_NUM = 100   # limit the number of threads

def writeLog(tag, url, log):
    """
    Write into Error Log.
    """
    with open("./monitorLog", "a") as f:
        logLock.acquire()
        f.write("{0}: {1}\t{2}\n{3}\n".format(tag, url, time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time())), log))
        #f.flush()
        logLock.release()


def writeData(content):
    """
    Write data into Log.
    """
    with open("./monitorLog", "a") as f:
        logLock.acquire()
        f.write(content)
        logLock.release()


def writeFile(url, length, md5Str):
    """
    Write into criterion File.
    """
    with open("./criterion_new", "a") as f:
        fileLock.acquire()
        f.write("{0},{1},{2}\n".format(url, length, md5Str))
        fileLock.release()


def intoFile(url, sourceCode):
    """
    record the sourceCode of the url into the specific file.
    """
    url = url.replace("/", "_")

    filename = "./test_" + url
    with open(filename, "w") as f:
        f.write(sourceCode + "\n")


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
        #toAddrs = ["chenyong@cnnic.cn", "liuxiaowei@cnnic.cn"]
        toAddrs = ["lxwin@foxmail.com", "liuxiaowei@cnnic.cn"]
        #ccAddrs = ["gengguanggang@cnnic.cn", "yanzhiwei@cnnic.cn"]
        ccAddrs = ["lxwin@foxmail.com"]

        message = Message()
        message["Subject"] = subject
        message["From"] = fromAddr
        message["To"] = ";".join(toAddrs)
        #Copy to
        #message["CC"] is only for display, to send the email we must specify it in the method "SMTP.sendmail".
        #message["CC"] = "gengguanggang@cnnic.cn;yanzhiwei@cnnic.cn"
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
        #time.sleep(5)
        sm.quit()
    except Exception, e:
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
    try:
        if length < urlObjDic[url].getLength():
            conList = diff2Str(filename, sourceCode)
            if conList != []:
                content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息减少(上次检测{2},本次检测{3})，具体差异如下:\n".format(url, checkTime, stdSize(urlObjDic[url].getLength()), stdSize(length))
                for item in conList:
                    content += item + "\n"
                content += "\n"
        elif length > urlObjDic[url].getLength():
            conList = diff2Str(filename, sourceCode)
            if conList != []:
                content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息增加(上次检测{2},本次检测{3})，具体差异如下:\n".format(url, checkTime, stdSize(urlObjDic[url].getLength()), stdSize(length))
                for item in conList:
                    content += item + "\n"
                content += "\n"
        elif md5Str != urlObjDic[url].getMD5Str():
            conList = diff2Str(filename, sourceCode)
            if conList != []:
                content = "URL: {0}\n检测时间: {1}\n检测结果: 检测到网站首页信息更新，具体差异如下:\n".format(url, checkTime)
                for item in conList:
                    content += item + "\n"
                content += "\n"

    except KeyError, ke:
        content = "URL: {0}\n检测时间: {1}\n检测结果: 网站恢复访问(上次检测时网站不可访问).\n\n".format(url, checkTime)
        writeLog("[Quite Normal, url recovery.] lxw_KeyError", url, "")
        if url in aeURLs:
            aeLock.acquire()
            aeURLs.remove(url)
            aeLock.release()

    return content


def getEmailContent_stale(url, oldUrlObj, newUrlObj):
    """
    Get the Email content if URL updates, or nothing if not.
    if length or md5 changes, then diff the source code.
    """
    content = ""
    filename = "./Intermedia/" + url.replace("/", "_")
    filenameNew = "./Intermedia_new/" + url.replace("/", "_")
    checkTime = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(time.time()))
    try:
        if newUrlObj.getLength() < oldUrlObj.getLength():
            conList = diff2Str_stale(filename, filenameNew)
            if conList != []:
                content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息减少(上次检测{2},本次检测{3})，具体差异如下:\n".format(url, checkTime, stdSize(oldUrlObj.getLength()), stdSize(newUrlObj.getLength()))
                for item in conList:
                    content += item + "\n"
                content += "\n"
        elif newUrlObj.getLength() > oldUrlObj.getLength():
            conList = diff2Str_stale(filename, filenameNew)
            if conList != []:
                content = "URL: {0}\n检测时间: {1}\n检测结果:检测到网站首页信息增加(上次检测{2},本次检测{3})，具体差异如下:\n".format(url, checkTime, stdSize(oldUrlObj.getLength()), stdSize(newUrlObj.getLength()))
                for item in conList:
                    content += item + "\n"
                content += "\n"
        elif oldUrlObj.getMD5Str() != newUrlObj.getMD5Str():
            conList = diff2Str_stale(filename, filenameNew)
            if conList != []:
                content = "URL: {0}\n检测时间: {1}\n检测结果: 检测到网站首页信息更新，具体差异如下:\n".format(url, checkTime)
                for item in conList:
                    content += item + "\n"
                content += "\n"

    except Exception, e:
        writeLog("lxw_Exception.", "", traceback.format_exc())

    return content


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

        #pick out the specific(title) elements ahead of diff.
        #list1 = pickA(list1)
        #list2 = pickA(list2)

        #Work Flow: diff -> filter -> pick -> uniq -> sort

        #Both methods below are OK.
        #1:
        #d = difflib.Differ()
        #res = list(d.compare(list1, list2))
        #2:
        diffList = list(difflib.ndiff(list1, list2))

        length = len(diffList)
        filterList = []
        #Filter the lines that are identical and meaningless.
        #Why put this code block in front of pickB()? I think pickB() cost a lot of time, so I try to reduce the work load of pickB().
        for index in xrange(length):
            if diffList[index].startswith(" "):      # ignore the lines that are identical.
                pass
            elif diffList[index].startswith("?"):    # ignore the lines that start with "?"
                pass
            elif len(diffList[index].strip()) < 2:   # delete the lines that is meaningless
                pass
            else:
                filterList.append(diffList[index])

        #filterList: only +/- exists.
        #pick out the specific(title) elements behind of diff.
        specList = pickB(filterList)

        #uniq should be always behind pick(pickA & pickB).
        #uniq:
        #remove the duplicate elements in res.
        #The reason to remove the duplicates is that sometimes the same content is represented by more than one objects.
        #For example, the same piece of news is represented by both a link and a img and a text string.
        #So, In this case we don't need to notify all of these differences, we just need to pick any one of them.
        finList = []
        [finList.append(item) for item in specList if not item in finList]

        #Sort the result:
        #The content added shows at front, content removed follows behind.
        #return sorted(finList)
        return finList

    except IOError, e:
        writeLog("lxw_IOERROR Occurred(File not found, url revives now.)", "", traceback.format_exc())
        return []

    except Exception, e:
        writeLog("lxw_ERROR", "", traceback.format_exc())
        return []


def diff2Str_stale(filename, filenameNew):
    """
    diff the content of "filename" and "filenameNew".
    """
    try:
        list1 = []
        with open(filename) as f:
            while 1:
                string = f.readline()
                if not string:
                    break
                list1.append(string.strip())

        list2 = []
        with open(filenameNew) as f:
            while 1:
                string = f.readline()
                if not string:
                    break
                list2.append(string.strip())

        #Work Flow: diff -> filter -> pick -> uniq -> sort
        diffList = list(difflib.ndiff(list1, list2))

        length = len(diffList)
        filterList = []
        #Filter the lines that are identical and meaningless.
        #Why put this code block in front of pickB()? I think pickB() cost a lot of time, so I try to reduce the work load of pickB().
        for index in xrange(length):
            if diffList[index].startswith(" "):      # ignore the lines that are identical.
                pass
            elif diffList[index].startswith("?"):    # ignore the lines that start with "?"
                pass
            elif len(diffList[index].strip()) < 2:   # delete the lines that is meaningless
                pass
            else:
                filterList.append(diffList[index])

        #filterList: only +/- exists.
        #pick out the specific(title) elements behind of diff.
        specList = pickB(filterList)

        #uniq should be always behind pick(pickA & pickB).
        #uniq:
        #remove the duplicate elements in res.
        #The reason to remove the duplicates is that sometimes the same content is represented by more than one objects.
        #For example, the same piece of news is represented by both a link and a img and a text string.
        #So, In this case we don't need to notify all of these differences, we just need to pick any one of them.
        finList = []
        [finList.append(item) for item in specList if not item in finList]

        #Sort the result:
        #The content added shows at front, content removed follows behind.
        #return sorted(finList)
        return finList

    except IOError, e:
        writeLog("lxw_IOERROR Occurred(File not found, url revives now.)", "", traceback.format_exc())
        return []

    except Exception, e:
        writeLog("lxw_ERROR", "", traceback.format_exc())
        return []


def pickA(aList):
    """
    deal with aList to ignore the information that's not important(pick out the specific elements).
    """
    resList = []
    try:
        for item in aList:
            index1 = item.find("title=\"")
            index3 = item.find("title='")
            if index1 >= 0:  #contain
                index2 = item[index1+7:].find("\"")
                if index2 != -1:
                    string = item[index1+7:index1+7+index2].strip()
                    if string != "":
                        resList.append(string)
            elif index3 >= 0:
                index4 = item[index3+7:].find("'")
                if index4 != -1:
                    string = item[index3+7:index3+7+index4].strip()
                    if string != "":
                        resList.append(string)
    except Exception, e:
        writeLog("lxw_pickA ERROR", "", traceback.format_exc())

    return resList


def pickB(aList):
    """
    deal with aList to ignore the information that's not important(pick out the specific elements).
    NOTE: the differences between pickA() and pickB() is that elements in pickB all start with +/-.
    """
    resList = []
    try:
        for item in aList:
            if item[0] != "-" and item[0] != "+":
                writeLog("lxw_NOTE: this should not happen.", item, "all should begin with +/-")
                continue

            index1 = item.find("title=\"")
            index3 = item.find("title='")
            if index1 >= 0:  #contain
                index2 = item[index1+7:].find("\"")
                if index2 != -1:
                    string = item[index1+7:index1+7+index2].strip()
                    if string != "":
                        resList.append(item[0] + string)
            elif index3 >= 0:
                index4 = item[index3+7:].find("'")
                if index4 != -1:
                    string = item[index3+7:index3+7+index4].strip()
                    if string != "":
                        resList.append(item[0] + string)
    except Exception, e:
        writeLog("lxw_pickB ERROR", "", traceback.format_exc())

    return resList


def eachCriterion(url):
    """
    Create the criterion file. File format: url,length,md5.
    """
    sourceCode = ""
    try:
        sourceCode = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        try:
            #NOTE: some websites do not allow us to access them by this method, they check the userAgent information, so we forge it.
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'};
            req = urllib2.Request(url=url, headers=headers)
            sourceCode  = urllib2.urlopen(req).read()
        except Exception, e:
            writeLog("Access Error", url, traceback.format_exc())
        else:
            length, md5Str = getLengthMd5(sourceCode)
            writeFile(url, length, md5Str)

    except Exception, e:
        writeLog("Access Error", url, traceback.format_exc())
    else:
        length, md5Str = getLengthMd5(sourceCode)
        writeFile(url, length, md5Str)

    return sourceCode


def recordInFile(url, sourceCode):
    """
    record the sourceCode of the url into the specific file.
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
    threadingNum = threading.Semaphore(THREADS_NUM)
    threads = []
    with open("./urls") as f:
        while 1:
            url = f.readline().strip()
            if not url:
                break
            #Multiple Thread: Deal with "each url by one single thread".
            mt = MyThread(eachCriterion, (url,), threadingNum)
            #mt.start()
            threads.append(mt)

    for thread in threads:
        thread.start()

    while 1:
        over = True
        for thread in threads:
            if thread.isAlive():
                if not thread.isTimedOut():     # not "Timed Out".
                    over = False
                else:
                    myUtils.writeLog("lxw_Timed Out", thread.getURL(), "")
        if over:
            break


def test():
    """
    Test each function in this file.
    """
    writeLog("test myUtils.py----------------------------0", "START", "")
    #writeLog()
    writeLog("writeLog() to monitorLog-------------------1", "", "")
    #writeData()
    writeData("writeData() to monitorLog------------------2\n")
    #writeFile()
    writeFile("writeFile() to criterion-------------------3\nurl", "length", "md5")
    #sendEmail()
    sendEmail("sendEmail() to lxwin@foxmail.com-----------4", "test-sendEmail_4")
    sendEmail("sendEmail() to lxwin@foxmail.com.a\nb\nc---5", "test-sendEmail_5")
    #stdSize()
    writeData("stdSize(210913): {0}. to monitorLog.-------6\n".format(stdSize(210913)))
    #getLengthMd5()
    writeData("getLengthMd5(): {0}. to monitorLog.----------7\n".format(getLengthMd5("Hello, this is a test.")))
    #pickA()
    aList = ["title=\"0 \"", "<>meaningless<>information<> title=\"1 \"", "title=", "title=' 2 '", "title", "test str"]
    writeData("pickA(): {0}. to monitorLog.---------------8\n".format(pickA(aList)))
    #pickB()
    aList = ["-title=\"0 \"", "-<>meaningless<>information<> title=\"1 \"", "title=\"0\"", "+title=' 2 '", "-title", "+test str"]
    writeData("pickB(): {0}. to monitorLog.---------------9\n".format(pickB(aList)))
    #eachCriterion() to criterion
    urls = ["baidu.com", "www.baidu.com", "http://www.baidu.com", "https://www.baidu.com"]
    for url in urls:
        intoFile(url, eachCriterion(url))
    #initCriterion()
    initCriterion()
    #getEmailContent()  # test alone
    #diff2Str() # test alone
    #recordInFile() #test alone
    writeLog("test myUtils.py---------------------------10", "FINISHED", "")


if __name__ == '__main__':
    start = datetime.datetime.now()
    initCriterion()
    end = datetime.datetime.now()
    writeLog("Method initCriterion() finishes. Time cost: ", "", str(end-start) + " seconds.")
