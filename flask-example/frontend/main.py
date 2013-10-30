#!/usr/bin/env python
"""
Entry point for the view/controller for a project
"""

import frontend.forms as forms

if __name__ == '__main__':
    forms.app.run(host='0.0.0.0', port=80)
