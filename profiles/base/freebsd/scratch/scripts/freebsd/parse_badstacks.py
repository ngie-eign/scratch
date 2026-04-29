#!/usr/bin/env python
"""Dump out debug.witness.badstacks in either plaintext or JSON format.

Copyright (c) 2015-2026 Enji Cooper
"""

# ruff: noqa: FBT001, FBT002, S101, S603, S607, T201

import argparse
import json
import re
import subprocess
import sys

BAD_STACKS_SYSCTL_OID = "debug.witness.badstacks"
BAD_STACK_START = (
    r'Lock order reversal between "([^"]+)"\(\w+\) and "([^"]+)"\(\w+\)!\n+'
)


def main(argv: list[str] | None = None) -> None:
    """Eponymous main."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--json-format",
        default=False,
        help="dump in JSON format",
        action="store_true",
    )
    parser.add_argument(
        "--json-pretty-print",
        default=False,
        help="pretty print JSON",
        action="store_true",
    )
    parser.add_argument(
        "--omit-stacks",
        default=False,
        help="omit stack backtraces",
        action="store_true",
    )
    args = parser.parse_args(argv)

    try:
        stdout = subprocess.check_output(
            ["sysctl", "-n", BAD_STACKS_SYSCTL_OID],
            stderr=subprocess.STDOUT,
            encoding=None,
            text=True,
        )
    except subprocess.CalledProcessError as cpe:
        print(f"Could not read {BAD_STACKS_SYSCTL_OID}: {cpe.stdout.rstrip('\n')}\n", end="")
        sys.exit(0)

    parse_and_print_bad_stacks(
        stdout,
        json_format=args.json_format,
        json_pretty_print=args.json_pretty_print,
        omit_stacks=args.omit_stacks,
    )


def parse_and_print_bad_stacks(
    output: str,
    json_format: bool = False,
    json_pretty_print: bool = False,
    omit_stacks: bool = False,
) -> None:
    """Parse and print out all entries from `debug.witness.badstacks`."""
    # This effectively parses all badstacks groupings. If "!" no longer separates
    # badstacks from others, this regular expression parsing will break.
    lor_expr = rf"{BAD_STACK_START}([^!]+)"
    flags = re.MULTILINE | re.DOTALL
    matches = re.findall(lor_expr, output, flags=flags)
    bad_stacks = []
    for match in matches:
        if not match:
            continue

        # This assertion's a little more intuitive than the resulting ValueError
        # when the tuple unpack fails
        #
        # ruff: noqa: PLR2004
        assert len(match) == 3, f"match not in expected format: {match!r}"

        bad_stack = {
            "lock 1": match[0].strip(),
            "lock 2": match[1].strip(),
        }
        if not omit_stacks:
            bad_stack["stack"] = match[2].strip() or None
        bad_stacks.append(bad_stack)

    if json_format:
        if json_pretty_print:
            dump_kw = {
                "indent": 4,
                "separators": (",", ": "),
                "sort_keys": True,
            }
        else:
            dump_kw = {}
        json.dump(bad_stacks, sys.stdout, **dump_kw)
        sys.exit(0)

    for bad_stack in bad_stacks:
        key = "lock 1"
        sys.stdout.write(f"{key}: {bad_stack[key]}\n")
        key = "lock 2"
        sys.stdout.write(f"{key}: {bad_stack[key]}\n")
        if not omit_stacks:
            key = "stack"
            sys.stdout.write(f"{key}:\n{bad_stack[key]}\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
