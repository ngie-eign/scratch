#!/bin/sh
#
# Demo showing that `var1` does not word split on the target shell.

var1="this variable has spaces in it"

case ${var1} in
*"has spaces in it")
	echo matched as expected
	;;
*)
	echo did not match as expected
	;;
esac
