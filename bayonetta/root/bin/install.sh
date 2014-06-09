#!/bin/sh

set -e
mergemaster -p $*
make installworld
make installkernel
mergemaster -iU $*
