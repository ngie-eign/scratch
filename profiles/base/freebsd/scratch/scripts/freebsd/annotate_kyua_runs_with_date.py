#!/usr/bin/env python
"""
 Copyright (c) 2015 EMC Corp.
 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:
 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

 THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
 FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 SUCH DAMAGE.

Examples:

    kyua report --results-filter failed | annotate_kyua_runs_with_date.py --start-time-format '%a %b %d %H:%M:%S %Y' --start-time 'Wed Apr 22 01:44:51 2015'

    annotate_kyua_runs_with_date.py --start-time-format '%a %b %d %H:%M:%S %Y' --start-time 'Wed Apr 22 01:44:51 2015' results.txt
"""


import optparse
import re
import sys
import time


DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def main(argv=None):
    parser = optparse.OptionParser(usage='usage: %prog [results.txt]')
    parser.add_option('--output-date-format', default=DEFAULT_DATE_FORMAT,
                      help=('time format to use for time output (see '
                            'strftime(3) for more details)'))
    parser.add_option('--start-time', default=None,
                      help='the time kyua was started')
    parser.add_option('--start-time-format', default=DEFAULT_DATE_FORMAT,
                      help=('time format to use for start time input (see '
                            'strftime(3) for more details)'))
    parser.add_option('--testcase-filter', dest='testcase_filter',
                      default='skipped,xfail,broken,failed,expected_failure,passed',
                      help=('testcase results to filter out (see man '
                            'kyua-report for more details). Default: '
                            '%default'))

    opts, args = parser.parse_args(argv)

    if len(args) > 1:
        parser.error('spurious arguments: %r' % (args, ))

    if not opts.start_time:
        parser.error('you must specify a start time with --start-time')

    output_date_format = opts.output_date_format
    start_time = opts.start_time
    start_time_format = opts.start_time_format
    testcase_filter = tuple(opts.testcase_filter.split(','))

    start_time_in_secs = time.mktime(time.strptime(start_time,
                                                   start_time_format))
    # Sanity check the output format
    time.strftime(output_date_format)

    try:
        if args:
            fd = open(args[0])
        else:
            fd = sys.stdin
        output = fd.read()
    finally:
        fd.close()

    result_re = re.compile(r'(\S+)\s+->\s+(.+)\s+\[(\d+\.\d+)s\]')
    time_elapsed = 0
    for line in output.splitlines():
        if '->' not in line:
            continue
        match = result_re.match(line.strip())
        if not match:
            continue
        tc_name, tc_result, tc_time_elapsed = match.groups()
        tc_time_elapsed = float(tc_time_elapsed)
        if tc_result.startswith(testcase_filter):
            tc_time_started_f = \
                time.localtime(start_time_in_secs + time_elapsed)
            tc_time_started_s = time.strftime(output_date_format,
                                              tc_time_started_f)
            sys.stdout.write('%s: %s -> %s [%s]\n'
                             % (tc_time_started_s, tc_name, tc_result,
                                tc_time_elapsed))
            sys.stdout.flush()
        time_elapsed += float(tc_time_elapsed)


if __name__ == '__main__':
    main()
