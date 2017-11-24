#!/bin/sh

cd /usr/lib/debug/
find boot/ -type d -maxdepth 1 -mindepth 1 | \
while read d; do
	[ -d /$d ] || rm -Rf $d
done
