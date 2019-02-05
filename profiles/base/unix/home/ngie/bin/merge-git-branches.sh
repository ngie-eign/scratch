#!/bin/sh

set -e
# Avoid the glob ;).
original_branch=$(git branch -l | awk '$1 == "*" { print $NF }')
trap "git checkout $original_branch" EXIT
cd "$(git rev-parse --show-toplevel)"
: ${GIT_MASTER=master}
git checkout $GIT_MASTER
git pull --all
git merge upstream/$GIT_MASTER
branches=$(git branch -l | grep -v master | grep -v $GIT_MASTER | sort -du || :)
for branch in $branches
do
	case "$branch" in
	*/*)
		parent_branch=upstream/$branch
		;;
	*)
		parent_branch=$GIT_MASTER
		;;
	esac
	git checkout $branch && git merge --no-edit $branch &&
	git rebase $parent_branch || exit 1
done
if ${AUTO_PUSH:-true}
then
	git push --all -f
fi
git gc
