#!/usr/bin/env python
"""
Print out a list of items joined with a conjunction, with an optional Oxford
comma ;)..
"""

import types

def join(l, conjunction='and', oxford_comma=True):
    if type(l) not in (types.ListType, types.TupleType):
        raise TypeError('l is not a list')
    if len(l) <= 1:
        return ''.join(l)
    return '%s%s %s %s' % (', '.join(l[:-1]),
                           ((len(l) > 2 and oxford_comma) and ',' or ''),
                           conjunction,
                           l[-1])


print join(list('ab'))
print join(list('abcd'))
print join(['a'])
print join([])

print join(list('abcd'), oxford_comma=False)
print join(['a'], oxford_comma=False)

print join(list('abcd'), conjunction='or')
print join(['a'], conjunction='or')
