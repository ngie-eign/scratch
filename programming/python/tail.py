#!/usr/bin/env python
"""A script that implements a subset of the tail(1) command

Requirements to implement:
* -f (follow)
* -n (number of lines)
* tail <filename>
* tail - assume stdin
"""

import argparse
import os
import stat
import sys


def positive_integer(optarg):
    value = int(optarg)
    if value <= 0:
        raise argparse.ArgumentTypeError('%r is not a positive integer'
                                         % (value))
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', dest='num_lines', default=10, type=positive_integer)
    ap.add_argument('-f', dest='follow', default=False, action='store_true')
    ap.add_argument('path', default=sys.stdin, nargs='?',
                    type=argparse.FileType('r'))
    args = ap.parse_args()

    # Not all file descriptors are seekable (like /dev/stdin or pipes). Do a best
    # effort to determine whether or not the file is regular, i.e., seekable, up
    # front. If for some odd reason the seek fails, fall back to the dumb
    # algorithm.
    file_num = args.path.fileno()
    file_stat = os.fstat(file_num)
    use_seekable_algorithm = not stat.S_ISREG(file_stat.st_mode)

    line_buffer = []
    if use_seekable_algorithm:
        try:
            # Read file from end.
            # Find appropriate number of lines.
            # Terminate loop when that's true, setting the lines obtained to
            # the line_buffer.
            offset = min(os.fstat(file_num).st_size, 1024) # XXX: customize min?
            while offset <= os.fstat(file_num).st_size:
                args.path.seek(offset, os.SEEK_END)
                buf = args.path.read()
                _line_buffer = buf.splitlines()
                if len(_line_buffer) >= args.num_lines:
                    line_buffer = _line_buffer[:-args.num_lines]
                    break
        except IOError:
            use_seekable_algorithm = False

    if not use_seekable_algorithm:
        for line in args.path.readlines():
            if args.num_lines < len(line_buffer):
                line_buffer.pop(0)
            line_buffer.append(line)

    for line in line_buffer:
        sys.stdout.write(line)
    sys.stdout.flush()

    if not args.follow:
        sys.exit(0)

    while True:
        # XXX: use non-blocking I/O to get past the fact that OSX sucks
        # with FIFOs.
        for line in args.path:
            sys.stdout.write(line)
            sys.stdout.flush()
        sys.stdout.flush()


if __name__ == '__main__':
    main()
