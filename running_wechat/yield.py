# -*- coding:utf-8 -*-
import time
import threading


def io_handler():
    def fun():
        print 'start io_handler'
        time.sleep(10)
        result = 'io result'

        global gen
        try:

            print 'end io_handler'
            gen.send(result)

        except StopIteration:
            pass

    thread1 = threading.Thread(target=fun)
    thread1.start()


def rep_a():
    print 'start rep_a'
    result = yield io_handler()
    print result
    print 'end rep_a'


def rep_b():
    print 'start rep_b'
    print 'end rep_b'


gen = None
if __name__ == '__main__':
    gen = rep_a()
    gen.next()
    rep_b()
