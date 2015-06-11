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
            prompt = "Congratulations! Email Account Configurations Finished!"
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
        prompt = "Congratulations! Email Account Configurations Finished!"
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
        sys.exit(1)
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

def testDBConnection(username, password, Host, Port):
    try:
        conn = MySQLdb.connect(host=Host, user=username, passwd=password, port=Port)
        return True
    except Exception, e:
        return False

def recordDBUser(username, password, host, port):
    mailServer = encodeStr(username)
    username = encodeStr(password)
    password = encodeStr(host)
    port = encodeStr(port)
    dbUser = DBUser(username, password, host, port)
    f = open("./.db.conf", "w")
    pickle.dump(dbUser, f)
    f.close()

def configDB():
    print "------" * 20
    print ""
    prompt = "Which host your mysql database locates?"
    prompt += "If you don't know about it or the host is localhost, just Press Enter to continue:"
    print prompt
    Host = raw_input()
    Host = Host.strip()
    if Host == "":
        Host = "localhost"
    else:
        pass

    print ""
    prompt = "Which port your mysql database uses?"
    prompt += "If you don't know about it or the port is 3306, just Press Enter to continue:"
    print prompt
    Port = raw_input()
    Port = Port.strip()
    if Port == "":
        Port = 3306
    else:
        pass

    print ""
    prompt = "Please Input the Username of Mysql:"
    print prompt
    username = raw_input()
    username = username.strip()
    if username == "":
        print "Illegal username"
        sys.exit(1)
    else:
        pass

    print ""
    prompt = "Please Input the password."
    print prompt
    password = getPasswd()
    password = password.strip()
    if password == "":
        pass
    else:
        pass
    test = testDBConnection(username, password, Host, Port)
    if test:
        print "Database connection Succeed."
        print "Initializing MySQL configuration."
        recordDBUser(username, password, Host, str(Port))
        initializeDB(username, password, Host, Port)
        waitingInfo()
        print ""
        prompt = "Congratulations! Database Configurations Finished!"
        #Use file to keep whether to use database or files.
        f = open("./dbOrFiles", "w")
        f.write("1")
        f.close()
        print prompt
        print ""
    else:
        prompt = "Database connection Failed."
        print prompt
        print ""
        f = open("./dbOrFiles", "w")
        f.write("0")
        f.close()

def initializeDB(username, password, Host, Port):
    try:
        conn = MySQLdb.connect(host=Host, user=username, passwd=password, port=Port)
        cur = conn.cursor()
        cur.execute("create database if not exists monitorURL")
        conn.select_db("monitorURL")
        sql = "drop table if exists criterion"
        cur.execute(sql)
        sql = "create table criterion "
        sql += "("
        sql += "id int not null auto_increment,"
        sql += "url varchar(1000),"
        sql += "length int,"
        sql += "md5 varchar(1000),"
        sql += "date char(1),"
        sql += "primary key(id)"
        sql += ")"
        cur.execute(sql)
        sql = "drop table if exists intermedia"
        cur.execute(sql)
        sql = "create table intermedia "
        sql += "("
        sql += "id int not null auto_increment,"
        sql += "url varchar(1000),"
        sql += "sourcecode mediumtext,"
        sql += "date char(1),"
        sql += "primary key(id)"
        sql += ")"
        cur.execute(sql)

        sql = "drop table if exists accessError"
        cur.execute(sql)
        sql = "create table accessError"
        sql += "("
        sql += "id int not null auto_increment,"
        sql += "url varchar(1000),"
        sql += "date char(1),"
        sql += "primary key(id)"
        sql += ")"
        cur.execute(sql)
        sql = "drop table if exists accessError"
        cur.execute(sql)
        sql = "drop table if exists monitorLog"
        cur.execute(sql)
        sql = "create table monitorLog"
        sql += "("
        sql += "id int not null auto_increment,"
        sql += "url varchar(1000),"
        sql += "date char(1),"
        sql += "primary key(id)"
        sql += ")"
        sql = "drop table if exists monitorLog"
        cur.execute(sql)
        sql = "drop table if exists criterion_new"
        cur.execute(sql)
        sql = "create table criterion_new "
        sql += "("
        sql += "id int not null auto_increment,"
        sql += "url varchar(1000),"
        sql += "length int,"
        sql += "md5 varchar(1000),"
        sql += "date char(1),"
        sql += "primary key(id)"
        sql += ")"
        cur.execute(sql)
        sql = "drop table if exists criterion_new"
        cur.execute(sql)
        sql = "drop table if exists intermedia_new"
        cur.execute(sql)
        sql = "create table intermedia_new"
        sql += "("
        sql += "id int not null auto_increment,"
        sql += "url varchar(1000),"
        sql += "sourcecode mediumtext,"
        sql += "date char(1),"
        sql += "primary key(id)"
        sql += ")"
        cur.execute(sql)
        sql = "drop table if exists intermedia_new"
        cur.execute(sql)
        sql = "drop table if exists accessError_new"
        cur.execute(sql)
        sql = "create table accessError_new"
        sql += "("
        sql += "id int not null auto_increment,"
        sql += "url varchar(1000),"
        sql += "date char(1),"
        sql += "primary key(id)"
        sql += ")"
        cur.execute(sql)
        sql = "drop table if exists accessError_new"
        cur.execute(sql)
        sql = "drop table if exists monitorLog_new"
        cur.execute(sql)
        sql = "create table monitorLog_new"
        sql += "("
        sql += "id int not null auto_increment,"
        sql += "url varchar(1000),"
        sql += "date char(1),"
        sql += "primary key(id)"
        sql += ")"
        sql = "drop table if exists monitorLog_new"
        cur.execute(sql)
        cur.execute(sql)
        cur.close()
        conn.close()
    except Exception, e:
        string1 = "lxw_Exception."
        string2 = "Database"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        myUtils.writeLog(string1, string2, string3)

def main():
    prompt = "Before Using this program, you should configure some options as follows:\n"
    prompt += "\t1. Add an Email Account to Send Notification Email.\n"
    prompt += "\t2. Config the MySQL database.\n"
    prompt += "If you have NOT configured 1 and 2, enter 1 please;\n"
    prompt += "If you have configured 1 and want to config 2, enter 2 please;\n"
    prompt += "If you have configured both, just press enter to exit:\n"
    print prompt
    choice = raw_input().strip()
    if choice == '':
        return
    if choice == '1':
        print "------" * 20
        print ""
        configMailServer()

    print "------" * 20
    print ""
    prompt = "We offer alternative ways to save the history data: in files or in database. "
    print prompt
    prompt = "Do you want to config the database? Y/N"
    print prompt
    choice = raw_input()
    if choice.upper() == "Y":
        configDB()
    else:
        pass

if __name__ == '__main__':
    main()
else:
    print("Being imported as a module.")
