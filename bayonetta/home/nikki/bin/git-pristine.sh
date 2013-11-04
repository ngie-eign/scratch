#!/bin/sh

cd "$(git rev-parse --show-toplevel)"
git reset --hard
git status | awk 'NF == 2 { print $NF } /Untracked/ {p=1}'  | xargs rm -rf
