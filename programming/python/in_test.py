#!/usr/bin/env python

import collections

class Number(object):
    def __init__(self, number):
        self.number = long(number)

    def __eq__(self, other):
        return self.number == other

NumberTuple = collections.namedtuple('NumberTuple', 'number')

BIG_NUM = 10000000L
SMALLER_NUM = BIG_NUM * 0.42

question = 'Q: Is %d in %d?\nA: %%s.' % (SMALLER_NUM, BIG_NUM)
yesno = lambda res: res and 'Yes' or 'No'

print(question % (yesno(SMALLER_NUM in xrange(BIG_NUM)), ))
print(question % (yesno(Number(SMALLER_NUM) in xrange(BIG_NUM)), ))
print(question % (yesno(NumberTuple(SMALLER_NUM).number in xrange(BIG_NUM), )))

"""
$ python -m cProfile in_test.py
Q: Is 4200000 in 10000000?
A: Yes.
Q: Is 4200000 in 10000000?
A: Yes.
Q: Is 4200000 in 10000000?
A: Yes.
         4200080 function calls in 2.380 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 <string>:1(NumberTuple)
        1    0.000    0.000    0.000    0.000 <string>:8(__new__)
        1    0.010    0.010    0.010    0.010 collections.py:1(<module>)
        1    0.000    0.000    0.000    0.000 collections.py:26(OrderedDict)
        1    0.000    0.000    0.000    0.000 collections.py:282(namedtuple)
       19    0.000    0.000    0.000    0.000 collections.py:323(<genexpr>)
        2    0.000    0.000    0.000    0.000 collections.py:347(<genexpr>)
        2    0.000    0.000    0.000    0.000 collections.py:349(<genexpr>)
        1    0.000    0.000    0.000    0.000 collections.py:381(Counter)
        1    0.000    0.000    0.000    0.000 heapq.py:31(<module>)
        3    0.000    0.000    0.000    0.000 in_test.py:18(<lambda>)
        1    1.350    1.350    2.380    2.380 in_test.py:3(<module>)
        1    0.000    0.000    0.000    0.000 in_test.py:5(Number)
        1    0.000    0.000    0.000    0.000 in_test.py:6(__init__)
  4200001    1.020    0.000    1.020    0.000 in_test.py:9(__eq__)
        1    0.000    0.000    0.000    0.000 keyword.py:11(<module>)
        2    0.000    0.000    0.000    0.000 {all}
        1    0.000    0.000    0.000    0.000 {built-in method __new__ of type object at 0x3fcdfd720}
        1    0.000    0.000    0.000    0.000 {isinstance}
        1    0.000    0.000    0.000    0.000 {len}
        1    0.000    0.000    0.000    0.000 {map}
        2    0.000    0.000    0.000    0.000 {method '__contains__' of 'frozenset' objects}
        1    0.000    0.000    0.000    0.000 {method 'add' of 'set' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        3    0.000    0.000    0.000    0.000 {method 'format' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
       17    0.000    0.000    0.000    0.000 {method 'isalnum' of 'str' objects}
        2    0.000    0.000    0.000    0.000 {method 'isdigit' of 'str' objects}
        2    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
        2    0.000    0.000    0.000    0.000 {method 'replace' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {method 'startswith' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {repr}
        1    0.000    0.000    0.000    0.000 {sys._getframe}

"""
