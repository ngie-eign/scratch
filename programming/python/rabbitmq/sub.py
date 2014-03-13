#!/usr/bin/env python

import sys

from pubsubcommon import *

def callback(body, message):
    sys.stdout.write('Message received was: %s\n' % (body, ))
    message.ack()


while True:
    with kombu.Connection(**conn_dict) as conn:
        with conn.Consumer(queue, callbacks=[callback]):
            for _ in kombu.eventloop(conn, timeout=None):
                pass
