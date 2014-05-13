#!/usr/bin/env python
"""
Dump out resource information for a forked PID via
lsof, ps, and /proc/*/status.
"""

import commands
import os
import sys
import time

child = os.fork()
if child:
    time.sleep(2)
    cmds = [
        'lsof -p %d' % (child, ),
        'ps auxww | awk "\$2 == %d"' % (child, ),
        "cat /proc/%d/status" % (child, ),
    ]
    for cmd in cmds:
        output = commands.getoutput("sh -xc '" + cmd + "'")
        if output:
            print(output)
    time.sleep(1)
sys.exit(1)
