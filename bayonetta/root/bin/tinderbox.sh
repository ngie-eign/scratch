#!/bin/sh

set -ex
: ${JOBS=$(sysctl -n kern.smp.cpus)}
make tinderbox JFLAG=$JOBS $*
