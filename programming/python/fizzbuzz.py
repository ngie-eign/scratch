#!/usr/bin/env python3
"""
An example fizzbuzz application.

Prints out 'fizz' when a value is cleanly divisible by 3, 'buzz' when a value
is cleanly divisible by 5, and 'fizzbuzz' when a value is divisible by both 3
and 5.

Complete with inline unit tests.
"""

from __future__ import print_function

import argparse
import sys
import unittest


def check_fizzbuzz(value):
    s = ""
    if not value:
        return s
    if (value % 3) == 0:
        s += "fizz"
    if (value % 5) == 0:
        s += "buzz"
    return s



class FizzBuzzTest(unittest.TestCase):
    def test_fizz(self):
        for i in (3, 6, 9, 12, 18):
            self.assertEqual("fizz", check_fizzbuzz(i))

    def test_buzz(self):
        for i in (5, 10, 20, 25, 35):
            self.assertEqual("buzz", check_fizzbuzz(i))

    def test_fizzbuzz(self):
        for i in (15, 30, 45, 60):
            self.assertEqual("fizzbuzz", check_fizzbuzz(i))

    def test_nul(self):
        for i in (-1, 0, 2, 27.3):
            self.assertEqual("", check_fizzbuzz(i))


def demo_main():
    for i in range(32):
        s = check_fizzbuzz(i)
        if s:
            print("{}: {}".format(i, s))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test",
        action="store_true",
        help="run tests instead of demo code",
    )
    opts, unknown_args = parser.parse_known_args()
    if opts.test:
        unittest.main(
            module=__name__, argv=([sys.argv[0]] + unknown_args), exit=True,
        )
    demo_main()


if __name__ == "__main__":
    main()
