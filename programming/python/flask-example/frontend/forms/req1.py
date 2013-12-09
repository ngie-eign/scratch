#!/usr/bin/env python
"""
Request Handler # 1

Garrett Cooper, October 2013
"""

import time

from frontend.forms import app, get_json_from_api

@app.route('/<int:api_version>/req1')
def req1(api_version):
    # 1. Grab the request.
    # 2. Punt it over to the model logic
    # 3. Present the result.
    return get_json_from_api(api_version)
