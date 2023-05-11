#!/usr/bin/env python3
import argparse
import hmac
import sys

SHORT_KEY = b"this is a passcode"
LONG_KEY = b"this is a SUPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPER LONG passcode"

parser = argparse.ArgumentParser()
parser.add_argument("--short", action="store_true", dest="want_short_key")
parser.add_argument("--long", action="store_false", dest="want_short_key")
args = parser.parse_args()

key = SHORT_KEY if args.want_short_key else LONG_KEY

text = b"abcdefghijklmnop"
hexdigest_len = 12

print("key:", key.decode())
print("text:", text.decode())
print("digest:", hmac.new(key, text, "MD5").hexdigest()[:hexdigest_len])
