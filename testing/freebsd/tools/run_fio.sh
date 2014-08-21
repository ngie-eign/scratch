#!/bin/sh
#
# usage: run_fio.sh device|file ...

: ${PYTHON=python}

random_bs()
{
	$PYTHON -c 'import random, sys;
sys.stdout.write(str(random.randrange(512, 10241)))'
}

random_io_engine()
{
	$PYTHON -c 'import random, sys;
rw_choices = "mmap posixaio psync pvsync sync vsync".split();
sys.stdout.write(random.choice(rw_choices))'
}

random_io_operation()
{
	$PYTHON -c 'import random, sys;
rw_choices = "read write randwrite randread randrw".split();
sys.stdout.write(random.choice(rw_choices))'
}

random_size()
{
	local size

	$need_size || return

	size=$($PYTHON -c 'import random, sys;
sys.stdout.write(str(random.randrange(1, 1024 * 1024)))')
	echo "size=$size"
}

if ! command -v fio; then
	echo "${0##*/}: ERROR: please install fio"
	exit 1
fi

need_size=false
for path in $*; do
	if [ -c $path ]; then
		:
	else
		if [ ! -e $path ] && ! : > $path; then
			echo "${0##*/}: ERROR: could not create path: $path"
			exit 1
		fi
		need_size=true
	fi
	PATHS="${PATHS:+$PATHS:}$path"
done

echo $PATHS; 
: ${NUM_JOBS=$(sysctl -n kern.smp.cpus)}

JOBFILE=fio.job
while :; do
	cat > $JOBFILE <<EOF
[jobs]
filename=$PATHS
ioengine=$(random_io_engine)
rw=$(random_io_operation)
numjobs=$NUM_JOBS
bs=$(random_bs)
$(random_size)
EOF

	echo ">>>> START $JOBFILE <<<<"
	cat $JOBFILE
	echo ">>>> END $JOBFILE <<<<"

	fio $JOBFILE
done
