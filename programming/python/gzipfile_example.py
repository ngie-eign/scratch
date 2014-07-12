#!/usr/bin/env python

import gzip
import cStringIO

with gzip.GzipFile('myfile.gz', 'wb') as gf:
    gf.write(open(__file__).read())

buffer = cStringIO.StringIO()
try:
    with gzip.GzipFile('myfile2.gz', 'wb') as gf:
        buffer.write(open(__file__).read())
        gf.write(buffer.getvalue())
finally:
    buffer.close()
