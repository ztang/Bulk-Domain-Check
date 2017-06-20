#!/usr/bin/env python
# -*- coding: utf-8 -*-

'a test file'

ll = []
with open('dnlist.txt', 'r') as f:
    for line in f.readlines():
        ll.append(line.strip())

print ll