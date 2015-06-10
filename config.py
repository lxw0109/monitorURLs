#!/usr/bin/python2.7
#coding: utf-8
#如果想有中文注释就必须得有上面的语句
# FileName: config.py
# Author: lxw
# Date: 2015-06-09

#import msvcrt
import sys
import getpass
import pickle
import base64
import myUtils
import traceback
import datetime
import urllib2
import hashlib
import time
from MyThread.myThread import MyThread
import threading
import smtplib
from email.message import Message
import difflib
import os.path

class MailUser(object):
    def __init__(self, name, password):
        self.username = name
        self.password = password
    def getUserName(self):
        return self.username
    def getPassword(self):
        return self.password
    def setUserName(self, name):
        self.username = name
    def getPassword(self, password):
        self.password = password

def getPasswdWin():
    '''
    Only for windows. import msvcrt.
    '''
    letters = []
    while 1:
        char = msvcrt.getch()
        if char in '\r\n': # 输入结束
            print ''
            break
        elif char == '\b': # 退格
            if letters:
                del letters[-1]
                sys.stdout.write('\b') # stdout删除一个星号
        else:
            letters.append(char)
            sys.stdout.write('*')

    passwd = ''.join(chars)
    return passwd


def config():
    prompt = "Please Input Your Mail Server:(such as smtp.gmail.com/smtp.cnnic.cn)"
    print prompt
    mailServer = raw_input()
    prompt = "Mail Username:"
    print prompt
    username = raw_input()
    password = getPasswd()
    if testConfig(mailServer, username, password):
        #encode
        username = base64.b64encode(username)
        password = base64.b64encode(password)
        user = MailUser(username, password)
        f = open("./.Data/user", "wb")
        pickle.dump(user, f)
        f.close()
    else:
        print "Something wrong to do with your configuration. Please run \"python config.py\" to config it again"


def getPasswd():
    passwd = getpass.getpass()
    return passwd


def testConfig(server, username, password):
    '''
    test whether the config is OK.
    '''
    return testSendEmail(server, username, password)


def testSendEmail(server, name, passwd):
    """
    Test Send Email.
    """
    myUtils.writeLog("TEST EMAIL SENDING", "", "")
    try:
        smtpServer = server
        userName = name
        password = passwd
        message = Message()
        message["Subject"] = ""
        message["From"] = ""
        message["To"] = ""
        message.set_payload("")
        message.set_charset("utf-8")
        msg = message.as_string()

        sm = smtplib.SMTP(smtpServer)
        sm.set_debuglevel(0)
        sm.ehlo()
        sm.starttls()
        sm.ehlo()
        sm.login(userName, password)

        sm.quit()
    except smtplib.SMTPAuthenticationError, sae:
        string1 = "TEST EMAIL SENDING ERROR"
        string2 = "SMTPAuthenticationError"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        myUtils.writeLog(string1, string2, string3)
        return False
    except Exception, e:
        string1 = "TEST EMAIL SENDING ERROR"
        string2 = "Other Exception"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        myUtils.writeLog(string1, string2, string3)
        return False
    else:
        string1 = "Congritulations! Configurations Succeed!"
        string2 = ""
        string3 = ""
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        print string1
        myUtils.writeLog("TEST MAIL SENDING SUCCESS", string2, string3)
        return True


def main():
    config()

if __name__ == '__main__':
    main()
else:
    print("Being imported as a module.")

