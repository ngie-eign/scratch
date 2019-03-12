#!/usr/bin/env python

import inspect

class a_class:
    def __init__(self):
        pass

def foo():
    def bar():
        pass

    a = 'b'
    b = 'b'
    c = foo
    d = a_class()
    e = d
    f = bar

    #print('globals', inspect.stack()[0][0].f_globals)
    #print('locals', inspect.stack()[0][0].f_locals)

    assert(inspect.stack()[0][0].f_globals == globals())
    assert(inspect.stack()[0][0].f_locals == locals())

    in_a_haystack = lambda key, value: value == needle and key != 'needle'

    for needle in (a, foo, bar, d, f, ):
        print("needle => '%r'" % (needle, ))
        print([key for key, value in locals().items() if in_a_haystack(key, value)])
        print([key for key, value in globals().items() if in_a_haystack(key, value)])


foo()
