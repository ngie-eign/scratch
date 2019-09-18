#!/usr/bin/env python

from __future__ import print_function

import sys
import time
import timeit


class DaveMatthewsException(Exception):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.message = "Crash... into me... yeah... babayyyyy..."

    def __str__(self):
        return self.message


def expensive_call():
    time.sleep(2)
    return "I'm expensive time-wise"


def expensive_call_that_crashes():
    value = expensive_call()
    try:
        raise DaveMatthewsException()
    except Exception as e:
        print("%s encountered: %s; returning `None`" % (
            e.__class__.__name__,
            e
        ))
        return None
    return value


class FooIsNotAProperty:
    foo = None

    def set_foo(self):
        """This is a setter for `foo`"""
        if self.foo is not None:
            self.foo = expensive_call()


class FooIsAProperty:
    _func_to_call = staticmethod(expensive_call)
    _foo = None

    @property
    def foo(self):
        """Here `foo` is a property.

        Each time you access it the first time, there's something else going
        on by side-effect, which is "expensive". What happens if
        `expensive_call()` failed repeatedly and something swallowed the
        exception, for example? It would take a lot of time to complete and
        never complete successfully.
        """
        if self._foo is None:
            self._foo = self._func_to_call()
        return self._foo


class FooIsAPropertyInANewStyleClass(FooIsAProperty, object):
    pass


class FooIsACrashyProperty(FooIsAProperty):
    _func_to_call = staticmethod(expensive_call_that_crashes)


if __name__ == "__main__":
    # Apparently python 3.x does some magic with the sys.version_info object
    # when it comes to `repr`'ing it.
    print("* `sys.version_info`: %s" % (repr(sys.version_info)))
    classes_to_time = [
        # Time all classes that start with `FooIs`.
        object_name for object_name in dir() if object_name.startswith("FooIs")
    ]

    result_debug = (
        "* Time elapsed for statement: %f sec\n* Statement:\n```%s```"
    )
    for class_to_time in classes_to_time:
        import_statement = (
            "from __main__ import %s, DaveMatthewsException" % (class_to_time)
        )
        statements = [
            "print(%s().foo)" % (class_to_time),
            """
bar = {0}()
TWICE_IS_NICE = 2
for attempt in range(TWICE_IS_NICE):
    print(bar.foo)
if hasattr(bar, "set_foo"):
    # This blatantly sets the value of `.foo` using an underlying call
    # structure, etc. This is a less opaque way of setting `.foo`.
    for attempt in range(TWICE_IS_NICE):
        bar.set_foo()
else:
    # This doesn't do what you might think at first glance at this block of
    # code, since it's a property ;).. This is a more opaque way of setting
    # `foo`.
    if isinstance(bar, object):
        try:
            for attempt in range(TWICE_IS_NICE):
                bar.foo = "junk"
            assert sys.version_info[0] == 2, "This should have crashed on 3.x"
        except AttributeError as e:
            # This will crash with new-style classes:
            # https://stackoverflow.com/a/15812738 .
            print("Failed to set `bar.foo`: %s" % (e, ))
    else:
        bar.foo = "junk"
for attempt in range(TWICE_IS_NICE):
    print(bar.foo)
""".format(class_to_time),
        ]
        for statement in statements:
            print("* `timeit.timeit` statement output:")
            time_taken = timeit.timeit(
                statement,
                number=1,
                setup=import_statement,
            )
            print(result_debug % (time_taken, statement))
