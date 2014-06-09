#!/usr/bin/env python

def big_list_generator():
    for i in xrange(1000000):
        yield i

big_list = big_list_generator()

i0 = None
i1 = None

try:
    while True:
        i0 = i1
        i1 = big_list.next()
        if i0 is None or i1 is None:
            continue
except StopIteration:
    pass
