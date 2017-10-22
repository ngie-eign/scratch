#!/bin/sh

set -e

: ${TESTSBASE=/usr/tests}

echo "Estimating the size of ${TESTSBASE}.."

echo $(( $(du -sm $TESTSBASE | awk '{ print $1 }') * 105 / 100 )) > usr-tests.size.txt

trap "rm -f usr-tests.txz" EXIT

echo "Creating tarball.."
tar cpJf usr-tests.txz -C /usr/tests .

trap - EXIT

cat <<EOF
Done!
EOF
