#!/bin/sh

set -ex

: ${DESTDIR=/}
export DESTDIR

if which mergemaster 2>/dev/null; then
	mergemaster -iU -p -m $PWD -D $DESTDIR
else
	etcupdate -s $PWD -D $DESTDIR -p
fi
$(dirname $0)/installkernel.sh || exit
make installworld
etcupdate -s $PWD -D $DESTDIR -F
etcupdate resolve
