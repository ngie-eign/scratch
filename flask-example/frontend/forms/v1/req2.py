#!/usr/bin/env python
"""
Request handler # 2

Garrett Cooper, October 2013
"""

import time
from flask import jsonify, request

from frontend.forms import app
from frontend.forms.v1 import api_version
from frontend.models.v1 import req2

@app.route('/%d/req2' % (api_version))
def req2():
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


