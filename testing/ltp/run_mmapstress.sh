#!/bin/sh
#
# A script for running mmapstress from LTP on FreeBSD

filesystem_high_watermark()
{
	echo $(( $(df -k . | awk 'NR > 1 { print $4 }') * 1024 * 8 / 10 ))
}

random_offset()
{

	python2 -c "import os, random, sys
sys.stdout.write(str(int(0.75 * random.randrange($(filesystem_high_watermark)) / os.sysconf('SC_PAGE_SIZE')) * os.sysconf('SC_PAGE_SIZE')))
"
}

random_size()
{

	python2 -c "import random, sys
sys.stdout.write(str(int(0.75 * random.randrange($(filesystem_high_watermark)))))
"
}

random_time()
{
	python2 -c "import random, sys
sys.stdout.write(str(random.randrange(10)))
"
}

STANDALONE_PROGS="mmap-corruption01 mmapstress02 mmapstress03 mmapstress08"
PROGS="$STANDALONE_PROGS mmapstress01 mmapstress04"

run_random_test()
{
	local _test=$(python2 -c "import random, sys
sys.stdout.write(random.choice('$PROGS'.split()))
")

	case "$_test" in
	mmapstress01)
		./$_test -p $(sysctl -n kern.smp.cpus) -t $(random_time) -f $(random_size)
		;;
	mmapstress04)
		./$_test $(mktemp -u) $(random_offset)
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

PIDS=
kill_kids()
{
	echo "Will kill $PIDS"
	for pid in $PIDS; do
		kill $pid || kill -9 $pid
	done
}
trap kill_kids EXIT INT TERM

i=0
: ${NUM_TEST_PROCS=$(sysctl -n kern.smp.cpus)}
while [ $i -lt $NUM_TEST_PROCS ]; do
	spawn_tests &
	PIDS="$PIDS $!"
	: $(( i += 1 ))
done
wait
