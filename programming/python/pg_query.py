#!/usr/bin/env python
"""
Simple psycopg2 wrapper for querying databases.
"""

import os
import sys

import psycopg2 as pg

if len(sys.argv) not in (4, 5):
    sys.exit('%s host password [database] query'
             % (os.path.basename(sys.argv[0]), ))

conn_dict = dict(
    host=sys.argv[1],
    port='5432',
    user='postgres',
    password=sys.argv[2],
)

if len(sys.argv) == 4:
    query = sys.argv[3]
else:
    conn_dict['database'] = sys.argv[3]
    query = sys.argv[4]

conn = pg.connect(**conn_dict)
try:
    cursor = conn.cursor()
    cursor.execute(query)
    print(cursor.fetchall())
finally:
    conn.close()
