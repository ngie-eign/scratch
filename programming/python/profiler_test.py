#!/usr/bin/env python

import time

import cProfile
import pstats
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

def loopy():
    for i in range(20):
        time.sleep(0.1)

stats_keys = ['calls', 'cumulative']
profiler = cProfile.Profile()
profiler.enable()

loopy()

profiler.disable()
stream = StringIO()
stats = pstats.Stats(profiler,
                     stream=stream).sort_stats(*stats_keys)
stats.print_stats()
print('Profiling statistics: %s' % (stream.getvalue(), ))
