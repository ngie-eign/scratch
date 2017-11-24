#!/bin/sh

set -e
git fetch upstream
git checkout master && git merge upstream/master
git checkout isilon-atf && git merge master
git checkout cleanup-libcam && git merge master
git checkout ntb-playground && git merge master
git checkout libcam-tests && git merge isilon-atf
git checkout isilon-atf
