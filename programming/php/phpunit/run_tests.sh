#!/bin/sh

for f in `grep --include \*.php -lr 'PHPUnit_Framework_TestCase' .`
do
	for c in `grep PHPUnit_Framework_TestCase $f | awk '/extends.*PHPUnit_Framework_TestCase/ { print $2 }'`
	do
		echo "$f $c..."
		phpunit --verbose $c $f
	done
done
