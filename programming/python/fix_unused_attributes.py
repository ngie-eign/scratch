#!/usr/bin/env python3
"""
The purpose of this script is to automate replacing unused attributes with
`LTP_ATTRIBUTE_UNUSED`.

Although my goals for this script are very fixed and niche, this is a common
problem that I have had to solve multiple times in the past in different forms.

Input: compiler output provided from clang, which includes lines of the form:

conformance/interfaces/timer_create/speculative/5-1.c:45:18: error: unused parameter 'signo' [-Werror,-Wunused-parameter]

What this means is that there is an unused variable, `signo` on line 45,
column 18 (which isn't really important) in
`conformance/interfaces/timer_create/speculative/5-1.c`

The goal is to open/slurp in said file, fast forward to said line, append
"LTP_ATTRIBUTE_UNUSED" to the variable, then write out the modified line.

Design notes:
- This module is not using temporary files, given that these files are
  contained in a git checkout, and can easily be saved/restored in the event
  there was actual file content corruption using `git checkout`, `git reset`,
  etc. Using `shutil.move(..)` with a deterministic filename extension (".bk")
  is sufficient for this task.
"""

import argparse
from collections import defaultdict
import functools
import re


UNUSED_ATTRIBUTE_CONSTANT = "LTP_ATTRIBUTE_UNUSED"
UNUSED_ATTRIBUTE_REGEXP = re.compile(
    r"(../)*(?P<path>.+):(?P<line>\d+):(?P<column>\d+): error: unused parameter '(?P<name>[^']+)'"
)
assert UNUSED_ATTRIBUTE_REGEXP.search(__doc__, re.M) is not None


@functools.total_ordering
class UnusedAttribute:

    def __init__(self, name, column, line):
        self.name = name
        self.column = int(column)
        self.line = int(line)

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.line == other.line and
            self.column == other.column
        )

    def __lt__(self, other):
        return (self.line, self.column) < (other.line, other.column)

    def __repr__(self):
        return "%s(name=%r, column=%r, line=%r)" % (
            self.__class__.__name__, self.name, self.column, self.line
        )


def annotate_unused_attributes_in_file(path, unused_attributes):
    if not unused_attributes:
        return
    with open(path) as fp:
        lines = fp.readlines()

    sorted_unused_attributes = sorted(unused_attributes, reverse=True)
    for unused_attribute in sorted_unused_attributes:
        column = unused_attribute.column
        line_number = unused_attribute.line
        name = unused_attribute.name
        replacement = "%s %s" % (name, UNUSED_ATTRIBUTE_CONSTANT)
        line = lines[line_number-1]
        try:
            lines[line_number-1] = "%s%s" % (
                line[:column-1],
                line[column-1:].replace(name, replacement, 1)
            )
        except IndexError:
            print(unused_attribute, lines[line_number-1])

    with open(path, "w") as fp:
        print("".join(lines), end="", file=fp)


def find_unused_attributes(input_file):
    unused_attributes_by_path = defaultdict(list)
    with open(input_file) as fp:
        for line in fp.readlines():
            match = UNUSED_ATTRIBUTE_REGEXP.search(line)
            if match is None:
                continue
            matchdict = match.groupdict()
            unused_attr = UnusedAttribute(
                **{attr: matchdict[attr] for attr in ("name", "column", "line")}
            )
            unused_attributes_by_path[matchdict["path"]].append(unused_attr)

    for path, unused_attributes in unused_attributes_by_path.items():
        annotate_unused_attributes_in_file(path, unused_attributes)


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")

    args = parser.parse_args()

    find_unused_attributes(args.input_file)


if __name__ == "__main__":
    main()
