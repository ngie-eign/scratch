#!/bin/sh

set -eu

max_workers=10
dir_path=$(realpath "$1")
set -- $(find "$dir_path" -type f -name \*.html)
while [ $# -gt 0 ]; do
	allocated_workers=0
	set +u
	for i in $(seq 1 $max_workers); do
		html_file=$1; shift
		if [ $# -gt 0 ]; then
			./parse_synopsis_from_openssl_html_manpage.py $html_file ${html_file%.html*}.txt &
			: $(( allocated_workers += 1 ))
		fi
	done
	for i in $(seq 1 $allocated_workers); do
		wait
	done
done
