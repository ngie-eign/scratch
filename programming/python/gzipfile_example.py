#!/usr/bin/env python

import gzip

with gzip.GzipFile('myfile.gz', 'wb') as gf:
    gf.write(open(__file__).read())
