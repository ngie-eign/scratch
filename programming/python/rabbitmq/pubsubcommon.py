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
    exchange_args = [
        args.exchange,
        'direct',
    ]

    exchange_kwargs = {
        'durable': True,
    }

    queue_kwargs['exchange'] = exchange = kombu.Exchange(*exchange_args,
                                                         **exchange_kwargs)
    queue_kwargs['exchange_opts'] = {
        'delivery_mode': kombu.Exchange.PERSISTENT_DELIVERY_MODE,
    }
else:
    exchange = None

if args.routing_key:
    queue_kwargs['routing_key'] = routing_key = args.routing_key
else:
    routing_key = None

queue_args = [
    args.queue,
]

queue = kombu.Queue(*queue_args, **queue_kwargs)
