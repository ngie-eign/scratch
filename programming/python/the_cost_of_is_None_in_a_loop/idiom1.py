#!/usr/bin/env python

def big_list_generator():
    for i in xrange(1000000):
        yield i

big_list = big_list_generator()

i0 = big_list.next()
i1 = big_list.next()

try:
    while True:
        #print(i0, i1)
        i0 = i1
        i1 = big_list.next()
except StopIteration:
    pass
