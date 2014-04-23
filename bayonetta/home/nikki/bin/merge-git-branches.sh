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
branches=$(git branch -l | grep -v $GIT_MASTER | sort -du || :)
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
		parent_branch=$GIT_MASTER
		;;
	esac
	git checkout $branch && git merge --no-edit $branch &&
	git merge --no-edit $parent_branch || exit 1
done
if ${AUTO_PUSH:-true}
then
	git push --all
fi
