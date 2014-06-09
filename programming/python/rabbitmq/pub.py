#!/usr/bin/env python

from pubsubcommon import *
import sys

with kombu.Connection(**conn_dict) as conn:
    with conn.Producer(exchange=exchange,
                       routing_key=queue.routing_key,
                       ) as producer:
        producer.publish(sys.stdin.read(),
                         declare=[queue],
                         )
