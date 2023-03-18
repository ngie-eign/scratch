#!/usr/bin/env python3
"""Flatten output from the clang preprocessor.

This script takes the output from `clang -dD -E` and flattens it so it can be more
easily analyzed/compared by rudimentary tools like awk, diff, and grep.
"""
import argparse
import atexit
import logging
import os
import re
import sys
import tempfile
from typing import Optional


INCLUDE_START_RE = re.compile(r'#\s+\d+\s+"(.+)"')
UNCLOSED_FUNC_DECL_RE = re.compile(r",$")
UNDEF_DIRECTIVE_RE = re.compile(r"^#undef\s+")


def main(argv: Optional[list[str]] = None) -> int:
    """Eponymous main(..)."""
    argparser = argparse.ArgumentParser()

    output_options = argparser.add_mutually_exclusive_group(required=True)
    output_options.add_argument("-i", "--in-place", action="store_true")
    output_options.add_argument(
        "-o", "--output", dest="output_file", type=argparse.FileType("w")
    )

    # argparser.add_argument("--keep-all-scope", action="store_true")
    argparser.add_argument("--keep-blank-lines", action="store_true")
    argparser.add_argument("--skip-undef", action="store_true")
    argparser.add_argument("input_file", type=argparse.FileType("r"))

    def remove_tempfile(temp_filename: str) -> None:
        os.unlink(temp_filename)

    def rename_tempfile(temp_filename: str, input_filename: str) -> None:
        os.rename(temp_filename, input_filename)

    args = argparser.parse_args(args=argv)
    if args.in_place:
        output_fileobj = tempfile.NamedTemporaryFile(
            mode="w+t",
            delete=False,
            dir=os.path.basename(args.input_file),
        )
        atexit.register(remove_tempfile, output_fileobj.name)
        atexit.register(rename_tempfile, output_fileobj.name, args.temp_fileobj.name)
    else:
        output_fileobj = args.output_file

    try:
        output_lines = []
        with args.input_file as input_fileobj:

            keep = False
            original_include_path = None

            for line in input_fileobj:

                if line == "\n":
                    if args.keep_blank_lines:
                        output_lines.append(line)
                    continue

                if args.skip_undef and UNDEF_DIRECTIVE_RE.match(line):
                    continue

                matches = INCLUDE_START_RE.match(line)
                if matches is not None:
                    path_match = matches.group(1)
                    if original_include_path is None:
                        original_include_path = path_match
                    keep = path_match == original_include_path
                    continue
                if not keep:
                    continue

                if UNCLOSED_FUNC_DECL_RE.match(line):
                    line = line.rstrip("\n")

                output_lines.append(line)

        with output_fileobj:
            output_fileobj.writelines(output_lines)
    except Exception:  # pylint: disable=broad-except
        logging.exception("Script failed abnormally.")
        atexit.unregister(rename_tempfile)
        return 1

    atexit.unregister(remove_tempfile)
    return 0


if __name__ == "__main__":
    sys.exit(main())
