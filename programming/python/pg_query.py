#!/usr/bin/env python
"""
Simple psycopg2 wrapper for querying databases.
"""

import argparse
import os
import sys

import psycopg2 as pg

parser = argparse.ArgumentParser()
parser.add_argument('--database')
parser.add_argument('--host')
parser.add_argument('--password')
parser.add_argument('query')
args = parser.parse_args()

if len(sys.argv) not in (4, 5):
    sys.exit('%s host password [database] query'
             % (os.path.basename(sys.argv[0]), ))

conn_dict = dict(
    database=args.database,
    host=args.host,
    port='5432',
    user='postgres',
    password=args.password,
)

with pg.connect(**conn_dict) as conn:
    cursor = conn.cursor()
    cursor.execute(args.query)
    if cursor.rowcount:
        sys.stdout.write('%r\n' % (cursor.fetchall(), ))
