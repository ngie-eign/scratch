#!/bin/sh

set -x

sh -c 'i=$(expr $i + 1); echo $i'
sh -c ': $(( i += 1 )); echo $i'
sh -c 'i=$(( $i + 1 )); echo $i'
