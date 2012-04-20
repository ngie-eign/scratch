#!/usr/bin/env python

import os
import sys
import tarfile
import tempfile

if len(sys.argv) != 2:
    sys.exit('usage: %s .BIN file' % (os.path.basename(sys.argv[0])))

with open(sys.argv[1], 'rb') as binfd:
    while True:
        line = binfd.readline()
        if line.startswith('#####Startofarchive#####'):
            with tarfile.open(fileobj=binfd) as tarobj:
                tarobj.extractall()
            break
