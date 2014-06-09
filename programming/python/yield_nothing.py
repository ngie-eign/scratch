#!/usr/bin/env python

def generates_a_lot():
    if False:
        for i in list('abcd'):
            yield i

for i in generates_a_lot():
    print(i)
