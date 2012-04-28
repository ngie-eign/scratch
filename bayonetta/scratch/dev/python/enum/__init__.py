#!/usr/bin/env python
"""
Simple enumerator module.

Better idea than parsing a bunch of nasty string arguments passed into
functions (seen it happen before more than once).

Garrett Cooper, April 2012
"""

class Enum(object):
   """Simple enumerator-like class.

   >>> import enum
   >>> # a - d
   >>> sequence = map(lambda x: chr(x + ord('a')), range(4))
   >>> e = enum.Enum(*sequence)
   >>> assert e.a == 0

   An AttributeError is thrown if a constant has not been registered:

   >>> import enum
   >>> sequence = map(lambda x: chr(x + ord('a')), range(4))
   >>> e = enum.Enum(*sequence)
   >>> e.h
   Traceback (most recent call last):
       ...
   AttributeError: 'Enum' object has no attribute 'h'
   >>>

   As is this case (Enum objects are readonly after they're initialized):

   >>> import enum
   >>> sequence = map(lambda x: chr(x + ord('a')), range(4))
   >>> e = enum.Enum(*sequence)
   >>> e.a = 42
   Traceback (most recent call last):
       ...
   AttributeError: 'Enum' object is read-only
   >>>

   And finally, this (Enum objects constants are immutable once fully
   initialzed):

   >>> import enum
   >>> sequence = map(lambda x: chr(x + ord('a')), range(4))
   >>> e = enum.Enum(*sequence)
   >>> del e.a
   Traceback (most recent call last):
       ...
   AttributeError: 'Enum' object is read-only
   >>>

   Some attributes aren't legal either (__class__, etc) because they're
   reserved.

   >>> import enum
   >>> e = enum.Enum('__class__')
   Traceback (most recent call last):
       ...
   ValueError: constant '__class__' already present in 'Enum' object 
   >>>

   """

   _readonly = False

   def __init__(self, *constants):

       self._class_name = "'" + str(self.__class__)[:-1].split('.')[-1]

       if not constants:
           raise ValueError('no enums defined')

       for i, constant in enumerate(constants):
           if getattr(self, constant, None):
               raise ValueError("constant '%s' already present in %s object "
                                % (constant, self._class_name, ))
           else:
               setattr(self, constant, i)

       self._readonly = True


   def __delattr__(self, name):
       if self._readonly:
           print 'This is me: %s' % self._class_name
           raise AttributeError('%s object is read-only' % (self._class_name))
       object.__detattr__(self, name, value)


   def __setattr__(self, name, value):
       if self._readonly:
           raise AttributeError('%s object is read-only' % (self._class_name))
       object.__setattr__(self, name, value)


