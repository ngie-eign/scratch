#!/usr/bin/env python

import getpass
import optparse


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
                  dest='queue_name',
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

exchange_kwargs = {
    'delivery_mode': kombu.Exchange.PERSISTENT_DELIVERY_MODE,
}

queue_args = [
    opts.queue_name,
]
queue_kwargs = {
    'exchange_opts': exchange_kwargs,
}


with kombu.Connection(**conn_dict) as conn:
    simple_queue = conn.SimpleQueue(*queue_args, **queue_kwargs)
    # If empty, raises Queue.Empty().
    message = simple_queue.get(block=True, timeout=1)
    print('Received %s' % (message.payload, ))
    # No ACK - message still in queue, as expected.
    message.ack()
    simple_queue.close()
