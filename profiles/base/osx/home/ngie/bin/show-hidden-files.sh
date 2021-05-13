#!/bin/sh
#
# Ref: https://osxdaily.com/2009/02/25/show-hidden-files-in-os-x/

defaults write com.apple.finder AppleShowAllFiles FALSE;killall Finder
