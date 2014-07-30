#!/bin/sh

if [ -z "$PPID" -o $PPID -le 0 ]
then
	echo "${0##*/}: ERROR: \$PPID is either undefined or less than 0"
	exit 1
fi

# Protect this script from the OOM and its parent
if protect -p $PPID
then
	# Remove protection after we're done
	trap "protect -c -p $PPID"
else
	echo "${0##*/}: WARNING: calling protect(8) failed; this script might be killed by the OOM later"
fi

for i in mmap*.sh; do
	echo "Running $i"
	protect sh ./$i
done
