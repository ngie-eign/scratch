#!/usr/bin/env python
"""
This script counts the number of items with a particular path prefix.

This script should take paths after they have been passed through
dirname, in order to eliminate paths in an immediate directory and more
accurately count files by path/tree.

Inspired by:
https://stackoverflow.com/questions/7852384/finding-multiple-common-starting-strings
"""

from __future__ import print_function

import argparse
import itertools
import os
import os.path
import sys


def trim_path(path, max_depth):
    while max_depth < path.count(os.sep):
        path = os.path.dirname(path)
    return path


def positive_int_type(val):
    val = int(val)
    if val <= 0:
        raise argparse.ArgumentTypeError("value passed was negative: %d" % (val))
    return val


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--max-depth",
        required=True,
        type=positive_int_type,
    )
    ap.add_argument(
        "input_file",
        type=argparse.FileType("rb"),
        default=sys.stdin,
        nargs="?",
    )
    args = ap.parse_args()

    with args.input_file as fp:
        lines = sorted([line.strip() for line in fp.readlines()])

    for key, group in itertools.groupby(lines, lambda p: trim_path(p, args.max_depth)):
        print(key, len(list(group)))


if __name__ == "__main__":
    main()
