#!/usr/bin/env python

import argparse
import os.path
import sqlite3
import sys
import xml.etree.ElementTree as ET

failure_href_prefix = 'javascript:showFailureSummary'

argparser = argparse.ArgumentParser()
argparser.add_argument('--build', required=True, type=int)
argparser.add_argument('--test-results-database', default='test_results.db',
                       required=True)
argparser.add_argument('--xml-file')

args = argparser.parse_args()

test_results_database = args.test_results_database
xml_file = args.xml_file if args.xml_file else '%d.xml' % (args.build, )

CREATE_RESULTS_TABLE_SQL = '''
CREATE TABLE results(
    build STRING NOT NULL,
    failed BOOLEAN,
    test_name STRING NOT NULL
);
'''

if not os.path.exists(test_results_database):
    with sqlite3.connect(test_results_database) as conn:
        cursor = conn.cursor()
        cursor.execute(CREATE_RESULTS_TABLE_SQL)

try:
    root = ET.parse(xml_file)
except ET.ParseError:
    sys.stderr.write('%s is malformed XML\n' % (xml_file, ))
    sys.exit(0)
failures = []
for a_node in root.iter('a'):
    if (a_node.attrib and
        a_node.attrib.get('href', '').startswith(failure_href_prefix)):
        test_name = os.path.dirname(a_node.attrib['id']).replace('test-', '', 1)
        failures.append(test_name)

if not failures:
    sys.exit(0)

with sqlite3.connect(test_results_database) as conn:
    cursor = conn.cursor()
    for failure in failures:
        cursor.execute('''INSERT INTO results VALUES (?, ?, ?)''',
                       (args.build, True, failure))
