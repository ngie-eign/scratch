#!/bin/sh

set -e
# Avoid the glob ;).
original_branch=$(git branch -l | awk '$1 == "*" { print $NF }')
trap "git checkout $original_branch" EXIT
cd "$(git rev-parse --show-toplevel)"
git checkout master
git pull
git pu
branches=$(git branch -l | grep -v master | sort -du || :)
for branch in $branches
do
	case "$branch" in
	*/*)
		parent_branch=upstream/$branch
		;;
	*)
		parent_branch=master
		;;
	esac
	git checkout $branch && git pull &&
	git merge --no-edit $parent_branch || exit 1
done
if ${AUTO_PUSH:-true}
then
	git push --all
fi
git gc
