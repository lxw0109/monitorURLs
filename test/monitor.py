import urllib2
import threading

class MyThread(threading.Thread):
	'''
	succeed class threading.Thread
	'''
    def __init__(self, func, args):        
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
    
    def getResult(self):
        return self.res

    def run(self):
       	self.res = apply(self.func, self.args)

def monitor(url):
	'''
	monitor each url.
	'''
    try:
    	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'};
        req = urllib2.Request(url=url, headers=headers)
        sourceCode = urllib2.urlopen(url).read()
        with open("./output_" + url, "w") as f:
    		f.write(sourceCode)
    except urllib2.HTTPError:
        print e
        return            
    except Exception as e:
       	print e
       	return

def main():
	threads = []
	with open("./urls") as f:
		while 1:
			line = f.readline()
			if not line:
				break;
			mt = MyThread(monitor, (line,))
			threads.append(mt)

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()


if __name__ == '__main__':
	main()