# FMQ

"FMQ" is for both **Feed-Me-Queue** and **Fast-Multiprocessing-Queue**. FMQ speeds up single-direction inter-process data transfer between python processes.

## Introduction

This project is inspired by the use of multiprocessing.Queue (mp.Queue). mp.Queue is slow for large data item because of the speed limitation of pipe (on Unix-like systems). 

With mp.Queue handling the inter-process transfer, FMQ implements a stealer thread, which steals an item from mp.Queue once any item is available, and puts it into a Queue.Queue. Then, the consumer process can fetch the data from the Queue.Queue immediately.

The speed-up is based on the assumption that **both producer and consumer processes are compute-intensive** (thus multiprocessing is neccessary) and the **data is large (eg. >50 227x227 images)**. Otherwise mp.Queue with multiprocessing or Queue.Queue with threading is good enough.

## License
MIT
