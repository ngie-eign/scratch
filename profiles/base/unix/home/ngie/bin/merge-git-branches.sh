#!/bin/sh

DEBUG=false
debug()
{
	if ! $DEBUG; then
		# To appease `set -e`, return early in the negative path with
		# `0`.
		return 0
	fi
	echo "${0##*/}: DEBUG: $*"
}

error()
{
	echo "${0##*/}: ERROR: $*"
	exit 1
}

set -e
# Avoid the glob ;).
original_branch=$(git branch -l | awk '$1 == "*" { print $NF }')
trap "git checkout $original_branch" EXIT
cd "$(git rev-parse --show-toplevel)"
: ${DO_NOT_MIRROR_UPSTREAM_IN_CLONE=false}
: ${GIT_MASTER=master}
: ${GIT_UPSTREAM=upstream}
if $DO_NOT_MIRROR_UPSTREAM_IN_CLONE; then
	debug "Not mirroring $GIT_UPSTREAM/$GIT_MASTER in clone. Fetching all repos instead."
	git fetch --all
else
	git checkout $GIT_MASTER
	git pull --all
	git merge $GIT_UPSTREAM/$GIT_MASTER
fi
branches=$(git branch -l | awk '$1 != "*" { print $NF }' | sort -du || :)
# If the end-user asked for a particular expression to whitelist
if [ -n "$WHITELIST_FILTER" ]; then
	debug "Before whitelist: $branches"
	branches=$(echo "$branches" | egrep "$WHITELIST_FILTER" || :)
	debug "After whitelist: $branches"
fi
for branch in $branches; do
	# Skip over branches that need to be merged manually.
	# TODO: determine parent in a more intelligent manner.
	if [ -n "$BLACKLIST_FILTER" ] && echo "$branch" | egrep -q "$BLACKLIST_FILTER"; then
		debug "$branch matched blacklist"
		continue
	fi
	git checkout $branch
	# Pull in the latest committed changes so they don't get stomped on by
	# another force-pushed set of changes.
	if ! branch_remote=$(git config branch.$branch.remote); then
		error "Could not determine remote for $branch"
	fi
	git rebase $branch_remote/$branch
	git merge --no-edit $branch
	if parent_branch=$(git config branch.$branch.parent); then
		debug "Using manual override for $branch (child) to $parent_branch (parent)"
	else
		case "$branch" in
		*/*)
			parent_branch=$GIT_UPSTREAM/$branch
			;;
		*)
			parent_branch=$GIT_MASTER
			;;
		esac
		debug "Guessing $branch's parent is $parent_branch"
	fi
	git rebase $parent_branch
	if ${AUTO_PUSH:-true}; then
		git push -f $branch_remote $branch
	fi
done
if ${AUTO_GC:-true}; then
	git gc
fi
