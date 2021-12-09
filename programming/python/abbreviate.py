#!/usr/bin/env python
"""Abbreviate buffer content repetitions into a more human readable format.

This also demonstrates how to use line_profiler, memory_profiler, and timeit to
measure computation and memory performance, as well as quantify wall time spent
computing the repetitions.

Examples:

% python -m kernprof -bl abbreviate.py
% python -m line_profiler abbreviate.py.lprof

% python -m memory_profiler abbreviate.py

% python -m timeit 'import abbreviate; abbreviate.run()'

IMPORTANT:
This method of compressing text only works with strings that don't contain digits.
"""

from functools import reduce
from itertools import groupby

try:
    #from memory_profiler import profile
    profile
except NameError:
    profile = lambda x: x



@profile
def abbreviate(buf):
    return reduce(lambda x, y: x + y[0] + str(len(list(y[1]))), groupby(buf), "")


@profile
def abbreviate_loop(buf):
    result = ""
    if not buf:
        return ""

    c0 = buf[0]
    count = 0
    for c in buf:
        if c == c0:
            count += 1
        else:
            result += c0 + str(count) if count > 2 else c0
            count = 1
            c0 = c
    result += c0 + str(count) if count > 2 else c0
    return result


a_buf = "abbcccddddeeeeeffffffggggggghhhhhhhh" * 100
repeat_buf = "a" * 1000
repeat_buf = list(i % ord("A") for i in range())

def run():
    abbreviate(a_buf)
    abbreviate_loop(a_buf)
    abbreviate(repeat_buf)
    abbreviate_loop(repeat_buf)
    abbreviate(non_repeat_buf)
    abbreviate_loop(non_repeat_buf)


if __name__ == "__main__":
    run()
