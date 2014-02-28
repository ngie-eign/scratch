#!/usr/bin/env python

from pubsubcommon import *

with kombu.Connection(**conn_dict) as conn:
    producer = conn.Producer()
    producer.publish(sys.stdin.read(),
                     exchange=exchange,
                     # XXX: why does this need to be here, i.e. why can't it
                     # be obtained from the exchange object?
                     routing_key=routing_key,
                     declare=[queue],
                     )
