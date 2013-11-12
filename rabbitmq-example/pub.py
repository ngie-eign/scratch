#!/usr/bin/env python

import getpass
import optparse
import sys

import kombu

parser = optparse.OptionParser()
parser.add_option('--password',
                  default='guest',
                  dest='password',
                  help='RabbitMQ password')
parser.add_option('--port',
                  default=5672,
                  dest='port',
                  type='int',
                  help='RabbitMQ port')
parser.add_option('--queue',
                  default='test',
                  dest='queue',
                  help='Queue to use when pub/sub\'ing')
parser.add_option('--routing-key',
                  default='test',
                  dest='routing_key',
                  help='Routing key to use when pub/sub\'ing')
parser.add_option('--server',
                  default='localhost',
                  dest='server',
                  help='RabbitMQ server')
parser.add_option('--username',
                  default='guest',
                  dest='username',
                  help='RabbitMQ username')
opts, __ = parser.parse_args()

conn_dict = {
    'hostname': opts.server,
    'password': opts.password,
    'port': opts.port,
    'ssl': False,
    'userid': opts.username,
}
conn_str = 'amqp://%(userid)s:%(password)s@%(hostname)s:%(port)d//' % conn_dict
msg = sys.stdin.read()
with kombu.Connection(**conn_dict) as conn:
    simple_queue = conn.SimpleQueue(opts.queue)
    simple_queue.put(msg)
    print('Sent %s' % (msg, ))
    simple_queue.close()
