#!/usr/bin/env python

import collections

A = collections.namedtuple('A', ['a', 'b'])
A.__eq__ = lambda self, other: self.a == other.a

a = A(*range(2))
b = A(*range(1, 3))
c = A(0, -1)

print(a == b)
print(a == c)
