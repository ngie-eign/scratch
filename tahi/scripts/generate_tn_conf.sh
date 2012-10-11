#!/bin/sh

readonly v6eval_etc_path=/usr/local/v6eval/etc

interface=$1

err()
{
	echo "ERROR: $@"
	exit 1
}

if [ -z "$interface" ]
then
	err "usage: ${0##*/} interface-name"
fi
macaddr=$(ifconfig $interface | awk '/ether/ { print $2 }')
if [ -z "$macaddr" ]
then
	err "No mac addr found for $interface!"
fi

set -e

ver=$(sysctl -n kern.osreldate)
tn_def="$v6eval_etc_path/tn.def"
cp $tn_def.sample $tn_def
if [ $ver -ge 800000 ]
then
	sed -i '' -e 's/cuad/cuau/g' $tn_def
fi

sed -E -i '' -e "/Link0/s/de0/$interface/" $tn_def
