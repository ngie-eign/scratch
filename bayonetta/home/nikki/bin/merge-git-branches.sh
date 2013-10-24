#!/bin/sh

set -e
# Avoid the glob ;).
original_branch=$(git branch -l | awk '$1 == "*" { print $NF }')
trap "git checkout $original_branch" EXIT
git checkout master
git pull
git pu
branches=$(git branch -l | grep -v master | sort -u || :)
for branch in $branches
do
	case "$branch" in
	stable/*)
		parent_branch=upstream/$branch
		;;
	stable-*)
		parent_branch=$(echo $branch | sed -e 's,stable-,stable ,g' -e 's,-.*,,g' -e 's,stable ,stable/,g')
		;;
	*)
		parent_branch=master
		;;
	esac
	git checkout $branch && git pull &&
	git merge --no-edit $parent_branch || exit 1
done
git checkout master
if ${AUTO_PUSH:-true}
then
	git push --all
fi
