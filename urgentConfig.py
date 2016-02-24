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
import hashlib
import smtplib
from email.message import Message
from MailUser.mailUser import MailUser
from MailUser.recipient import Recipient
from DBUser.dbUser import DBUser
import time
import MySQLdb
import warnings

def configRecipient():
    try:
        prompt = "Please Input the Recipient Email Address"
        prompt += "(such as lxw.ucas@gmail.com,lxw0109@gmail.com).\n"
        prompt += "If more than one email offered, split them with a comma symbol ',' :"
        time.sleep(1)
        print ""
        print prompt
        recipient = raw_input().strip()
        if not recipient:
            prompt = "Illegal recipient. System Exit!"
            print prompt
            sys.exit(1)
        if '@' not in recipient:
            prompt = "Illegal Email Address. System Exit!"
            print prompt
            sys.exit(1)

        prompt = "Please Input the Carbon Copy Email Address"
        prompt += "(such as lxw.ucas@gmail.com,lxw0109@gmail.com).\n"
        prompt += "If more than one email offered, split them with a comma symbol ',' :\n"
        prompt += "If no Carbon Copy Email Address, just press 'Enter'."
        print ""
        print prompt
        carbonCopy = raw_input()
        carbonCopy = carbonCopy.strip()
        if not carbonCopy:
            pass
        elif '@' not in carbonCopy:
            prompt = "Illegal Email Address. System Exit!"
            print prompt
            sys.exit(1)

        prompt = "Please Input the Blind Carbon Copy Email Address"
        prompt += "(such as lxw.ucas@gmail.com,lxw0109@gmail.com).\n"
        prompt += "If more than one email offered, split them with a comma symbol ',' :\n"
        prompt += "If no Carbon Copy Email Address, just press 'Enter'."
        print ""
        print prompt
        blindCarbonCopy = raw_input()
        blindCarbonCopy = blindCarbonCopy.strip()
        if not blindCarbonCopy:
            pass
        elif '@' not in blindCarbonCopy:
            prompt = "Illegal Email Address. System Exit!"
            print prompt
            sys.exit(1)
        inReceiveFile(recipient, carbonCopy, blindCarbonCopy)
    except Exception, e:
        string1 = "Exception"
        string2 = "Recipient Configuration Error"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        myUtils.writeLog(string1, string2, string3)
def inReceiveFile(recipient, carbonCopy, blindCarbonCopy):
    try:
        recipient = Recipient(recipient, carbonCopy, blindCarbonCopy)
        f = open("./urgentReceive.conf", "w")
        pickle.dump(recipient, f)
        f.close()
    except Exception, e:
        string1 = "Exception"
        string2 = "Pickle Error"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        myUtils.writeLog(string1, string2, string3)

def waitingInfo():
    interval = 0.5
    times = 3
    char = "."
    for i in xrange(times):
        time.sleep(interval)
        sys.stdout.write(char)
        sys.stdout.flush()

    char = " "
    time.sleep(interval)
    sys.stdout.write(char)
    sys.stdout.flush()

    times = 3
    char = "."
    for i in xrange(times):
        time.sleep(interval)
        sys.stdout.write(char)
        sys.stdout.flush()

def testSendEmail(server, name, passwd):
    """
    Test Send Email.
    """
    myUtils.writeLog("TEST EMAIL SENDING", "", "")
    try:
        #print name, passwd, server
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
        print "Checking Email Server Configuration "
        waitingInfo()
        print ""
        print ""
        string1 = "TEST EMAIL SENDING ERROR"
        string2 = "SMTPAuthenticationError"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        myUtils.writeLog(string1, string2, string3)
        return False
    except Exception, e:
        print "Checking Email Server Configuration "
        waitingInfo()
        print ""
        print ""
        string1 = "TEST EMAIL SENDING ERROR"
        string2 = "Other Exception"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        myUtils.writeLog(string1, string2, string3)
        return False
    else:
        print "Checking Email Server Configuration "
        waitingInfo()
        print ""
        print ""
        string1 = "Congratulations! Configurations Succeed!"
        string2 = ""
        string3 = ""
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        string5 = "TEST MAIL SENDING SUCCESS"
        print string1
        myUtils.writeLog(string5, string2, string3)
        return True

def main():
    try:
        prompt = "Config the receipient:\n"
        print prompt
        configRecipient()
    except Exception, e:
        string1 = "Exception"
        string2 = "in urgentConfig.py main()"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        myUtils.writeLog(string1, string2, string3)


if __name__ == '__main__':
    main()
else:
    string = "Being imported as a module."
    print string
