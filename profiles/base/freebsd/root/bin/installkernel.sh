#!/bin/sh

set -x

: ${SYSDIR=$PWD/sys}

if [ -d "${SYSDIR}/../.git" ] ; then
	for dir in /usr/bin /usr/local/bin; do
		if [ -x "${dir}/git" ] ; then
			git_cmd="${dir}/git --git-dir=${SYSDIR}/../.git"
			break
		fi
	done
fi

if [ -n "$git_cmd" ] ; then
	git=`$git_cmd rev-parse --verify --short HEAD 2>/dev/null`
	git_b=`$git_cmd rev-parse --abbrev-ref HEAD`
	if [ -n "$git_b" ] ; then
		git="${git}"
	fi
	if $git_cmd --work-tree=${SYSDIR}/.. diff-index \
	    --name-only HEAD | read dummy; then
		git="${git}-dirty"
	fi
fi
git=$(echo -n "${git:-}" | sed -e 's, ,,g')

: ${DESTDIR=/}
export DESTDIR
: ${SRCCONF=/etc/src.conf}

KERNCONF=$(make -VKERNCONF -f $SRCCONF)
KERNCONF=${KERNCONF:-GENERIC}
VCS_VERSION="${git:-$git}"
[ -n "$VCS_VERSION" ] && VCS_VERSION=".${VCS_VERSION}"
set -e
for _kc in ${KERNCONF}; do
	instkernname=$_kc${VCS_VERSION}
	make installkernel INSTKERNNAME="$instkernname" KERNCONF=$_kc
done
if [ -n "${DEFAULT_KERNCONF}" ]; then
	default_kern_name=${DEFAULT_KERNCONF}.${svn:-$svn}${git:-$git}

	if [ ! -d "${DESTDIR}/boot/${default_kern_name}" ]; then
		echo "${default_kern_name} not installed at ${DESTDIR}/boot/"
		exit 1
	fi

	ln -sfh ${default_kern_name} ${DESTDIR}/boot/kernel
fi
