#!/usr/bin/env python

from builtins import input

from .fizzbuzz import FizzBuzzer


def main():
    """Run Fizzbuzz program"""

    fizzbuzzer = FizzBuzzer()
    while True:
        output = fizzbuzzer(input("Provide a value> "))
        if output:
            print("%s" % (output))


if __name__ == "__main__":
    main()
