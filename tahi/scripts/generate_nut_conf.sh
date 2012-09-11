#!/bin/sh

readonly v6eval_etc_path=/usr/local/v6eval/etc

interface=$1
password=$2

err()
{
	echo "ERROR: $@"
	exit 1
}

if [ -z "$interface" -o -z "$password" ]
then
	err "usage: ${0##*/} interface-name password"
fi
macaddr=$(ifconfig $interface | awk '/ether/ { print $2 }')
if [ -z "$macaddr" ]
then
	err "No mac addr found for $interface!"
fi

set -e

nut_def="$v6eval_etc_path/nut.def"
cp $nut_def.sample $nut_def
sed -E -i '' -e "s/^(HostName[[:space:]]+)[^[:space:]]+\$/\1$(hostname)/" $nut_def
sed -E -i '' -e "s/^(Link0[[:space:]]+)fxp0+([[:space:]]+)[^[:space:]]+\$/\1$interface\2$macaddr/" $nut_def
sed -E -i '' -e "s/^(Password[[:space:]]+)[^[:space:]]+\$/\1$password/" $nut_def
