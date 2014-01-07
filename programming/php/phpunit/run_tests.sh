#!/bin/sh
#
# Why write a wrapper script to run phpunit? Because:
# http://stackoverflow.com/questions/1988768/testing-multiple-classes-with-phpunit?answertab=votes#tab-top

for f in `grep --include \*.php -lr 'PHPUnit_Framework_TestCase' .`
do
	for c in `grep PHPUnit_Framework_TestCase $f | awk '/extends.*PHPUnit_Framework_TestCase/ { print $2 }'`
	do
		echo "$f $c..."
		phpunit --verbose $c $f
	done
done
