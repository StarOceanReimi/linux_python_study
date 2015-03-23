#!/usr/bin/python

from multiprocessing import Process, Queue
import os, time, random

def write(q):
    for value in ['A', 'B', 'C']:
        print 'Put %s to queue...' % value
        q.put(value)
        time.sleep(random.random())

def read(q):
    while True:
        value = q.get(True)
        print 'Get %s from queue (pid=%r).' % (value, os.getpid())


if __name__ == '__main__':
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pr2 = Process(target=read, args=(q,))
    pr2.start()
    pw.start()
    pr.start()
    pw.join()
    pr.terminate()
    pr2.terminate()
