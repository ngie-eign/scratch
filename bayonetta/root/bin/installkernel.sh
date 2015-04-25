#!/bin/sh

set -x

: ${SYSDIR=$PWD/sys}

for dir in /usr/bin /usr/local/bin; do
	if [ ! -z "${svnversion}" ] ; then
		break
	fi
	if [ -x "${dir}/svnversion" ] && [ -z ${svnversion} ] ; then
		# Run svnversion from ${dir} on this script; if return code
		# is not zero, the checkout might not be compatible with the
		# svnversion being used.
		${dir}/svnversion $(realpath ${0}) >/dev/null 2>&1
		if [ $? -eq 0 ]; then
			svnversion=${dir}/svnversion
			break
		fi
	fi
done

if [ -z "${svnversion}" ] && [ -x /usr/bin/svnliteversion ] ; then
	/usr/bin/svnliteversion $(realpath ${0}) >/dev/null 2>&1
	if [ $? -eq 0 ]; then
		svnversion=/usr/bin/svnliteversion
	else
		svnversion=
	fi
fi

if [ -d "${SYSDIR}/../.git" ] ; then
	for dir in /usr/bin /usr/local/bin; do
		if [ -x "${dir}/git" ] ; then
			git_cmd="${dir}/git --git-dir=${SYSDIR}/../.git"
			break
		fi
	done
fi

if [ -n "$svnversion" ] ; then
	svn=`cd ${SYSDIR} && $svnversion 2>/dev/null`
	case "$svn" in
	[0-9]*)	svn="r${svn}" ;;
	*)	unset svn ;;
	esac
fi

if [ -n "$git_cmd" ] ; then
	git=`$git_cmd rev-parse --verify --short HEAD 2>/dev/null`
	svn=`$git_cmd svn find-rev $git 2>/dev/null`
	if [ -n "$svn" ] ; then
		svn="r${svn}"
		git="=${git}"
	else
		svn=`$git_cmd log | fgrep 'git-svn-id:' | head -1 | \
		     sed -n 's/^.*@\([0-9][0-9]*\).*$/\1/p'`
		if [ -z "$svn" ] ; then
			svn=`$git_cmd log --format='format:%N' | \
			     grep '^svn ' | head -1 | \
			     sed -n 's/^.*revision=\([0-9][0-9]*\).*$/\1/p'`
		fi
		if [ -n "$svn" ] ; then
			svn="r${svn}"
			git="+${git}"
		else
			git=" ${git}"
		fi
	fi
	git_b=`$git_cmd rev-parse --abbrev-ref HEAD`
	if [ -n "$git_b" ] ; then
		git="${git}(${git_b})"
	fi
	if $git_cmd --work-tree=${SYSDIR}/.. diff-index \
	    --name-only HEAD | read dummy; then
		git="${git}-dirty"
	fi
fi

[ -n "$svn" ] && rev="$svn"
[ -n "$git" ] && rev="$git"

: ${DESTDIR=/}
export DESTDIR
: ${SRCCONF=/etc/src.conf}

set -e
for _kc in $(make -VKERNCONF -f $SRCCONF)
do
	make installkernel INSTKERNNAME="$_kc.$rev" KERNCONF=$_kc
done
