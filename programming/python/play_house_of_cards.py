#!/usr/bin/env python3
"""
Related to:
https://stackoverflow.com/questions/43031968/how-to-make-simple-alarms-on-python/43032092

time.sleep(..) can be interrupted, resulting in a time which differs
from the expected slept time. The suggestion to use `signal.alarm`
instead of `time.sleep()` .

`signal.alarm()` is a good alternative for simple single process
asynchronous event handling, but is only guaranteed to be supported on
Unix, and there are limits to the precision (in seconds) that can be
used for timing things.

See the `time.sleep(..)` docs for more details, along with your OS-specific
documentation for `sleep(3)` to better understand why `sleep(3)` can be
less exact than `alarm(3)`.

Using an alternative API for multiprocessing and per-thread timing is
recommended. Unfortunately (as of my writing this) there isn't really a
solid interface implemented per POSIX with pthreads, so it's best to use
python's timeout-enabled interfaces, e.g., `concurrent.futures.Executor.map`,
`threading` interfaces, or OS-specific alternative interfaces, e.g.,
`kqueue` and `select`.

- https://docs.python.org/3/library/time.html#time.sleep .
- https://www.freebsd.org/cgi/man.cgi?query=sleep&apropos=0&sektion=3
- https://www.freebsd.org/cgi/man.cgi?query=alarm&apropos=0&sektion=3
"""

import datetime
import os
import signal
import time

now = datetime.datetime.now()

the_future = datetime.datetime.combine(now.date(), datetime.time(16, 48, 0))

ALARMED = False
def smack_alarm(*args):
    # IMPORTANT: don't do calls from signal handlers that can be reentered,
    # e.g., printing messages or exiting programs!
    global ALARMED
    ALARMED = True

signal.signal(signal.SIGALRM, smack_alarm)
signal.alarm(int((the_future - now).total_seconds()))

# Don't burn CPU necessarily; use a file mutex instead of doing naive polling
# like the following in performance-sensitive applications.
while not ALARMED:
    time.sleep(0.75)

print("would have run `start BTS_House_Of_Cards.mp3`")
