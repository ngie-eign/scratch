#!/usr/bin/env python

import os
import sys

import kombu

def usage():
    sys.exit('usage: %s [exchange|queue] user password virtual-host'
             % (os.path.basename(sys.argv[0]), ))


if len(sys.argv) != 6:
    usage()

objname = sys.argv[1].capitalize()
if objname not in ('Exchange', 'Queue', ):
    usage()

conn_dict = {
    'hostname': 'localhost',
    'userid': sys.argv[2],
    'password': sys.argv[3],
    'virtual_host': sys.argv[4],
    'transport': 'pyamqp',
}
name = sys.argv[5]

with kombu.Connection(**conn_dict) as conn:
    obj = getattr(kombu, objname)(name, channel=conn)
    obj.delete()
