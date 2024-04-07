#!/bin/sh

. "$BINDIR/msglib.sh" || exit

: ${PYTHON=python}

system_summary()
{
	info "System summary"

	uname -movr
	uptime
	$PYTHON -V
}

run_timeit()
{
	"$PYTHON" -m timeit "$@"
}
