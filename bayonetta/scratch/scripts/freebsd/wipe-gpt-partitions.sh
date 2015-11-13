#!/bin/sh
#
# Example:
#	./wipe-gpt-partitions.sh da0
#
# Requires FreeBSD 9.x+

MB=$(( 1024 * 1024 ))

disk=$1
diskdev=/dev/$1
if [ -z "$disk" -o ! -c $diskdev ]; then
	echo "${0##*/}: ERROR: you must specify a disk that exists"
	exit 1
fi

set -e

# Wipe out the GPT partition the "nice" way; don't worry about errors here.
# We'll error out below with diskinfo if this fails
gpart destroy -F $disk || :

# Avoid precision error dividing by 1MB and ensuring
mediasize_in_bytes=$(diskinfo -v $diskdev | awk '/mediasize in bytes/ { print $1 }')
oseek_in_mb=$(( $(( $mediasize_in_bytes - 10 * $MB )) / $MB ))

# Get rid of the partition at the front of the disk; yes, this is overkill
dd if=/dev/zero of=$diskdev bs=1m count=1

# Wipe out the recovery partition
dd if=/dev/zero of=$diskdev bs=1m oseek=$oseek_in_mb
