#!/usr/bin/env python
"""
Example:

What changed between FreeBSD 9.0-RELEASE and 11.0-RELEASE, from a 2-component
directory level:

    git_branch_stat.py --exclude '*/Makefile.depend' \
            --exclude 'tools/regression/*' \
            --strip-remainder 2 \
            --output=freebsd-9-to-11.csv release/9.0.0 stable/11.0.0
"""

import argparse
from collections import OrderedDict
import csv
import errno
import fnmatch
try:
    import io
except ImportError:
    import StringIO as io
import os.path
import subprocess
import sys


class StripAction(argparse.Action):
    """Custom action for --strip"""
    def __call__(self, parser, namespace, values, option_string=None):
        if values < 0:
            raise ValueError('Value specified to %s must be an integral value '
                             'greater than or equal to 0' % (option_string))

        setattr(namespace, self.dest, values)


def main():
    """main"""

    parser = argparse.ArgumentParser()
    parser.add_argument('--exclude', action='append', default=['/dev/null'],
                        help=('exclude [fnmatch-compatible] patterns from '
                              'summary'))
    parser.add_argument('--input',
                        help='input diff file to run through diffstat')
    parser.add_argument('--output',
                        help='output file for csv-formatted stats')
    parser.add_argument('--strip-remainder',
                        action=StripAction,
                        help=('number of components to keep when stripping '
                              'off trailing parts.'),
                        type=int)
    parser.add_argument('src', help='source branch/git commit hash')
    parser.add_argument('dest', help='destination branch/git commit hash')

    args = parser.parse_args()

    if args.input:
        cmd = 'cat %s' % (args.input)
    else:
        cmd = 'git diff --dst-prefix= --src-prefix= %s %s 2>/dev/null' % \
            (args.src, args.dest)
    output = subprocess.check_output('%s | diffstat -qt' % (cmd),
                                     shell=True)
    with io.StringIO(unicode(output)) as input_fp:
        csv_reader = csv.DictReader(input_fp)
        rows = []

        csv_fields = csv_reader.fieldnames
        for row in csv_reader:
            for exclude_pattern in args.exclude:
                if fnmatch.fnmatch(row['FILENAME'], exclude_pattern):
                    break
            else:
                rows.append(row)

    if args.strip_remainder:
        rows_by_path = OrderedDict()

        stat_fields = csv_fields[:-1] # Skip over 'FILENAME'

        for row in rows:
            path_split = row['FILENAME'].split(os.path.sep,
                                               args.strip_remainder)
            if len(path_split) <= args.strip_remainder:
                continue
            path = os.path.sep.join(path_split[:-1])
            rows_by_path.setdefault(path, {field: 0 for field in stat_fields})

            for stat_field in stat_fields:
                rows_by_path[path][stat_field] += int(row[stat_field])

        rows = [dict(stats, FILENAME=path) \
                for path, stats in rows_by_path.items()]

    if args.output:
        output_fp = open(args.output, 'w')
    else:
        output_fp = sys.stdout
    try:
        csv_writer = csv.DictWriter(output_fp, csv_fields)
        csv_writer.writeheader()
        csv_writer.writerows(rows)
    finally:
        output_fp.close()


if __name__ == '__main__':
    try:
        main()
    except IOError as ioe:
        if ioe.errno != errno.EPIPE:
            raise
