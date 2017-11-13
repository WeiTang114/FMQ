# FMQ

"FMQ" is for both **Feed-Me-Queue** and **Fast-Multiprocessing-Queue**. FMQ speeds up single-direction inter-process data transfer between python processes.

Package: [https://pypi.python.org/pypi/fmq](https://pypi.python.org/pypi/fmq)

## Install
- Requirements: python2.7

```
pip install fmq
```

## Introduction

This project is inspired by the use of multiprocessing.Queue (mp.Queue). mp.Queue is slow for large data item because of the speed limitation of pipe (on Unix-like systems). 

With mp.Queue handling the inter-process transfer, FMQ implements a stealer thread, which steals an item from mp.Queue once any item is available, and puts it into a Queue.Queue. Then, the consumer process can fetch the data from the Queue.Queue immediately.

The speed-up is based on the assumption that **both producer and consumer processes are compute-intensive** (thus multiprocessing is neccessary) and the **data is large (eg. >50 227x227 images)**. Otherwise mp.Queue with multiprocessing or Queue.Queue with threading is good enough.

## Usages
```python
from fmq import Queue
q = Queue() 

# maxsize=10:
q = Queue(maxsize=10)
```

### Put

```python
# put any type of object
q.put("123")
q.put(321)

# simulating a large object (eg 100 256x256 images) 
# which fmq aims to deal with.
q.put(np.zeros((100,256,256,3)))
```

### Get

```python
a = q.get()
```

## Test the time

This example shows the speed difference between mp.Queue and fmq.Queue to get/put a large object (150MB).

Note that fmq.Queue's first get() is as slow as mp.Queue theoretically and practically. You may switch the order to see the difference.

```python
import multiprocessing as mp
import numpy as np
from time import time
import sys
import fmq

q1 = mp.Queue(10)
q2 = fmq.Queue(10)

# uncomment thie line to switch the order
# q1, q2 = q2, q1

a = np.zeros((100, 256, 256, 3))
a_size = sys.getsizeof(a)
print 'Object size: %d bytes = %dKB = %dMB' % (a_size, a_size/1024, a_size/1024/1024)

for i in range(10):
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

# It will cause an error here
# See "Known Issues: main thread exits before queue object is deleted" section for more details.
```

Output:

```
 $ python2 test_speed.py                                                                                                                            [1:19:08]
157286544 bytes, 153600kb, 150mb
mp get() a time 1.44557714462
mp get() a time 2.59632015228
mp get() a time 0.465645074844
mp get() a time 1.47132301331
mp get() a time 0.970722913742
fmq get() a time 0.0138399600983
fmq get() a time 0.00159907341003
fmq get() a time 0.00137996673584
fmq get() a time 0.00151395797729
fmq get() a time 0.00147581100464
Traceback (most recent call last):
  File "test_speed.py", line 30, in <module>
    q2.close()
AttributeError: Queue instance has no attribute 'close'
EOFError
```

# Know Issues

## Main thread exits before queue object is deleted

An EOFError will be raised. The reason is that the background thread is still blocked at srcq.get() (srcq is mp.Queue) when main thread exits and the program is finished.

This will happen only **at the end of the program**, which whould not bother too much if the speed gain is more important to you.

A possible solution is to finish the daemon stealer threads and close the queues once the program finishes. But my experiments are not successful yet.

## License
MIT
