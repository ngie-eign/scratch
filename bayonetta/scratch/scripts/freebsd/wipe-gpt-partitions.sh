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

# Recovery partitions are fun when wiping out disks. If FreeBSD finds the
# recovery partition, but doesn't find a correct partition table, or finds
# a corrupt partition table at the beginning sectors of the disk, it will
# try and use whatever the recovery partition says should be there, which
# could be horribly wrong if the disk was used after the fact
#
# This script's purpose is to wipe out GPT partitions, so we want to make
# sure the primary and recovery partition tables are toast.
#
# The oseek is there to avoid having to wipe the entire disk to get to the
# recovery partition (which can take a long time on large spinning disks)
#
# Relevant reading:
# - http://serverfault.com/questions/666886/gpt-partition-errors-on-boot-zfs-freebsd
# - https://forums.freenas.org/index.php?threads/gpt-table-is-corrupt-or-invalid-error-on-bootup.12171/

# Avoid precision error dividing by 1MB
mediasize_in_bytes=$(diskinfo -v $diskdev | awk '/mediasize in bytes/ { print $1 }')
oseek_in_mb=$(( $(( $mediasize_in_bytes - 10 * $MB )) / $MB ))

# Get rid of the partition at the front of the disk; yes, this is overkill
dd if=/dev/zero of=$diskdev bs=1m count=1

# Wipe out the recovery partition
dd if=/dev/zero of=$diskdev bs=1m oseek=$oseek_in_mb
