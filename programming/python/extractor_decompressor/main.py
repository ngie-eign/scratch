#!/usr/bin/env python
"""
A generalized decompressor/extractor script

This is useful in cases when bsdtar/libarchive isn't present as it
automatically determines the appropriate format for extracting files.

Originally written against Python 2.7.5.

...moduleauthor: Enji Cooper
...date: May 2014
"""

import argparse
import sys

from . import (
    decompressors,
    extractors,
)


if sys.version_info < (2, 7):
    sys.exit('This script is only supported on 2.7+')


def main(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('--keep', action='store_true')

    parser.add_argument('filename')
    parser.add_argument('destdir')

    args = parser.parse_args()

    filename = args.filename

    for extractor in [extractor for ext, extractor in extractors.items()
                      if filename.endswith(ext)]:
        extractor(filename, args.destdir, keep=args.keep)
        sys.exit(0)

    for decompressor in [decompressor for ext, decompressor in
                         decompressors.items()
                         if filename.endswith(ext)]:
        decompressor(filename, args.destdir, keep=args.keep)
        sys.exit(0)

    sys.exit('Unsupported file: %s' % (filename, ))


if __name__ == '__main__':
    main()
