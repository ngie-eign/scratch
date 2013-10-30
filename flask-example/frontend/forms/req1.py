#!/usr/bin/env python
"""
Request Handler # 1

Garrett Cooper, October 2013
"""

import time
from flask import jsonify

from frontend.forms import app, valid_api_version

@app.route('/<int:api_version>/req1')
def req1(api_version):
    if valid_api_version(api_version):
        status = 'aok'
    else:
        status = 'sadtrombone.com'
    d = {
        'status': status,
        'time': time.clock(),
        'version': api_version,
        'my': 'precious...',
    }
    return jsonify(d)


