#!/usr/bin/python2.7
#!/usr/bin/python2.7
# FileName: recipient.py
# Author: lxw
# Date: 2015-06-11

class Recipient(object):
    def __init__(self, recipient, carbonCopy, blindCC):
        self.recipient = recipient
        self.carbonCopy = carbonCopy
        self.blindCC = blindCC
    def getRecipient(self):
        return self.recipient
    def getCarbonCopy(self):
        return self.carbonCopy
    def getBlindCC(self):
        return self.blindCC
    def setRecipient(self, recipient):
        self.recipient = recipient
    def setCarbonCopy(self, cc):
        self.carbonCopy = cc
    def setPassword(self, blindCC):
        self.blindCC = blindCC

def main():
    pass

if __name__ == '__main__':
    main()
else:
    pass
