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
import time

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

def encodeStr(string):
    result = base64.b64encode(string)
    return result

def okServer():
    '''
    Check whether config the Server
    '''
    eps = myUtils.getServerEmail()
    email = eps[0]
    passwd = eps[1]
    server = eps[2]
    flag = testConfigMailServer(server, email, passwd)
    if flag:
        return True
    else:
        return False

def configMailServer():
    prompt = "Before Using this program, you should config some options as follows:"
    print prompt
    print "------" * 20
    print ""
    if not okServer():
        prompt = "Please Input Your Mail Server(such as smtp.gmail.com/smtp.cnnic.cn):"
        print prompt
        mailServer = raw_input()
        print ""
        prompt = "E-Mail(such as lxw0109@gmail.com):"
        print prompt
        username = raw_input()
        password = getPasswd()
        flag = testConfigMailServer(mailServer, username, password)
        if flag:
            mailServer = encodeStr(mailServer)
            username = encodeStr(username)
            password = encodeStr(password)
            user = MailUser(mailServer, username, password)
            f = open("./.Data/user", "wb")
            pickle.dump(user, f)
            f.close()
            time.sleep(1)
            print "------" * 20
            print ""
            prompt = "Now you can config the Email Recipients, Carbon Copy and Blind Carbon Copy!"
            print prompt
            configRecipient()
            time.sleep(1)
            print ""
            prompt = "Congratulations! Recipient & Carbon Copy & Blind Carbon Copy Configurations Succeed!"
            print prompt
            time.sleep(1)
            print "------" * 20
            print ""
            prompt = "Now you can config the urls to be monitored!"
            print prompt
            configUrls()
            print "------" * 20
            print ""
            prompt = "Congratulations! All Configurations Finished!"
            print prompt
        else:
            print "Something wrong to do with your configuration. Please run \"python config.py\" to config it again"
    else:
        print "------" * 20
        print ""
        time.sleep(1)
        prompt = "Now you can config the Email Recipients, Carbon Copy and Blind Carbon Copy!"
        print prompt
        configRecipient()
        time.sleep(1)
        print ""
        prompt = "Congratulations! Recipient & Carbon Copy & Blind Carbon Copy Configurations Succeed!"
        print prompt
        time.sleep(1)
        print "------" * 20
        print ""
        prompt = "Now you can config the urls to be monitored!"
        print prompt
        configUrls()
        print "------" * 20
        print ""
        prompt = "Congratulations! All Configurations Finished!"
        print prompt

def configUrls():
    print ""
    prompt = "You can append urls to be monitored into the 'urls' file."
    print prompt
    print ""
    prompt = "Press 'Enter' to continue!"
    print prompt
    raw_input()

def configRecipient():
    prompt = "Please Input the Recipient Email Address(such as lxw.ucas@gmail.com,lxw0109@gmail.com).\n"
    prompt += "If more than one email offered, split them with a comma symbol ',' :"
    time.sleep(1)
    print ""
    print prompt
    recipient = raw_input().strip()
    if not recipient:
        print "Illegal recipient. System Exit!"
    if '@' not in recipient:
        print "Illegal Email Address. System Exit!"
        sys.exit(1)

    prompt = "Please Input the Carbon Copy Email Address(such as lxw.ucas@gmail.com,lxw0109@gmail.com).\n"
    prompt += "If more than one email offered, split them with a comma symbol ',' :\n"
    prompt += "If no Carbon Copy Email Address, just press 'Enter'."
    print ""
    print prompt
    carbonCopy = raw_input().strip()
    if not carbonCopy:
        pass
    elif '@' not in carbonCopy:
        print "Illegal Email Address. System Exit!"
        sys.exit(1)

    prompt = "Please Input the Blind Carbon Copy Email Address(such as lxw.ucas@gmail.com,lxw0109@gmail.com).\n"
    prompt += "If more than one email offered, split them with a comma symbol ',' :\n"
    prompt += "If no Carbon Copy Email Address, just press 'Enter'."
    print ""
    print prompt
    blindCarbonCopy = raw_input().strip()
    if not blindCarbonCopy:
        pass
    elif '@' not in blindCarbonCopy:
        print "Illegal Email Address. System Exit!"
        sys.exit(1)
    inReceiveFile(recipient, carbonCopy, blindCarbonCopy)

def inReceiveFile(recipient, carbonCopy, blindCarbonCopy):
    recipient = Recipient(recipient, carbonCopy, blindCarbonCopy)
    f = open("./receive.conf", "w")
    pickle.dump(recipient, f)
    f.close()

def getPasswd():
    passwd = getpass.getpass()
    return passwd

def testConfigMailServer(server, username, password):
    '''
    test whether the Mail Server config is OK.
    '''
    name = username
    passwd = password
    result = testSendEmail(server, name, passwd)
    return result

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
    configMailServer()

if __name__ == '__main__':
    main()
else:
    print("Being imported as a module.")
