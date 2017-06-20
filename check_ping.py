#!/usr/bin/env python
# -*- coding: utf-8 -*-

'test ping check'

import subprocess as sp
import multiprocessing
import time


import socket
import signal



def host_check(dn):
    try:
        socket.gethostbyname(dn)
        return True
    except socket.error:
        return False


def handler(signum, frame):
    raise AssertionError

if __name__ == '__main__':

    p = multiprocessing.Process(target=host_check('06.com'))
    p.start()
    p.join(1)
    if p.is_alive():
        print 'timeout'
        p.terminate()
        p.join()
