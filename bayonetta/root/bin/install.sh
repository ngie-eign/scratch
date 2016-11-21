#!/bin/sh

set -e

: ${DESTDIR=/}
export DESTDIR

mergemaster -iU -p -m $PWD -D $DESTDIR
$(dirname $0)/installkernel.sh || exit
make installworld
mergemaster -iU -m $PWD -D $DESTDIR
