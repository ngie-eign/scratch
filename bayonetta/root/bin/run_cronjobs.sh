#!/bin/sh
IFS="
"
for cmd in $(crontab -l | awk '$1 !~ /^#/ { l=""; for (i=6; i <= NF; i++) { l = l $i " "; } print l }')
do
	$cmd
done
