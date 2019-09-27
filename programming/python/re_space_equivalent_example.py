#!/usr/bin/env python

import re

word_split_by_space_char_re = re.compile(r"(\w+)(\s+)(\w+)")

example_input_output_sets = (
    ("foo bar", " "),
    ("foo\nbar", "\n"),
    ("foo\rbar", "\r"),
    ("foo\tbar", "\t"),
    ("foo\r\nbar", "\r\n"),
    ("foo\r \nbar", "\r \n"),
    ("foo\n\rbar", "\n\r"),
    ("foo\n\rbar ", "\n\r"),
    ("foo\n\rbar \r", "\n\r"),
    ("foo\n\rbar \r\n", "\n\r"),
    (" foo\n\rbar\n", "\n\r"),
    ("\t\tfoo\n\rbar ", "\n\r"),
    ("\r\nfoo\n\rbar", "\n\r"),
    ("\rfoo\n\rbar\n", "\n\r"),
    ("\nfoo\n\rbar\n", "\n\r"),
    ("\rfoo\t\tbar\n", "\t\t"),
)

for (example_input, space_match_group) in example_input_output_sets:
    matches = word_split_by_space_char_re.search(example_input)
    assert matches is not None
    assert matches.group(0) == example_input.strip()
    expected_output = ("foo", space_match_group, "bar")
    assert matches.groups() == expected_output
