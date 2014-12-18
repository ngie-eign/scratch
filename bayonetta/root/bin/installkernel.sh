#!/bin/sh

set -x

git=`git rev-parse --verify --short HEAD 2>/dev/null`
svn=$(git svn find-rev $git 2>/dev/null)
if [ -n "$svn" ] ; then
	git="=${git}"
else
	svn=`git log | fgrep 'git-svn-id:' | head -1 | \
	     sed -n 's/^.*@\([0-9][0-9]*\).*$/\1/p'`
	if [ -n "$svn" ] ; then
		git="+${git}"
	else
		git="${git}"
	fi
fi
: ${SYSDIR=$PWD/sys}
if git --work-tree=${SYSDIR}/.. diff-index \
    --name-only HEAD | read dummy; then
	git="${git}-dirty"
fi
rev="${svn:+r$svn}$git"

: ${DESTDIR=/}
export DESTDIR

set -e
for _kc in $(make -VKERNCONF)
do
	make installkernel INSTKERNNAME="$_kc.$rev" KERNCONF=$_kc
done
