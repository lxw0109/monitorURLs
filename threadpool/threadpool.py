# ThreadPool is a simple thread pool
#
# Copyright (C) 2012 Yummy Bian <yummy.bian#gmail.com>
#
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ThreadPool is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.";
#

import sys
import Queue
#import queue
import threading

#"The Queue class in queue module implements all the required locking semantics.", so queue.Queue class is thread-safe?

#KEY: Queue.get() and Queue.put() block until resource(an item/a slot) is available.

class Worker(threading.Thread):
    """
    Routines for work thread.
    """
    def __init__(self, in_queue, out_queue, err_queue):
        """
        Initialize and launch a work thread,
        in_queue which tasks in it waiting for processing,
        out_queue which the return value of the task in it,
        err_queue which stores error info when processing the task.
        """
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.in_queue = in_queue    #4-tuple: (command, callback, args, kwds)
        self.out_queue = out_queue  #2-tuple or 3-tuple, etc. Determined by the type of return value of callback.
        self.err_queue = err_queue  #2-tuple
        #Start the thread once it is created.
        self.start()

    def run(self):
        #while True:
        while 1:
            # Processing tasks in the in_queue until command is "stop".
            # Similar to 360 interview: "args" and "kwds" can be assigned correctly. TODO: Prove this.
            command, callback, args, kwds = self.in_queue.get()
            if command == "stop":
                break
            try:
                if command != "process":
                    raise ValueError("Unknown command %r" % command)
            except:
                self.report_error()
            else:
                self.out_queue.put(callback(*args, **kwds))

    def dismiss(self):
        command = "stop"
        self.in_queue.put((command, None, None, None))

    def report_error(self):
        """'''
        We "report" errors by adding error information to err_queue.
        """
        self.err_queue.put(sys.exc_info()[:2])


class ThreadPool():
    """
    Manager thread pool.
    """
    MAX_THREADS = 32

    def __init__(self, num_threads, pool_size=0):
        """
        Spawn num_threads threads in the thread pool,
        and initialize three queues.
        """
        # pool_size = 0 indicates buffer is unlimited.
        num_threads = ThreadPool.MAX_THREADS \
            if num_threads > ThreadPool.MAX_THREADS \
            else num_threads
        self.in_queue = Queue.Queue(pool_size)
        self.out_queue = Queue.Queue(pool_size)
        self.err_queue = Queue.Queue(pool_size)
        """
        self.in_queue = queue.Queue(pool_size)  # queue.Queue(maxsize=0)  If maxsize is less than or equal to zero, the queue size is infinite.
        self.out_queue = queue.Queue(pool_size)
        self.err_queue = queue.Queue(pool_size)
        """
        self.workers = {}
        for i in range(num_threads):
            worker = Worker(self.in_queue, self.out_queue, self.err_queue)
            self.workers[i] = worker

    def add_task(self, callback, *args, **kwds):
        command = 'process'
        self.in_queue.put((command, callback, args, kwds))

    def get_task(self):
        return self.out_queue.get()

    def _get_results(self, queue):
        """
        Generator to yield one after the others all items currently
        in the queue, without any waiting
        """
        try:
            #while True:
            while 1:
                yield queue.get_nowait()
        #except queue.Empty:
        except Queue.Empty:
            raise StopIteration

    def show_results(self):
        for result in self._get_results(self.out_queue):
            print 'Result:', result
            #print('Result: {0}'.format(result))

    def show_errors(self):
        for etyp, err in self._get_results(self.err_queue):
            print 'Error:', etyp, err
            #print('Error: {0} {1}'.format(etyp, err))

    def destroy(self):
        # order is important: first, request all threads to stop...:
        for i in self.workers:
            self.workers[i].dismiss()
        # ...then, wait for each of them to terminate:
        for i in self.workers:
            self.workers[i].join(30)
        # clean up the workers from now-unused thread objects
        del self.workers
