#!/usr/bin/env python
"""
Request handler # 2

Garrett Cooper, October 2013
"""

import time
from flask import jsonify, request

from frontend.forms import app

@app.route('/<int:api_version>/req2')
def req2(api_version):
    d = {
        'time': time.clock(),
        'version': api_version,
    }
    if request.args.get('action', None) == 'gets_me_a_string':
        d['foo'] = 'foo'
        d['a'] = list('abcd')
    else:
        d['error'] = 'INVALID REQUEST!'
    return jsonify(d)


