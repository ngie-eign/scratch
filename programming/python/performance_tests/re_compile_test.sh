#!/bin/sh

BINDIR=$(dirname $0) || exit
. "$(dirname $0)/perflib.sh"

NEEDLE=$(mktemp -u)
HAYSTACK=$(mktemp -u)
trap "rm -f '$HAYSTACK' '$NEEDLE'" EXIT INT TERM

seq 1 1024 | tr -d ' ' | dd of="$NEEDLE" bs=1k 2>/dev/null || exit
dd if=/dev/urandom bs=128M of="$HAYSTACK" count=1 2>/dev/null

system_summary

info "Without precompiled regex."
run_timeit -s "import re; HAYSTACK = open('$HAYSTACK', 'rb').read(); NEEDLE = re.escape(open('$NEEDLE', 'rb').read())" "re.match(NEEDLE, HAYSTACK)"

info "With precompiled regex."
run_timeit -s "import re; HAYSTACK = open('$HAYSTACK', 'rb').read(); NEEDLE_re = re.compile(re.escape(open('$NEEDLE', 'rb').read()))" "NEEDLE_re.match(HAYSTACK)"
