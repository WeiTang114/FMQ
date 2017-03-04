import multiprocessing as mp
import Queue as Queue_
from threading import Thread
import _multiprocessing as _mp
import weakref

class Queue():
    def __init__(self, maxsize=0, debug=False):
        if maxsize <= 0:
            # same as mp.Queue
            maxsize = _mp.SemLock.SEM_VALUE_MAX

        self.mpq = mp.Queue(maxsize=maxsize)
        self.qq = Queue_.Queue(maxsize=maxsize)
        self.maxsize = maxsize
        Queue._steal_daemon(self.mpq, self.qq, self)
        self.debug = debug

    def __del__(self):
        if self.debug:
            print 'del'

    def put(self, obj):
        self.mpq.put(obj)

    def get(self):
        return self.qq.get()

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


