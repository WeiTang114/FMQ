import multiprocessing as mp
import numpy as np
from time import time
import sys
import fmq

q1 = mp.Queue(10)
q2 = fmq.Queue(10)

a = np.zeros((100, 256, 256, 3))
a_size = sys.getsizeof(a)
print '%d bytes, %dKB, %dMB' % (a_size, a_size/1024, a_size/1024/1024)

for i in range(5):
    q1.put(np.array(a))
    q2.put(np.array(a))

# mp queue get
for i in range(5):
    st = time()
    b = q1.get()
    print 'mp get() a time', time() - st

# fmq queue get
for i in range(5):
    st = time()
    b = q2.get()
    print 'fmq get() a time', time() - st

q2.close()
