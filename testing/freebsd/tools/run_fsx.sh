#!/bin/sh

: ${PYTHON=python}

random_operations()
{
	$PYTHON -c "import random, sys
sys.stdout.write(str(random.randrange(1, 1024 ** 3)))
"
}

spawn_tests()
{
	while :; do
		fsx -N $(random_operations) $(mktemp $TMPDIR/fsxfile.XXXXXX)
	done
}

cleanup()
{
	trap "" EXIT INT TERM

	cleanup_kids
	cleanup_tmpdir

	trap - EXIT INT TERM
}

PIDS=
cleanup_kids()
{
	[ -n "$PIDS" ] || return 0

	echo "Will kill${PIDS}"
	for pid in $PIDS; do
		kill $pid 2>/dev/null || kill -9 $pid
	done
}

: ${TMPDIR=$(mktemp -d fsx.XXXXXXX)}
cleanup_tmpdir()
{
	cd /
	rm -Rf $TMPDIR
}

trap cleanup EXIT INT TERM

i=0
: ${NUM_TEST_PROCS=$(sysctl -n kern.smp.cpus)}
while [ $i -lt $NUM_TEST_PROCS ]; do
	spawn_tests &
	PIDS="$PIDS $!"
	: $(( i += 1 ))
done
wait
