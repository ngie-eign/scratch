#!/usr/bin/env python
"""
Request Handler # 1

Garrett Cooper, October 2013
"""

import time
from flask import jsonify

from frontend.forms import app
from frontend.forms.v1 import api_version
from frontend.models.v1 import req1

@app.route('/%d/req1' % (api_version))
def req1():
    d = {
        'time': time.clock(),
        'version': api_version,
        'my': 'precious...',
    }
    return jsonify(d)


