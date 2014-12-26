#!/bin/sh

set -ex
: ${JOBS=$(sysctl -n kern.smp.cpus)}
script ~/bw.log time make buildworld -j$JOBS
script ~/bk.log time make buildkernel -j$JOBS
