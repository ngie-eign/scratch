#!/bin/sh

svn status /usr/src/etc/ | awk '{ print $2 }' | xargs -J % cp % etc/.
