#!/usr/bin/env python

from . import logger


def func():
    logger(__name__).info("Calling Major Tom!")


def foo_bar_baz(*args, **kwargs):
    logger("foo.bar.baz").debug("args=%r, kwargs=%r", args, kwargs)


class Classy:
    def foo_bar_baz(self, *args, **kwargs):
        logger("foo.bar.baz.with_class").critical("args=%r, kwargs=%r", args, kwargs)


func()
foo_bar_baz("a", 1, b=2, c="str")
Classy().foo_bar_baz("a", 1, b=2, c="str")
