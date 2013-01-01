#!/bin/sh

set -e
# Avoid the glob ;).
git checkout master
branches=$(git branch -l | grep -v master)
for branch in $branches
do
	case "$branch" in
	stable*)
		parent_branch=origin/$branch
		;;
	*)
		parent_branch=master
		;;
	esac
	git checkout $branch && git merge --no-edit $parent_branch || exit 1
done
if [ -n "$branches" ]
then
	git push --all
fi
