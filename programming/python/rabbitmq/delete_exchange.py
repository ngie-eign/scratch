#!/usr/bin/env python

import os
import sys

import kombu

if len(sys.argv) != 5:
    sys.exit('usage: %s user password virtual-host' % (os.path.basename(sys.argv[0]), ))

conn_dict = {
    'hostname': 'localhost',
    'userid': sys.argv[1],
    'password': sys.argv[2],
    'virtual_host': sys.argv[3],
    'transport': 'pyamqp',
}
exchange_name = sys.argv[4]

with kombu.Connection(**conn_dict) as conn:
    exchange = kombu.Exchange(exchange_name, channel=conn)
    exchange.delete()
