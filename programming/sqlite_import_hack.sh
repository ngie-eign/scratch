#!/bin/sh

set -eu

db=$1
csv=$2
table=$3

IFS="
"
while read line
do
	if [ -z "${header:-}" ]
	then
		header=$line
	else
		sqlite3 $db "INSERT INTO $table($header) VALUES($line)"
	fi
done < $csv
