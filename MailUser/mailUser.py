#!/usr/bin/python2.7
# FileName: MailUser.py
# Author: lxw
# Date: 2015-06-10

class MailUser(object):
    def __init__(self, mailServer, name, password):
        self.username = name
        self.password = password
        self.mailServer = mailServer
    def getMailServer(self):
        return self.mailServer
    def getUserName(self):
        return self.username
    def getPassword(self):
        return self.password
    def setMailServer(self, password):
        self.password = password
    def setUserName(self, name):
        self.username = name
    def setPassword(self, password):
        self.password = password

def main():
    pass

if __name__ == '__main__':
    main()
else:
    pass
