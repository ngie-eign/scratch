#!/usr/bin/env python

from argparse import ArgumentParser

import kombu

parser = ArgumentParser()
parser.add_argument('--exchange',
                    )
parser.add_argument('--queue',
                    required=True,
                    )
parser.add_argument('--password',
                    )
parser.add_argument('--routing-key',
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

queue_kwargs = {}

if args.exchange:
    queue_kwargs['exchange'] = exchange = \
        kombu.Exchange(name=args.exchange,
                       delivery_mode=kombu.Exchange.PERSISTENT_DELIVERY_MODE,
                       durable=True,
                       type='direct',
                       )
else:
    exchange = None

if args.routing_key:
    queue_kwargs['routing_key'] = routing_key = args.routing_key
else:
    routing_key = None

queue_kwargs['name'] = args.queue

queue = kombu.Queue(**queue_kwargs)
