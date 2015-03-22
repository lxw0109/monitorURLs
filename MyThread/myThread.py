#!/usr/bin/python2.7
#File: myThread.py
#Author: lxw
#Time: 2014-09-06

import threading
#from time import ctime
import datetime

class MyThread(threading.Thread):
    def __init__(self, func, args, name=""):
        """
        if the subclass overrides the constructor, it must make sure to
        invoke the base class constructor (Thread.__init__()) before
        doing anything else to the thread.
        """
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name
        self.startTime = datetime.datetime.now()


    def isTimedOut(self):
        """
        Judge whether the current thread timed out or not.
        """
        now = datetime.datetime.now()
        deltaTime = (now - self.startTime).seconds
        if deltaTime > 20:
            return True
        else:
            return False


    def getResult(self):
        return self.res


    def run(self):
        self.startTime = datetime.datetime.now()
        self.res = apply(self.func, self.args)
