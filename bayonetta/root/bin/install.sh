#!/bin/sh

set -e

: ${DESTDIR=/}
export DESTDIR

sudo mergemaster -iU -p -m $PWD -D $DESTDIR
$(dirname $0)/installkernel.sh || exit
make installworld
sudo mergemaster -iU -m $PWD -D $DESTDIR
