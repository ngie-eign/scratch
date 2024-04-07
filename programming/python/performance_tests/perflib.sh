#!/bin/sh

. "$BINDIR/msglib.sh" || exit

: ${PYTHON=python}

run_timeit()
{
	"$PYTHON" -m timeit "$@"
}
