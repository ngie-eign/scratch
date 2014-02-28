#!/usr/bin/env python

from argparse import ArgumentParser
import os
import sys

import kombu

parser = ArgumentParser()
parser.add_argument('--name',
                    )
parser.add_argument('--password',
                    )
parser.add_argument('--type',
                    choices=('Exchange', 'Queue'),
                    required=True,
                    )
parser.add_argument('--user',
                    )
parser.add_argument('--virtual-host',
                    )
args = parser.parse_args()

conn_dict = {
    'hostname': 'localhost',
    'userid': args.user,
    'password': args.password,
    'virtual_host': args.virtual_host,
    'transport': 'pyamqp',
}
name = args.name

with kombu.Connection(**conn_dict) as conn:
    obj = getattr(kombu, args.type)(name, channel=conn)
    obj.delete()
