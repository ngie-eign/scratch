#!/bin/sh
#
# Run the TAHI p1/p2 tests in sequence. Nothing special here; just some simple
# canned commands.

set -e

if [ ! -f "Makefile.test" ]
then
	echo >&2 "${0##*/}: not in the Self_Test directory"
	exit 1
fi

run()
{
	[ -d ../$1 ] || mkdir ../$1
	: > ../$1/.w
	rm ../$1/.w
	make ipv6ready_${1}_host || :
	rm -Rf ../$1
	cp -Rf . ../$1
}
run "p1"
run "p2"
