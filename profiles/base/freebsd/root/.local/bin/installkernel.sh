#!/bin/sh

set -x

: "${SYSDIR=${PWD}/sys}"
SRCTOP="$(dirname "$(realpath "${SYSDIR}")")"

if [ -e "${SRCTOP}/.git" ] ; then
	if _git="$(which git)"; then
		git_cmd="${_git}"
	fi
fi

if [ -n "${git_cmd}" ] ; then
	git=$("${git_cmd}" rev-parse --verify --short HEAD 2>/dev/null)
	git_b="$("${git_cmd}" rev-parse --abbrev-ref HEAD)"
	if [ -n "${git_b}" ] ; then
		git="${git_b}"
	fi
	if "${git_cmd}" diff-index --name-only HEAD | read -r _dummy; then
		git="${git}-dirty"
	fi
fi
git="$(printf "%s" "${git:-}" | tr -d '[:space:]')"

: "${DESTDIR=/}"
export DESTDIR
: "${SRCCONF=/etc/src.conf}"

KERNCONFS="$(make -VKERNCONF -f "${SRCCONF}")"
: "${DEFAULT_KERNCONF="$(make -V'KERNCONF:[0]')"}"
VCS_VERSION="${git}"
[ -n "${VCS_VERSION}" ] && VCS_VERSION=".${VCS_VERSION}"
set -e
for _kc in ${KERNCONFS}; do
	instkernname="${_kc}${VCS_VERSION}"
	make installkernel INSTKERNNAME="${instkernname}" KERNCONF="${_kc}"
done
if [ -n "${DEFAULT_KERNCONF}" ]; then
	default_kern_name="${DEFAULT_KERNCONF}${VCS_VERSION}"

	if [ ! -d "${DESTDIR}/boot/${default_kern_name}" ]; then
		echo "${default_kern_name} not installed at ${DESTDIR}/boot/"
		exit 1
	fi

	ln -sfh "${default_kern_name}" "${DESTDIR}/boot/kernel"
fi
