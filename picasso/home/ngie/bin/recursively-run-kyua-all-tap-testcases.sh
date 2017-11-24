#!/bin/sh

for i in $(find . -name Kyuafile)
do
	grep -q tap_test_program $i || continue
	(
	cd $(dirname $i)
	pwd
	kyua test
	)
done
