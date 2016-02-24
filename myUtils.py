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
import pickle
import sys
import base64
from MailUser.mailUser import MailUser
import MySQLdb
from DBUser.dbUser import DBUser
import random
import os
import fileinput
import socket
from time import sleep
from pyquery import PyQuery
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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

def dealUrls():
    f = open("./urls")
    f1 = open("./.urls", "w")
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if '.' not in line:
            continue
        elif 'http' not in line:
            line = "http://" + line
        f1.write(line + "\n")
    f.close()
    f1.close()

def intoFile(url, sourceCode):
    """
    record the sourceCode of the url into the specific file.
    """
    url = url.replace("/", "_")

    filename = "./test_" + url
    f = open(filename, "w")
    f.write(sourceCode + "\n")
    f.close()

def decode(string):
    result = base64.b64decode(string)
    return result

def calculateLines(directory):
    count = 0
    for dirPath, dirNames, fileNames in os.walk(directory):
        for fileName in fileNames:
            try:
                with open(dirPath+os.sep+fileName) as f:
                    while 1:
                        string = f.readline()
                        if not string:
                            break
                        count += 1
            except Exception, e:
                print("---------Exception-----:\n\t" + e)


    if directory == ".":
        print("The number of lines in all files in current direcotry is {0}!".format(count))
    else:
        print("The number of lines in all files in direcotry \"{0}\" is {1}!".format(directory, count))

def getServerEmail():
    try:
        f = open("./.Data/user")
        user = pickle.load(f)
        email = user.getUserName()
        passwd = user.getPassword()
        server = user.getMailServer()
        email = decode(email)
        passwd = decode(passwd)
        server = decode(server)
        email = email.strip()
        passwd = passwd.strip()
        server = server.strip()
        f.close()
        return email, passwd, server
    except Exception, e:
        string1 = "lxw_Exception."
        string2 = ".Data/user pickle Error"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        writeLog(string1, string2, string3)
        return "", "", ""

def getRCB():
    '''
    Format
    Recipient:lxw.ucas@gmail.com,lxw0109@gmail.com
    Carbon Copy:lxw.ucas@gmail.com,lxw0109@gmail.com
    Blind Carbon Copy:lxw.ucas@gmail.com,lxw0109@gmail.com
    '''
    f = open("./receive.conf")
    receive = pickle.load(f)
    recipient = receive.getRecipient()
    carbonCopy = receive.getCarbonCopy()
    blindCC = receive.getBlindCC()
    f.close()
    return recipient, carbonCopy, blindCC

def splitStr(string, sep):
    aList = string.split(sep)
    length = len(aList)
    for i in xrange(length):
        string = aList[i]
        string = string.strip()
        aList[i] = string
    return aList

def filterList(aList):
    length = len(aList)
    i = 0
    while i < len(aList):
        if aList[i] == "":
            del aList[i]
        else:
            i += 1
    return aList

def getDBUser():
    try:
        f = open("./.db.conf")
        user = pickle.load(f)
        username = user.getUserName()
        passwd = user.getPassword()
        host = user.getHost()
        port = user.getPort()
        username = decode(username)
        passwd = decode(passwd)
        host = decode(host)
        port = decode(port)
        username = username.strip()
        passwd = passwd.strip()
        host= host.strip()
        port = port.strip()
        f.close()
        return username, passwd, host, port
    except Exception, e:
        string1 = "lxw_Exception."
        string2 = ".db.conf pickle Error"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        writeLog(string1, string2, string3)
        return "", "", "", ""

def updateCriterion(dic):
    '''
    dic -> newUrlObjDic[url] = URL(length, md5Str)
    dic[url] = URL(length, md5Str)
    '''
    try:
        uphp = getDBUser()
        username = uphp[0]
        passwd = uphp[1]
        host = uphp[2]
        port = uphp[3]
        password = passwd
        Host = host
        Port = int(port)
        print "type(username): {0}, username:{1}".format(type(username), username)
        print "type(passwd): {0}, passwd:{1}".format(type(passwd), passwd)
        print "type(Host): {0}, Host:{1}".format(type(Host), Host)
        print "type(Port): {0}, Port:{1}".format(type(Port), Port)
        conn = MySQLdb.connect(host=Host, user=username, passwd=password, port=Port)
        conn.select_db('monitorURL')
        cur = conn.cursor()
        values = []
        for key in dic.keys():
            length = dic[key].getLength()
            md5Str = dic[key].getMD5Str()
            values.append((key, length, md5Str, "1"))
        length = len(values)
        if False:
            for i in xrange(length):
                print i, length, values[i][2], values[i][0]
                sql = "insert into `criterion` values(url='%s',length=%s,md5='%s',date='%s')"
                cur.execute(sql, values[i])
        cur.close()
        conn.close()
    except Exception, e:
        string1 = "DB_Exception."
        string2 = "criterion"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        writeLog(string1, string2, string3)
    else:
        string1 = "OK."
        string2 = "update criterion table in the database"
        string3 = ""
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        writeLog(string1, string2, string3)

def updateIntermedia(url, sourcecode):
    try:
        uphp = getDBUser()
        username = uphp[0]
        passwd = uphp[1]
        host = uphp[2]
        port = uphp[3]
        password = passwd
        Host = host
        Port = int(port)
        print "type(username): {0}, username:{1}".format(type(username), username)
        print "type(passwd): {0}, passwd:{1}".format(type(passwd), passwd)
        print "type(Host): {0}, Host:{1}".format(type(Host), Host)
        print "type(Port): {0}, Port:{1}".format(type(Port), Port)
        conn = MySQLdb.connect(host=Host, user=username, passwd=password, port=Port)
        conn.select_db('monitorURL')
        cur = conn.cursor()
        values = []
        values.append((url, sourcecode, "1"))
        length = len(values)
        if False:
            for i in xrange(length):
                print i, length, values[i][1], values[i][0]
                sql = "insert into `intermedia` values(url='%s', sourcecode='%s', date='%s')"
                cur.execute(sql, values[i])
        cur.close()
        conn.close()
    except Exception, e:
        string1 = "DB_Exception."
        string2 = "Intermedia"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        writeLog(string1, string2, string3)
    else:
        string1 = "OK."
        string2 = "update intermedia table in the database"
        string3 = ""
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        writeLog(string1, string2, string3)

def sendEmail(subject, content):
    """
    Send Email.
    """
    writeLog("EMAIL SENDING", "", "")
    try:
        eps = getServerEmail()
        email = eps[0]
        passwd = eps[1]
        server = eps[2]
        smtpServer = server
        userName = email
        password = passwd
        rcb = getRCB()
        recipient = rcb[0]
        carbonCopy = rcb[1]
        blindCC = rcb[2]
        rList = splitStr(recipient, ",")
        cList = splitStr(carbonCopy, ",")
        bList = splitStr(blindCC, ",")
        rList = filterList(rList)
        cList = filterList(cList)
        bList = filterList(bList)

        fromAddr = email
        toAddrs = rList #["lxwin@foxmail.com", "wangcuicui@cnnic.cn"]
        ccAddrs = cList #["lxwin@foxmail.com"]
        bccAddrs = bList

        message = Message()
        message["Subject"] = subject
        message["From"] = fromAddr
        message["To"] = ";".join(toAddrs)
        #Copy to
        #message["CC"] is only for display, to send the email we must specify it in the method "SMTP.sendmail".
        #message["CC"] = "gengguanggang@cnnic.cn;yanzhiwei@cnnic.cn"
        message["CC"] = ";".join(ccAddrs)
        message.set_payload(content)
        message.set_charset("utf-8")
        msg = message.as_string()

        sm = smtplib.SMTP(smtpServer)
        sm.set_debuglevel(0)    #sm.set_debuglevel(1)
        sm.ehlo()
        sm.starttls()
        sm.ehlo()
        sm.login(userName, password)

        sm.sendmail(fromAddr, toAddrs+ccAddrs+bccAddrs, msg)
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
        content = "URL: {0}\n检测时间: {1}\n检测结果: 网站恢复访问(上次检测时网站不可访问).\n".format(url, checkTime)
        #update & add: 2015.9.8
        writeLog("Information: URL recovery. lxw_KeyError", url, "")
        conList = diff2Str(filename, sourceCode)
        if conList != []:
            content += "检测到网站首页信息更新，具体差异如下:\n"
            for item in conList:
                content += item + "\n"
            content += "\n"
        else:
            content += "网站首页无信息更新.\n\n"

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
    except KeyError, ke:
        content = "URL: {0}\n检测时间: {1}\n检测结果: 网站恢复访问(上次检测时网站不可访问).\n".format(url, checkTime)
        #update & add: 2015.9.8
        writeLog("Information: URL recovery. lxw_KeyError", url, "")
        conList = diff2Str_stale(filename, filenameNew)
        if conList != []:
            content += "检测到网站首页信息更新，具体差异如下:\n"
            for item in conList:
                content += item + "\n"
            content += "\n"
        else:
            content += "网站首页无信息更新.\n\n"

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
        writeLog(string1, string2, string3)

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

        pq1 = PyQuery("".join(list1))
        pq2 = PyQuery("".join(list2))

        list1 = []
        list2 = []
        for data in pq1.find("a"):
            list1.append(PyQuery(data).text())
        for data in pq1.find("title"):
            list1.append(PyQuery(data).text())
        for data in pq2.find("a"):
            list2.append(PyQuery(data).text())
        for data in pq2.find("title"):
            list2.append(PyQuery(data).text())

        #pick out the specific(title) elements ahead of diff.
        #list1 = pickA(list1)
        #list2 = pickA(list2)

        #Work Flow: diff   ->   filter   ->   pick   ->   uniq   ->   sort
        #diff: do the diff among 2 sourceCode.
        #filter: only keep the different information(lines start with +/-).
        #pick: pick out the content of specific labels(e.g. title/div).
        #uniq: remove the duplicate content.
        #sort: keep lines begin with "+" at the front of lines begin with "-".

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
            elif diffList[index].startswith("-"):
                pass
            else:
                filterList.append(diffList[index])

        #filterList: only +/- exists.
        #pick out the specific(title) elements behind of diff.
        #specList = pickB(filterList)

        #uniq should be always behind pick(pickA & pickB).
        #uniq:
        #remove the duplicate elements in res.
        #The reason to remove the duplicates is that sometimes the same content is represented by more than one objects.
        #For example, the same piece of news is represented by both a link and a img and a text string.
        #So, In this case we don't need to notify all of these differences, we just need to pick any one of them.
        finList = []
        #[finList.append(item) for item in specList if not item in finList]
        [finList.append(item) for item in filterList if not item in finList]

        #solve the "specific labels unchange problem"
        finList = pickFilter(finList[:])

        #filter the meaningless lines
        length = len(finList)
        del(filterList)
        filterList = []
        [filterList.append(item) for item in finList if len(item) > 7 ]

        #2016.2.18 Remove content of old information.
        filterList = contentFilter(filterList)

        return filterList

    except IOError, e:
        writeLog("lxw_IOERROR Occurred(File not found, url revives now.)", "", traceback.format_exc())
        return []

    except Exception, e:
        writeLog("lxw_ERROR", "", traceback.format_exc())
        return []

def contentFilter(aList):
    """
    Deal with "Content Filter" in contentFilter().
    Content Filters:
    1. CVE-2013-????:*  Remove the vulnerabilities before 2015.
    2.
    """
    retList = []
    for item in aList:
        if item[2:8] == 'CVE-20':
            if int(item[8:10]) > 14:
                retList.append(item)
    return retList


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

        pq1 = PyQuery("".join(list1))
        pq2 = PyQuery("".join(list2))

        list1 = []
        list2 = []
        for data in pq1.find("a"):
            list1.append(PyQuery(data).text())
        for data in pq1.find("title"):
            list1.append(PyQuery(data).text())
        for data in pq2.find("a"):
            list2.append(PyQuery(data).text())
        for data in pq2.find("title"):
            list2.append(PyQuery(data).text())

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
        #specList = pickB(filterList)

        #uniq should be always behind pick(pickA & pickB).
        #uniq:
        #remove the duplicate elements in res.
        #The reason to remove the duplicates is that sometimes the same content is represented by more than one objects.
        #For example, the same piece of news is represented by both a link and a img and a text string.
        #So, In this case we don't need to notify all of these differences, we just need to pick any one of them.
        finList = []
        [finList.append(item) for item in filterList if not item in finList]

        #solve the "specific labels unchange problem"
        finList = pickFilter(finList[:])

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

def diff2StrSwitch(filename, sourceCode):
    """
    NO_USE
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

        list1 = pickA(list1)
        list2 = pickA(list2)

        d = difflib.Differ()
        res = list(d.compare(list1, list2))
        diffList = list(difflib.ndiff(list1, list2))

        length = len(diffList)
        filterList = []
        for index in xrange(length):
            if diffList[index].startswith(" "):      # ignore the lines that are identical.
                pass
            elif diffList[index].startswith("?"):    # ignore the lines that start with "?"
                pass
            elif len(diffList[index].strip()) < 2:   # delete the lines that is meaningless
                pass
            else:
                filterList.append(diffList[index])

        specList = pickB(filterList)

        finList = []
        [finList.append(item) for item in specList if not item in finList]

        finList = pickFilter(finList[:])

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

            #"title" field
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
            '''
            #NO
            #"a href" field
            index1 = item.find("a href=\"")
            index3 = item.find("a href='")
            '''

    except Exception, e:
        writeLog("lxw_pickB ERROR", "", traceback.format_exc())

    return resList


def pickFilter(aList):
    """
    NOTE: no sort method allowed between diff() and pickFilter().

    After pick the specific labels in the result, a problems exists(let's call it "specific labels unchange problem"):
    SourceCode:          Old             New        (Assuming that "A" is the specific labels.)
                        abcA             bcA
    we got the following result:
    -abcA
    +bcA
    after pick():
    -A
    +A
    The result seems confusing.

    This method is to solve the problem mentioned above.
    """

    length = len(aList)
    pickFilList = []
    index = 0
    while index < length:
        if aList[index][0] == "-":
            lineM = aList[index]    #line begins with "-"(Minus)
            content1 = lineM[1:]
            index += 1
            if index == length:
                pickFilList.append(lineM)
                break
            if aList[index][0] == "+":
                lineA = aList[index]    #line begins with "+"(Add)
                content2 = lineA[1:]
                if content1 != content2:
                    pickFilList.append(lineM)
                    pickFilList.append(lineA)
        #lxw 2015.12.19
        #The following line is essential.
        else:   #line begins with "+"
            pickFilList.append(aList[index])
        index += 1

    return pickFilList


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

#add: 2015.9.8
def cpFile(url):
    """
    copy the url file from the ./Intermedia into ./Intermedia_new
    This function is called when Access Error Occurred(no files in the ./Intermedia_new), the old version of the url sourcecode MUST be saved.
    """
    #writeLog("call cpFile()", "", "\n")
    url = url.replace("/", "_")

    filename1 = "./Intermedia/" + url
    filename2 = "./Intermedia_new/" + url
    try:
        with open(filename1, "r") as f1:
            with open(filename2, "w") as f2:
                while 1:
                    line = f1.readline()
                    if not line:
                        break
                    f2.write(line)
    except IOError as ioe:
        writeLog("lxw_IOError", "", str(ioe))

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
    with open("./.urls") as f:
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
    '''
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
    getServerEmail()
    getRCB()
    '''
    #database()
    pass


if __name__ == '__main__':
    start = datetime.datetime.now()
    #initCriterion()
    test()
    end = datetime.datetime.now()
    writeLog("myUtils.py finishes. Time cost: ", str(end-start) + " seconds.", "")
