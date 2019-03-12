#!/usr/bin/env python

import argparse
import os
import sys
import tempfile


def compare_pattern(pattern, filename, offset):
    with open(filename, "r+b") as fd:
        fd.seek(offset)
        return pattern == fd.read(len(pattern)).decode("ascii")


def write_pattern(pattern, filename, offset):
    with open(filename, "w+b") as fd:
        fd.seek(offset)
        fd.write(pattern.encode("ascii"))


# a-z,A-Z,0-9
ALPHANUMERIC_PATTERN = \
        "".join([chr(i) for i in range(ord("a"), ord("z")+1)]) + \
        "".join([chr(i) for i in range(ord("A"), ord("Z")+1)]) + \
        "".join([chr(i) for i in range(ord("0"), ord("9")+1)])


def run(filename, pattern, offset=0):
    write_pattern(pattern, filename, offset=offset)

    assert compare_pattern(pattern, filename, offset=offset)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--offset", default=0, type=int)

    args = parser.parse_args()

    pattern = ALPHANUMERIC_PATTERN * 30
    filename = tempfile.NamedTemporaryFile(delete=True).name
    try:
        run(filename, pattern, offset=args.offset)
    finally:
        if os.path.exists(filename):
            with open(filename, "r+b") as fd:
                print(fd.read().decode("ascii"))
            print("\n%r" % (repr(os.stat(filename))))
            os.unlink(filename)


if __name__ == "__main__":
    main(argv=sys.argv)
