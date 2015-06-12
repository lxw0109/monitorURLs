#!/usr/bin/python2.7
# FileName: MailUser.py
# Author: lxw
# Date: 2015-06-10

class DBUser(object):
    def __init__(self, name, password, host, port):
        self.username = name
        self.password = password
        self.host = host
        self.port = port
    def getUserName(self):
        return self.username
    def getPassword(self):
        return self.password
    def getHost(self):
        return self.host
    def getPort(self):
        return str(self.port)
    def setUserName(self, name):
        self.username = name
    def setPassword(self, password):
        self.password = password
    def setHost(self, host):
        self.host = host
    def setPort(self, port):
        self.port = str(port)

def main():
    pass

if __name__ == '__main__':
    main()
else:
    pass
