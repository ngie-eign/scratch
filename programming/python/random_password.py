#!/usr/bin/env python
"""Good for generating random ASCII passwords
"""

import argparse
import random
import string


def positive_integer(optarg):
    """Cribbed from https://docs.python.org/2/library/argparse.html#type"""
    value = int(optarg)
    if value <= 0:
        raise argparse.ArgumentTypeError('%r is not a positive integer'
                                         % (value))
    return value


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--digits', action='store_true', default=False,
                        help='include digits in the working set')
    parser.add_argument('--letters', action='store_true', default=False,
                        help='include ASCII characters in the working set')
    parser.add_argument('--length', required=True, type=positive_integer,
                        help='length of the random string')
    parser.add_argument('--no-repeating', action='store_true', default=False,
                        help='do not repeat characters')
    parser.add_argument('--special-chars', type=str, default='',
                        help='additional characters to add to the working set')

    args = parser.parse_args()

    character_set = args.special_chars
    if args.digits:
        character_set += string.digits
    if args.letters:
        character_set += string.ascii_letters

    if not character_set:
        parser.error('No overall working character set specified via one of '
                     'the options')

    character_set = ''.join(set(character_set[:])) # Dedupe the character set

    if len(character_set) < args.length and args.no_repeating:
        parser.error('Not enough unique working characters to make a '
                     'non-repeating random string')

    random_string = ''
    while len(random_string) < args.length:
        random_char = random.choice(character_set)
        if not args.no_repeating or random_char not in random_string:
            random_string += random_char

    print(random_string)


if __name__ == '__main__':
    main()
