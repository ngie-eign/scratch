#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import binascii
import hashlib
import random
import sys


is_py3 = sys.version_info >= (3, )  # XXX: use six package instead.
if is_py3:
    CHR_MAX = 0x10FFFF
    CONV_FUNC = lambda x: str(chr(x))
else:
    CHR_MAX = 128
    CONV_FUNC = lambda x: chr(x)
MINIMUM_LENGTH = 6


def length_type(arg):
    value = int(arg)
    if value <= MINIMUM_LENGTH:
        raise argparse.ArgumentTypeError(
            "The --length argument (%d) must be greater than %d"
            % (value, MINIMUM_LENGTH)
        )
    return value


def main():
    ap = argparse.ArgumentParser()
    # TODO: support other hashlib-supported algorithms.
    # ap.add_argument("--algorithm")
    ap.add_argument(
        "--length",
        type=length_type,
        default=MINIMUM_LENGTH,
        help="Hash string length"
    )
    args = ap.parse_args()

    random.seed()

    m = hashlib.sha512()
    rand_str = "".join([
        CONV_FUNC(random.randrange(CHR_MAX - 1))
                  for _ in range(args.length)
    ])
    if is_py3:  # use six
        rand_str = rand_str.encode("utf-8")

    m.update(rand_str)
    # NB: python 2.x doesn't support `.hexdigest(length)`
    print(m.hexdigest()[:args.length])


if __name__ == "__main__":
    main()
