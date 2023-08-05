#!/usr/bin/env python
"""Helper script for creating Makefile.crates for FreeBSD ports.
"""

import argparse
import sys
from typing import Optional

try:
    import tomllib
except ImportError:
    import toml as tomllib


def main(argv: Optional[list[str]] = None) -> int:
    argparser = argparse.ArgumentParser()
    argparser.add_argument("cargo_lock_file", type=argparse.FileType("r"))

    args = argparser.parse_args(args=argv)

    with args.cargo_lock_file as fp:
        print(
            "CARGO_CRATES=    {}".format(
                " \\\n\t".join(
                    p["name"] + "-" + p["version"] for p in tomllib.load(fp)["package"]
                )
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
