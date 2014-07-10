#!/bin/sh

cat >> /etc/fstab <<EOF
/dev/md99	/usr/tests	ufs	rw,noauto	0	0
EOF
