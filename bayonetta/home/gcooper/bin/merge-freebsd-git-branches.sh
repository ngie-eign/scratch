#!/bin/sh

set -e
# Avoid the glob ;).
git checkout master
git pull
git pu
branches=$(git branch -l | grep -v master)
for branch in $branches
do
	case "$branch" in
	stable*)
		parent_branch=upstream/$branch
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
