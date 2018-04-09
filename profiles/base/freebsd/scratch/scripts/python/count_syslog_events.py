#!/usr/bin/env python
"""
Script for counting events in syslog to help analyze how many times an event
has occurred.

How to use this:
1. Strip all variable data from the syslog output (dates, unique identifiers,
   etc).
2. Call the script with the filtered output like so:
   python ./count_syslog_events.py < filtered.log

This will dump out a table of events and messages.

Ngie Cooper, November 2013
"""

import hashlib
import sys
d = {}
hashes = {}
for line in sys.stdin.readlines():
    service, message = line.split('ERROR:')
    message = message.strip()
    service = service.strip().replace(' ', '.')
    _hash = hashlib.md5(message).hexdigest()
    if _hash not in hashes:
        hashes[_hash] = message
    key = (service, _hash, )
    if key not in d:
        d[key] = 1
    else:
        d[key] += 1

def fmt(count, service, _hash):
    return ' | '.join(['%06d  ' % count, service.replace(' ', '.'), _hash])

print(' | '.join(['Count   ', 'Service', 'Event ID']))
print('-' * 80)
print('\n'.join(sorted([fmt(count, *key) for key, count in d.iteritems()],
                       reverse=True)))
print('')
print('-' * 80)
print(' | '.join(['Event ID', 'Event']))
print('-' * 80)
for _hash, phrase in hashes.iteritems():
    print(_hash)
    print(phrase)
    print('')
