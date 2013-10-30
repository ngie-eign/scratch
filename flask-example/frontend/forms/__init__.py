from flask import Flask

app = Flask(__name__)

VALID_API_VERSIONS = (1, )

def valid_api_version(version):
    if version in VALID_API_VERSIONS:
        return True
    return False

import frontend.forms.req1
import frontend.forms.req2
