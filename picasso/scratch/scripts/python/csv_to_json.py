#!/usr/bin/env python

import csv
import json
import sys

json_dict = {}
reader = csv.reader(sys.stdin)
json_dict = dict([(key, value) for key, value in reader])
sys.stdout.write(json.dumps(json_dict, indent=4))
