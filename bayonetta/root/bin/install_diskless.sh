#!/bin/sh

set -eux

if [ "${DESTDIR:-/}" = "/" ]; then
	echo "DESTDIR must be set to a value other than /"
	exit 1
fi

if [ -d "$DESTDIR" ]; then
	rm -xRf $DESTDIR || :
	chflags -R 0 $DESTDIR || :
	rm -xRf $DESTDIR
fi

export PATH=$PATH:$(dirname $0)
env DEFAULT_KERNCONF=GENERIC install.sh

cat > ${DESTDIR}/boot/loader.conf <<'EOF'
console="comconsole vidconsole"
comconsole_speed="115200"
EOF

printf "%s\n" '-Dhn' > ${DESTDIR}/boot.config

: > "${DESTDIR}/etc/diskless"

echo "tmpfs	/tmp	tmpfs		rw,size=512m 0	0" > ${DESTDIR}/etc/fstab

cat > ${DESTDIR}/etc/rc.conf <<'EOF'
ntpd_enable="YES"
rpc_lockd_enable="YES"
rpc_statd_enable="YES"
sendmail_enable="NONE"
sshd_enable="YES"
EOF

echo -n abcd1234 | pw useradd -R ${DESTDIR} unprivileged -h 0 -m -G wheel
env DEFAULT_ALWAYS_YES=1 pkg -c ${DESTDIR} install -y ipmitool sudo

CONF=${DESTDIR}/conf
BASE=${CONF}/base
mkdir -p ${BASE}

(
cd ${DESTDIR}
for d in var etc; do
	find $d -print | cpio -dumpl ${BASE}/
done
)
sectors_in_mb=$(( $(( 1024 * 1024 )) / 512))
echo -n $(( 32 * $sectors_in_mb )) > ${BASE}/etc/md_size
echo -n $(( 1024 * $sectors_in_mb )) > ${BASE}/var/md_size
