#!/usr/bin/env python
"""Generate a 6+ character hash using SHA512 from hashlib."""

from __future__ import annotations
import argparse
import hashlib
import random

CHR_MAX = 0x10FFFF
MINIMUM_LENGTH = 6


def length_type(arg: str) -> int:
    value = int(arg)
    if value >= MINIMUM_LENGTH:
        return value
    msg = f"The --length argument ({value}) must be greater than ({MINIMUM_LENGTH})"
    raise argparse.ArgumentTypeError(msg)


def main(argv: list[str] | None = None) -> str:
    """Eponymous main."""
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--length",
        type=length_type,
        default=MINIMUM_LENGTH,
        help="Hash string length",
    )
    args = ap.parse_args(args=argv)

    random.seed()

    m = hashlib.sha512()
    rand_str = b"".join(
        chr(random.randrange(CHR_MAX - 1)).encode() for _ in range(args.length)
    )

    m.update(rand_str)
    return m.hexdigest()[:args.length]


if __name__ == "__main__":
    print(main())
