#!/usr/bin/env python
# -*- coding: utf-8 -*-

'timeout function'

# import multiprocessing
import time
import threading
import socket


def host_check(dn):
    try:
        socket.gethostbyname(dn)
        print 'true'
        return True
    except socket.error:
        print 'false'
        return False


def time_out(func, args):
    p = threading.Thread(target=func, args=[args])
    p.setDaemon(True)
    p.start()
    p.join(1)
    if p.is_alive():
        print 'timeout'
        return False


if __name__ == '__main__':
    t2 = 0
    t00 = time.time()
    dn = '06.com'
    def timeout(func, args):
        global t2
        p = threading.Thread(target=func, args=[args])
        p.setDaemon(True)
        # p = multiprocessing.Process(target=host_check('06.com'))
        t0 = time.time()
        p.start()
        t1 = time.time()
        p.join(1)
        t2 = time.time()
        print t0 - t00
        print t1 - t0
        print t2 - t1
        # print 'test'
        if p.is_alive():
            # print 'timeout'
            # p.terminate()
            print 'timeout'
            return False

        t4 = time.time()
        print t4 - t2
        # return True

    print timeout(host_check,'dd.de')
    t3 = time.time()
    print t3 - t2