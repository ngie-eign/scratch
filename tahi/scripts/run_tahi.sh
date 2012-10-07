#!/bin/sh
#
# Run the TAHI p1/p2 tests in sequence. Nothing special here; just some simple
# canned commands.

# Check to make sure the directories can be shuffled, run the tests, and
# shuffle the results to the right directory once done.
#
# Parameters:
# 1 - phase
# 2 - type (host, router, special)
run()
{
	local phase=$1
	local type=$2

	# Phase directory.
	pdir=../$phase
	# Prereq checks (see if the directory is writable, etc).
	set -e
	[ -d $pdir ] || mkdir $pdir # Make sure the directory exists.
	: > $pdir/.w # Truncate a file in the directory (writable).
	rm $pdir/.w # Clean it up after we're done.
	set +e
	# Run the test.
	make ipv6ready_${phase}_${type}
	# Shuffle the results around.
	rm -Rf $pdir
	cp -Rf . $pdir
}

if ! make -f Makefile.test -n ipv6ready_p1_host >/dev/null 2>&1
then
	echo >&2 "${0##*/}: this must be run from Self_Test directory"
	exit 1
fi

if [ $# -eq 0 ]
then
	type=host
else
	case "$1" in
	host|router|special)
		type=$1
		;;
	*)
		cat >&2 <<EOF
	usage: ${0##*/}: [host|router|special]

	Defaults to host.
EOF
		exit 1
		;;
	esac
fi
run "p1" "$type"
if [ "$type" != "special" ]
then
	run "p2" "$type"
fi
