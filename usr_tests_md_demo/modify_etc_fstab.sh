#!/bin/sh

cat >> /etc/fstab <<EOF
/dev/md99	/usr/tests2	ufs	defaults,noauto	0	0
EOF
