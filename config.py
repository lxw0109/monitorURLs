#!/usr/bin/python2.7
#coding: utf-8
#如果想有中文注释就必须得有上面的语句
# FileName: config.py
# Author: lxw
# Date: 2015-06-09

#import msvcrt
import sys
import getpass

def config():
    prompt = "Please Input Your Mail Server:\n"
    mailServer = raw_input(prompt)
    #print mailServer
    prompt = "Mail Username:\n"
    username = raw_input(prompt)
    password = getPasswd()


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


def getPasswd():
    passwd = getpass.getpass()
    return passwd


def testConfig():
    '''
    test whether the config is OK.
    '''
    pass


def main():
    config()

if __name__ == '__main__':
    main()
else:
    print("Being imported as a module.")

