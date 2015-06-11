#!/usr/bin/python2.7
#!/usr/bin/python2.7
# FileName: initialize.py
# Author: lxw
# Date: 2015-06-11

import myUtils
import traceback

def main():
    try:
        f = open("./dbOrFiles")
        while 1:
            line = f.readline()
            if not line:
                break
            dbFlag = False
            if "0" not in line:
                if "1" not in line:
                    dbFlag = False
                else:
                    dbFlag = True
            else:
                dbFlag = False
    except Exception, e:
        string1 = "lxw_No such file."
        string2 = "./dbOrFiles"
        string3 = traceback.format_exc()
        string4 = "\n" + "------"*13 + "\n"
        string3 += string4
        myUtils.writeLog(string1, string2, string3)

    myUtils.dealUrls()
    myUtils.initCriterion()

if __name__ == '__main__':
    main()
else:
    string = "Being imported as a module."
    print string
