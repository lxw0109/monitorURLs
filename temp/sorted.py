#!/usr/bin/python2.7
#File: test.py
#Author: lxw
#Time: 2015-03-21


def main():
    aList = ["-20", "+1", "-23", "-34", "+30"]
    print("aList:{0}".format(aList))
    bList = sorted(aList)
    print("bList:{0}".format(bList))


if __name__ == '__main__':
    main()
else:
    print("Being imported as a module.")

