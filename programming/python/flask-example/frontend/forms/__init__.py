"""
TODO:
1. Write a decorator for noting that app.route is JSON format.
2. Write a decorator for noting that app.route is API versioned.
3. Using 2., better hide/tie get_json_from_api to source code instead as this
   is really clunky right now.
"""

import importlib
from importlib.util import spec_from_file_location
import inspect
import logging

from flask import Flask, jsonify, request

import frontend.settings as settings

app = Flask(__name__)

# The gist of any call from the forms to the models should be something like:
# 1. Grab the request (flask)
# 2. Punt it over to the model logic (us)
# 3. Present the result (us->flask)
def form_to_model(api_version, stack=1):
    """Convert a form name to a model name"""

    frame_record = inspect.getouterframes(inspect.currentframe())[stack]
    form_module = inspect.getmodulename(frame_record.filename)
    model_module = importlib.import_module(
        ".%s" % (form_module), "frontend.models.v%d" % (api_version)
    )
    model_func = getattr(model_module, frame_record.function)

    return model_func


# This function makes item 2. noted above a bit more transparent.
#
# NOTES:
# - The adds 1 to the stack (hence stack=2).
#
# XXX: this probably should be made transparent via a decorator pattern, but I
#      need to write another decorator to make versioned APIs transparent
#      first.
def get_json_from_api(api_version):

    model_callee = form_to_model(api_version, stack=2)

    return jsonify(model_callee(**dict(request.args)))


import frontend.forms.req1
import frontend.forms.req2
