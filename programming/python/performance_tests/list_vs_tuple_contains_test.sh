#!/bin/sh
#
# `tuple.__contains__` is generally faster than `list.__contains__` in python because
# tuples are immutable data structures:
# https://stackoverflow.com/questions/68630/are-tuples-more-efficient-than-lists-in-python
#
# There are other older articles out there that say the same/similar, but the
# prior link is a nicely summarized StackOverflow post.

BINDIR=$(dirname $0) || exit
. "$(dirname $0)/perflib.sh"

system_summary

info "list.__contains__"
run_timeit -s "import random; VALUES = [random.randrange(10000) for i in range(1000)]; NEEDLE = VALUES[-1]" "NEEDLE in VALUES"

info "tuple.__contains__"
run_timeit -s "import random; VALUES = tuple([random.randrange(10000) for i in range(1000)]); NEEDLE = VALUES[-1]" "NEEDLE in VALUES"
