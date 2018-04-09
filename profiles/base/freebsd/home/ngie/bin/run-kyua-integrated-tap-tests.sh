#!/bin/sh

[ -f Kyuafile ] || exit
grep tap_test_program Kyuafile | sed -e 's,.*name=",,' -e 's,".*,,g' |
    xargs -n 1 -I % prove -v ./%
