#!/bin/sh

usage()
{
	cat <<EOF
usage: ${0##*/} [-u unit] [-v]
EOF
	exit 1
}

UNITS=$(cd /dev; ls mfi* | grep -v d | sed -e 's/mfi//g')
VERBOSE=false
while getopts 'v' optch
do
	case "$optch" in
	*u*)
		UNITS="$OPTARG"
		;;
	*v*)
		VERBOSE=true
		;;
	*)
		usage
		;;
	esac
done

for unit in $UNITS
do
	if ! drives="$(mfiutil -u $unit show drives)"
	then
		echo >&2 "Could not read drive state for unit $unit"
		continue
	fi
	unhealthy_drives="$(echo "$drives" |
			    awk '! /Physical/ { gsub(/\([^\)]+\)/, ""); print $1, $2 }' |
			    egrep -v 'COPYBACK|GOOD|JBOD|ONLINE|SPARE')"
	if [ -n "$unhealthy_drives" ]
	then
		cat >&2 <<EOF
The following drives are unhealthy for unit $unit

Drive	State
$unhealthy_drives
EOF
	else
		echo "All drives for controller $unit are healthy"
	fi
done
