#!/bin/sh

set -ex
: ${JOBS=$(sysctl -n kern.smp.cpus)}
rm -f ~/bw.s
(make buildworld -j24 2>&1 && touch ~/bw.s) | tee ~/bw.log
[ -f ~/bw.s ]
rm -f ~/bk.s
(make buildkernel -j24 2>&1 && touch ~/bk.s) | tee ~/bk.log
[ -f ~/bk.s ]
