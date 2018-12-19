# -*- coding:utf-8 -*-
import time
import threading

def io_handler(callback):
    def fun(cb):
        print 'start io_handler'
        time.sleep(10)
        print 'end io_handler'
        result='io result'
        cb(result)
    thread1=threading.Thread(target=fun,args=(callback,))
    thread1.start()

def cb(ret):
    print 'start cb'
    print ret
    print 'end cb'



def rep_a():
    print 'start rep_a'
    io_handler(cb)
    print 'end rep_a'

def rep_b():
    print 'start rep_b'
    print 'end rep_b'

if __name__ == '__main__':
    rep_a()
    rep_b()