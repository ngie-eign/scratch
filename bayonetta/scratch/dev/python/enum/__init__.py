#!/usr/bin/env python
"""
A simple enum module.

Better idea than parsing a bunch of nasty string arguments passed into
functions (seen it happen before more than once).

Garrett Cooper, April 2012
"""

class Enum:
   """Simple enum-like class.

   >>> import enum
   >>> # a - d
   >>> sequence = map(lambda x: chr(x + ord('a')), range(4))
   >>> e = enum.Enum(*sequence)
   >>> assert e.a == 0
   >>> try:
   ...    e.h
   ... except AttributeError, exc:
   ...    pass
   ... else:
   ...    raise AssertionError('Expected e.h to raise an AttributeError')
   >>>

   """

   def __init__(self, *values):
       if not values:
           raise ValueError('no enums defined')

       seen = {}
       for i, value in enumerate(values):
           if value in seen:
               raise ValueError('duplicate element ``%s`` found at index %d'
                                % (value, i, ))
           else:
               seen[value] = True

       self.values = values


   def __getattr__(self, value):
       if value in self.values:
           return self.values.index(value)
       raise AttributeError("'%s' object has no attribute '%s'"
                            % (str(self.__class__).split('.')[-1], value))
