import multiprocessing as mp
import queue as queue_
from threading import Thread
import _multiprocessing as _mp
import weakref


class Queue(object):
    def __init__(self, maxsize=0, debug=False):
        if maxsize <= 0:
            # same as mp.Queue
            maxsize = _mp.SemLock.SEM_VALUE_MAX

        self.mpq = mp.Queue(maxsize=maxsize)
        self.qq = queue_.Queue(maxsize=maxsize)
        self.maxsize = maxsize
        Queue._steal_daemon(self.mpq, self.qq, self)
        self.debug = debug

    def __del__(self):
        if self.debug:
            print('del')

    def put(self, item, block=True, timeout=None):
        """
        :param item:
        :param bool block:
        :param int timeout:
        :return:
        """
        self.mpq.put(item, block, timeout)

    def put_nowait(self, item):
        self.mpq.put_nowait(item)

    def get(self, block=True, timeout=None):
        """

        :param bool block:
        :param int timeout:
        :return:
        """
        return self.qq.get(block, timeout)

    def get_nowait(self):
        return self.qq.get_nowait()

    def qsize(self):
        """
        can be 2*(maxsize), because this is the sum of qq.size and mpq.size
        """
        return self.qq.qsize() + self.mpq.qsize()

    def empty(self):
        return self.qq.empty() and self.mpq.empty()

    def full(self):
        return self.qq.full() and self.mpq.full()

    # static for not referencing "self" strongly
    # but only weakly-referencing "me"
    @staticmethod
    def _steal_daemon(srcq, dstq, me):
        sentinel = object()

        def steal(srcq, dstq, me_ref):
            while me_ref():
                # block here
                obj = srcq.get()
                if obj is sentinel:
                    break
                dstq.put(obj)
                    
                # print 'steal'
            # print 'daemon done'
        
        def stop(ref):
            # print 'stop called'
            srcq.put(sentinel)

        # when the FastMyQueue object is GCed, stop the thread
        # by the stop() callback
        me1 = weakref.ref(me, stop)
        stealer = Thread(target=steal, args=(srcq, dstq, me1,))
        stealer.daemon = True
        stealer.start()
