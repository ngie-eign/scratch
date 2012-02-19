#!/bin/sh

export PATH=/bin:/usr/bin:/usr/local/bin

cd /scratch/git/gitorious/freenas-clean
git pull gitorious master
git svn rebase
git push gitorious master
