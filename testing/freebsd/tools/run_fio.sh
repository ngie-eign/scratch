#!/bin/sh

: ${PYTHON=python}

random_io_operation()
{
	$PYTHON -c 'import random, sys;
rw_choices = "read write randwrite randread rw,readwrite randrw".split()
sys.stdout.write(random.choice(rw.choices))'
}

JOBS=$(sysctl -n kern.smp.cpus)
while :; do
	cat > fio.job <<EOF
[jobs]
filename=/dev/da1
rw=$(random_io_operation)
numjobs=$NUM_JOBS
bs=10m
EOF
	fio fio.job
done
