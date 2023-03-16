#!/bin/sh

bindir=$(dirname "$0")
versions="1.0.2 1.1.1 3.0 3.1"
for ver in $versions; do
	d="$ver"
	mkdir -p "$d"
	"$bindir/openssl_manpage_libcall_scrape.py" https://www.openssl.org/docs/man${ver}/man3/ | \
	    xargs -n 10 -P 5 "$bindir/../concurrent_fetch.py" --output-dir="$d" --verbose --retries=3
done
