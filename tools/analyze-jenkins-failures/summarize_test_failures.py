#!/usr/bin/env python

import argparse
import sqlite3
import sys

argparser = argparse.ArgumentParser()
argparser.add_argument('--test-results-database', required=True)

args = argparser.parse_args()

test_results_database = args.test_results_database

def pretty_subrange(start, end):
    if start == end:
        return str(start)
    else:
        return '%d-%d' % (start, end, )

def pretty_range(builds):
    if not builds:
        return ''
    if len(builds) <= 2:
        # No sense making this more complicated than it needs to be for less
        # than 3 builds
        return map(str, builds)

    build_range = []
    is_contiguous = False
    range_start = 0
    for i in xrange(len(builds) - 1):
        if range_start == i:
            continue # Don't check yourself
        if builds[i] + 1 == builds[i + 1]:
            is_contiguous = True
        else:
            if is_contiguous: # Dump out the subrange
                start = builds[range_start]
                end = builds[i]
            else: # Dump out just one value
                start = end = builds[range_start]
            build_range.append(pretty_subrange(start, end))
            range_start = i + 1

    build_range.append(pretty_subrange(builds[range_start], builds[-1]))

    return build_range

SELECT_BUILD_FROM_FAILED_TEST_SQL = '''
SELECT build FROM results WHERE failed AND test_name=? ORDER BY build;
'''
with sqlite3.connect(test_results_database) as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT test_name FROM results WHERE failed')
    failed_tests = sorted(set([failed_test for failed_test, in cursor]))
    for failed_test in failed_tests:
        cursor.execute(SELECT_BUILD_FROM_FAILED_TEST_SQL, (failed_test, ))
        failed_builds = [build for build, in cursor]
        sys.stdout.write('Test = %s, Failed builds = %s\n' % \
                         (failed_test,
                         ', '.join(pretty_range(failed_builds))))
