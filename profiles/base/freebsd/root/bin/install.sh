#!/bin/sh

set -ex

: ${DESTDIR=/}
export DESTDIR

mergemaster -iU -p -m $PWD -D $DESTDIR
$(dirname $0)/installkernel.sh || exit
make installworld
etcupdate -s $PWD -D $DESTDIR -F
etcupdate resolve
