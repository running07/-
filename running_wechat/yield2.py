# -*- coding:utf-8 -*-
import time
import threading


def get_content(fn):
    def wrapper():
        gen_fn = fn()
        gen_io = gen_fn.next()

        def fun():
            result = gen_io.next()
            try:
                print 'send结果唤醒挂起的程序继续执行'
                gen_fn.send(result)
            except StopIteration:
                pass

        thread1 = threading.Thread(target=fun)
        thread1.start()

    return wrapper


def io_handler():
    print 'start io_handler'
    time.sleep(5)
    print 'end io_handler'
    result = 'io result'
    yield result


@get_content
def rep_a():
    print 'start rep_a'
    result = yield io_handler()
    print result
    print 'end rep_a'


def rep_b():
    print 'start rep_b'
    print 'end rep_b'


if __name__ == '__main__':
    rep_a()
    rep_b()
