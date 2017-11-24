#!/usr/bin/env python

import os
import shutil
import sys

if len(sys.argv) <= 1:
    sys.exit('usage: %s path ..' % (os.path.basename(sys.argv[0])))

for root in sys.argv[1:]:
    for dirpath, dirs, files in os.walk(root, topdown=True):

        for i, dirname in enumerate(dirs):
            src = os.path.join(dirpath, dirname)
            dest = os.path.join(dirpath, str(i))
            shutil.move(src, dest)
            shutil.rmtree(dest, ignore_errors=True)

        for i, filepath in enumerate(files):
            os.remove(filepath)

    shutil.rmtree(root)
