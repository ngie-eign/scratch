#!/bin/sh

: ${TMPDIR=/tmp}
SSH_AGENT_ENV=$TMPDIR/ssh-agent-env.$(whoami)
if [ -f $SSH_AGENT_ENV ]; then
	(
	. $SSH_AGENT_ENV >/dev/null
	pgrep ssh-agent | grep -q $SSH_AGENT_PID &&
	    kill -0 $SSH_AGENT_PID
	if [ $? -ne 0 ]; then # Not running; nuke stale environment script
		rm -f $SSH_AGENT_ENV
		exit 1
	fi
	exit 0
	)
fi
if [ ! -f $SSH_AGENT_ENV ]; then
	if ! ssh-agent > $SSH_AGENT_ENV; then
		rm -f $SSH_AGENT_ENV
		exit 1
	fi
fi
. $SSH_AGENT_ENV >/dev/null
for extra_ssh_key in $(find ~/.ssh/ -name \*.pub | sed -e 's/\.pub//'); do
	if [ -e $extra_ssh_key ]; then
		ssh-add $extra_ssh_key
	fi
done
