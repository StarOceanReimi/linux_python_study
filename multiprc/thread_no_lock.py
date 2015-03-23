#!/usr/bin/python

import time, threading
balance = 0
init_balance = balance
print 'Initial balance are %d' % balance
def change_it(n):
    global balance
    balance = balance + n
    balance = balance -n

def run_thread(n):
    for i in range(5000):
        change_it(n)

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))

t1.start()
t2.start()
t1.join()
t2.join()

print 'Atfer run transacation balance is %d, but should be %d' % (balance, init_balance)
