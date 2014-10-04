#!/bin/sh
#
# A script for running mmapstress from LTP on FreeBSD

: ${PYTHON=python}

filesystem_high_watermark()
{
	echo $(( $(df -k . | awk 'NR > 1 { print $4 }') * 1024 * 8 / 10 ))
}

random_offset()
{

	$PYTHON -c "import os, random, sys
sys.stdout.write(str(min(1024 * 1024 * 1024, int(0.75 * random.randrange($(filesystem_high_watermark)) / os.sysconf('SC_PAGE_SIZE')) * os.sysconf('SC_PAGE_SIZE'))))
"
}

random_size()
{

	$PYTHON -c "import random, sys
sys.stdout.write(str(min(1024 * 1024 * 1024, int(0.75 * random.randrange($(filesystem_high_watermark))))))
"
}

random_minutes()
{
	$PYTHON -c "import random, sys
sys.stdout.write(str(random.randrange(1, 10)))
"
}

random_seconds()
{
	echo $(( $($PYTHON -c "import random, sys
sys.stdout.write(str(random.randrange(1, 60)))") * $(random_minutes) ))
}

STANDALONE_PROGS="mmap-corruption01 mmapstress02 mmapstress03 mmapstress08"
PROGS="$STANDALONE_PROGS mmapstress01 mmapstress04 mmapstress05 mmapstress06 mmapstress07 mmapstress09 mmapstress10"

run_random_test()
{
	local _test=$($PYTHON -c "import random, sys
sys.stdout.write(random.choice('$PROGS'.split()))
")

	case "$_test" in
	mmapstress01)
		./$_test -p $(sysctl -n kern.smp.cpus) -t $(random_minutes) -f $(random_size)
		;;
	mmapstress04)
		./$_test $(mktemp -u) $(random_offset)
		;;
	mmapstress06)
		./$_test $(random_seconds)
		;;
	mmapstress07)
		./$_test $(mktemp -u) $(random_offset) 1 $(random_offset)
		;;
	mmapstress09)
		./$_test -p $(sysctl -n kern.smp.cpus) -t $(random_minutes) -s $(random_size)
		;;
	mmapstress10)
		./$_test -f $(random_size) -p $(sysctl -n kern.smp.cpus) -t $(random_minutes) -f $(random_size) -S $(random_offset)
		;;
	*)
		./$_test
		;;
	esac
}

spawn_tests()
{
	while :; do
		run_random_test || break
	done
}

for prog in $PROGS; do
	if [ ! -x $prog ]; then
		echo "${0##*/}: ERROR missing program: $prog"
		exit 1
	fi
done

cleanup()
{
	trap "" EXIT INT TERM

	cleanup_kids
	cleanup_tmpdir
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

trap cleanup EXIT INT TERM

i=0
: ${NUM_TEST_PROCS=$(sysctl -n kern.smp.cpus)}
while [ $i -lt $NUM_TEST_PROCS ]; do
	spawn_tests &
	PIDS="$PIDS $!"
	: $(( i += 1 ))
done
wait
