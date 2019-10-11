#!/bin/sh

: ${PORTSDIR=/usr/ports}

# "make patch" isn't available as a top-level target, so a little bit of Unix
# command-line golf is required to get the extracted/patched versions of
# ports.
#
# This is the first step to auditing for security vulnerabilities.
find ports -mindepth 3 -maxdepth 3 -name Makefile -exec dirname {} + | xargs -n 1 -I % make -C % patch
