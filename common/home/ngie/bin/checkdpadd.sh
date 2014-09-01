#!/bin/sh

#set -a
#eval `grep LD share/mk/src.libnames.mk | sed -e 's,?,,g' -e 's,=.*/lib,=-l,' -e 's,\..*,,g'`
#set +a
script checkdpadd.script make checkdpadd
grep -B 2 LDADD checkdpadd.script | less
