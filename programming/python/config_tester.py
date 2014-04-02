#!/usr/bin/env python

from ConfigParser import ConfigParser
import os
import sys
import tempfile

temp_file = tempfile.NamedTemporaryFile(delete=False)
try:
    try:
        temp_file.write('''
[section1]
foo: true
bar: false

[section2]
foo=true
bar=false
''')
    finally:
        temp_file.close()

    cp = ConfigParser()
    if not cp.read(temp_file.name):
        sys.exit('Could not read %s' % (temp_file.name, ))
    for section in cp.sections():
        print('%s: %s' % (section, cp.items(section), ))
    for section in cp.sections():
        print('%s: %s' % (section, cp.getboolean(section, 'foo'), ))

finally:
    os.unlink(temp_file.name)
