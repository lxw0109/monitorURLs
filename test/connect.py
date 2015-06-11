#!/usr/bin/python2.7
#!/usr/bin/python2.7
# FileName: connect.py
# Author: lxw
# Date: 2015-06-11

import MySQLdb

def main():
    try:
        conn = MySQLdb.connect(host="localhost", user="root", passwd="lxw", db="monitorURL", port=3306, charset="utf8")
    except Exception, e:
        print e

if __name__ == '__main__':
    main()
else:
    print("Being imported as a module.")

