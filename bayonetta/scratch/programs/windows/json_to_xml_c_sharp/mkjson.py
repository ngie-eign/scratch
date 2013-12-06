#!/usr/bin/env python

import json

print json.dumps({
    '?xml': {
        '@version': '1.0',
        '@standalone': 'no',
    },
    'root': {
        'person': [
          {
            '@id': '1',
            'name': 'alan',
            'url': 'http://www.google.com'
          },
          {
            '@id': '2',
            'name': 'louis',
            'url': 'http://www.yahoo.com'
          },
        ]
    }
}, indent=2, sort_keys=True)
