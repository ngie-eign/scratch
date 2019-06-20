#!/bin/sh

set -e
# Avoid the glob ;).
original_branch=$(git branch -l | awk '$1 == "*" { print $NF }')
trap "git checkout $original_branch" EXIT
cd "$(git rev-parse --show-toplevel)"
: ${GIT_MASTER=master}
: ${GIT_UPSTREAM=upstream}
git checkout $GIT_MASTER
git pull --all
git merge $GIT_UPSTREAM/$GIT_MASTER
branches=$(git branch -l | awk '$1 != "*" { print $NF }' | sort -du || :)
for branch in $branches
do
	case "$branch" in
	*/*)
		parent_branch=$GIT_UPSTREAM/$branch
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
if ${AUTO_GC:-true}
then
	git gc
fi
