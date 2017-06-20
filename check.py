#!/usr/bin/env python
# -*- coding: utf-8 -*-

'check whois'

__author__ = 'Z. Tang'

import subprocess as sp
import re
import sys
import string
import itertools
import socket
import threading
from timeout import time_out

class WhoisCheck():
    def __init__(self):
        self.ava_list = []

    def _help(self):
        print 'Please Enter your Domain Name Rule to bulk check domains'
        print 'Domain Rules:'
        print ' - N: Number,'
        print ' - L: Letter'
        print ' - A: Both number or letter'
        print 'e.g.,'
        print ' - NNN.com means 3-number .com domains'
        print ' - NLL.cn means 1-number and 2-letter .cn domains'
        print ' - NLN.me means 1-number, 1-letter and 1-number .me domains'
        print ' - AAA.org means all 3-character(both number of letter) .org domains'
        print 'After input the domain rules, the script will generate and check all domains'
        print 'that match the rules'
        print 'use \'-f file_name\' option to read domain list from file'
        print 'This script support all tlds that has whois server.'
        print 'Have fun!'

    def generate_list(self, dn_rule):

        if not re.match(r'[nlaNLA]+[\.][a-zA-Z]+', dn_rule):
            print '== Domain Rule Error =='
            self._help()
            sys.exit(0)

        prefix = re.split(r'[\.]', dn_rule)[0]
        extension = re.split(r'[\.]', dn_rule)[1]

        # get all lists for each character
        char_list = []
        for char in prefix:
            if char == 'n' or char == 'N':
                if char_list == []:
                    tmp = itertools.product(string.digits)
                else:
                    tmp = itertools.product(char_list, string.digits)
                char_list = [''.join(nn) for nn in tmp]
            elif char == 'l' or char == 'L':
                if char_list == []:
                    tmp = itertools.product(string.lowercase)
                else:
                    tmp = itertools.product(char_list, string.ascii_lowercase)
                char_list = [''.join(ll) for ll in tmp]
            else:
                if char_list == []:
                    tmp = itertools.product(string.digits + string.lowercase)
                else:
                    tmp = itertools.product(char_list, string.digits + string.lowercase)
                char_list = [''.join(aa) for aa in tmp]

        dn_list = [ch + '.' + extension for ch in char_list]
        # print dn_list
        return dn_list

    # get the list from file
    def get_list(self, file_name):
        tmp = []
        with open(file_name, 'r') as f:
            for line in f.readlines():
                tmp.append(line.strip())

        return tmp

    # get the whois from system
    def check_whois(self, dn):
        try:
            dn_info = sp.check_output('whois %s' % dn, shell=True)
            # print 'The domain %s has been registered!' %dn
            return True
        except sp.CalledProcessError, e:
            # print 'The domain %s is available!' %dn
            return False

    def check_ping(self, dn):
        try:
            socket.gethostbyname(dn)
            return True
        except socket.error:
            return False

    '''
    def timeout(self, func, args):
        p = threading.Thread(target=func, args=[args])
        p.setDaemon(True)
        p.start()
        p.join(1)
        if p.is_alive():
            print 'timeout'
            return False
    '''

    def check_available(self, dn):
        # if time out, we think it false
        if time_out(self.check_ping, dn) == False:
            # when time out, check whois
            if self.check_whois(dn) == True:
                return True
            else:
                return False
        # if not time out, get ping result
        else:
            if self.check_ping(dn) == True:
                return True
            else:
                return False

    def check_available_new(self, dn):
        try:
            socket.gethostbyname(dn)
            return True
        except socket.error:
            try:
                dn_info = sp.check_output('whois %s' %dn, shell=True)
                return True
            except sp.CalledProcessError:
                return False

    def check_all(self, dn_list):
        for dn in dn_list:
            #result = self.check_available_new(dn)
            result = self.check_available(dn)
            if result == True:
                print 'The domain %s has been registered!' %dn
            else:
                print 'The domain %s is available!' %dn
                self.ava_list.append(dn)


if __name__ == '__main__':

    wc = WhoisCheck()

    # print sys.argv
    # sys.exit(0)
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            wc._help()
            sys.exit(0)
        else:
            print 'Wrong input, please use -h for help'
            sys.exit(0)

    elif len(sys.argv) == 3:
        if sys.argv[1] == '-f' or sys.argv[1] == '--file':
            file_name = sys.argv[2]
            dn_list = wc.get_list(file_name)
        else:
            print 'Wrong input, please use -h for help'
            sys.exit(0)

    elif len(sys.argv) >= 4:
        print 'Wrong input, please use -h for help'
        sys.exit(0)

    else:
        dn_rule = raw_input('Please input domain name rule:')
        dn_list = wc.generate_list(dn_rule)

    wc.check_all(dn_list)
    print 'All domain available:'
    for ava_dn in wc.ava_list:
        print ava_dn

    with open('available.txt', 'w') as f:
        for av_dn in wc.ava_list:
            f.write(av_dn)
            f.write('\n')
    with open('dnlist.txt', 'w') as f:
        for dns in dn_list:
            f.write(dns)
            f.write('\n')

