#!/bin/sh
#
# Build a bootable vanilla FreeBSD image for USB thumb drives with IPv6 enabled
# by default and with IB/OFED support built in.
#
# The output image name is the `branch-subdir.nanobsd.img`
#
# Additional arguments are passed through to nanobsd.sh directly.
#
# Tweakable variables:
#
# - FBSD_BRANCH - branch relative to http://svn.freebsd.org/base/ where you want
#                 to grab your sources from, e.g. releng/7.3; defaults to
#                 releng/7.3.
# - TMPDIR      - temporary directory where all the files will be put; defaults to
#                 a random directory under /tmp/
#
# Examples:
#
# 1. Build CURRENT (latest revision) using a random directory under /tmp:
#
# sudo env FBSD_BRANCH=head sh build-diskimage.sh
#
# 2. Build 8.3-RELEASE (latest patchset) using pre-pulled sources in /tmp/tmp.inaZw4
#    and do not blast away the objdir:
#
# sudo env FBSD_BRANCH=releng/8.3 TMPDIR=/tmp/tmp.inaZw4 sh build-diskimage.sh -b

err() {
	echo 2>&1 "${0##*/}: ERROR: $*"
	exit 1
}

SCRIPTDIR=$(dirname $(realpath $0))
NANOBSDDIR=$(realpath $SCRIPTDIR/../nanobsd/)

# XXX: someday, hopefully nanobsd will support non-root installs/gpart/makefs, but
# until then..
if [ $(id -u) -ne 0 ]
then
	err "you must be root when executing this script!"
fi
if [ ! -d $NANOBSDDIR ]
then
	err "couldn't find nanobsd; did you check out $NANOBSDDIR too?"
fi

set -e

: ${FBSD_BRANCH=releng/7.3}
: ${TMPDIR=$(mktemp -d /tmp/tmp.XXXXXX)}
_nanobsd_conf="$TMPDIR/nanobsd.conf"
NANO_SRC="$TMPDIR/src"

NANO_LABEL=$(echo "$FBSD_BRANCH" | sed -e 's,/,,g' -e 's,\.,,')

cat > $_nanobsd_conf <<EOF
#!/bin/sh

NANO_RAM_TMPVARSIZE=$(( 1024 * 1024 / 2 ))
FlashDevice generic 256m
MAKEOBJDIRPREFIX="$TMPDIR/obj"
NANO_BOOT2CFG="-Dh"
NANO_BOOTLOADER=boot/boot0
NANO_IMAGES=1
NANO_LABEL="$NANO_LABEL"
NANO_OBJ="$TMPDIR/nobj"
NANO_SRC="$NANO_SRC"
NANO_TOOLS="$NANOBSDDIR"

EOF

cat >> $_nanobsd_conf <<"EOF"
CONF_BUILD="
WITHOUT_ATM=
WITHOUT_AUDIT=
WITHOUT_BIND_DNSSEC=
WITHOUT_BIND_ETC=
WITHOUT_BIND_LIBS_LWRES=
WITHOUT_BIND_NAMED=
WITHOUT_BLUETOOTH=
WITHOUT_BSNMP=
WITHOUT_CALENDAR=
WITHOUT_CDDL=
WITHOUT_CLANG=
WITHOUT_CTM=
WITHOUT_CVS=
WITHOUT_DICT=
WITHOUT_EXAMPLES=
WITHOUT_FORTRAN=
WITHOUT_FREEBSD_UPDATE=
WITHOUT_GAMES=
WITHOUT_GCOV=
WITHOUT_GPIB=
WITHOUT_GSSAPI=
WITHOUT_HESOID=
WITHOUT_HTML=
WITHOUT_I4B=
WITHOUT_IPFILTER=
WITHOUT_IPFW=
WITHOUT_IPX=
WITHOUT_KERBEROS=
WITHOUT_LIBKSE=
WITHOUT_LOCALES=
WITHOUT_LPR=
WITHOUT_MAN=
WITHOUT_NCP=
WITHOUT_NDIS=
WITHOUT_NIS=
WITHOUT_NLS=
WITHOUT_NS_CACHING=
WITHOUT_OBJC=
WITH_OFED=
WITHOUT_PF=
WITHOUT_PORTSNAP=
WITHOUT_PPP=
WITHOUT_PROFILE=
WITHOUT_RCMDS=
WITHOUT_SENDMAIL=
WITHOUT_SSP=
WITHOUT_SYSINSTALL=
WITHOUT_WIRELESS=
WITHOUT_WPA_SUPPLICANT_EAPOL=
"

CONF_INSTALL="$CONF_BUILD
WITHOUT_TOOLCHAIN=
"

setup_nanobsd_etc2() {

    cd $NANO_WORLDDIR/etc
    cat > rc.conf <<"EOF2"
ifconfig_cxgb0="up"
ifconfig_cxgb1="up"
ifconfig_em1="up"
ifconfig_igb1="up"
case "$(uname -r)" in
9*|1[0-9]*)
    ifconfig_cxgb0_ipv6="inet6 -ifdisabled"
    ifconfig_cxgb1_ipv6="inet6 -ifdisabled"
    ifconfig_em1_ipv6="inet6 -ifdisabled"
    ifconfig_igb1_ipv6="inet6 -ifdisabled"
    ifconfig_ix0_ipv6="inet6 -ifdisabled"
    ;;
8*)
    ipv6_ifconfig_cxgb0="-ifdisabled"
    ipv6_ifconfig_cxgb1="-ifdisabled"
    ipv6_ifconfig_em1="-ifdisabled"
    ipv6_ifconfig_igb1="-ifdisabled"
    ipv6_ifconfig_ix0="-ifdisabled"
    ipv6_enable="YES"
    ;;
7*)
    ipv6_ifconfig_cxgb0="up"
    ipv6_ifconfig_cxgb1="up"
    ipv6_ifconfig_em1="up"
    ipv6_ifconfig_igb1="up"
    ipv6_ifconfig_ix0="up"
    ipv6_enable="YES"
    ;;
esac
ifconfig_em0="DHCP"
ifconfig_igb0="DHCP"

sshd_enable="YES"
ntpd_enable="YES"
EOF2

    cat >> sysctl.conf <<EOF2
kern.ipc.nmbjumbo9=262144
kern.ipc.nmbjumbo16=262144
kern.ipc.nmbclusters=262144
kern.ipc.nmbjumbop=262144
kern.ipc.maxsockbuf=2097152
net.inet.tcp.recvspace=65536
net.inet.tcp.recvbuf_max=2097152
net.inet.tcp.recvbuf_max=2097152
net.inet.tcp.recvbuf_inc=16384
net.inet.tcp.recvspace_max=2097152
net.inet.tcp.recvspace_inc=16384
net.inet.tcp.sendspace=32768
net.inet.tcp.sendbuf_max=2097152
net.inet.tcp.sendbuf_inc=8192
net.inet.tcp.sendspace_max=2097152
net.inet.tcp.sendspace_inc=16384
EOF2

    # Speed up baudrate
    sed -E -i '' -e '/^(sio|uart)/s/9600/115200/' remote

}
customize_cmd setup_nanobsd_etc2

# Copied from nanobsd.sh
cust_comconsole() {
    cd $NANO_WORLDDIR

    # Speed up baudrate
    sed -E -i '' -e 's/9600/115200/g' etc/ttys

    # Enable getty on COM1
    sed -E -i '' -e /tty[du]0/s/off/on/ etc/ttys

    # Disable getty on syscons devices apart from /dev/ttyv0
    sed -E -i '' -e '/^ttyv[1-8]/s/([[:space:]]*)on/\1off/' etc/ttys

    # Tell loader to use serial console early.
    echo "${NANO_BOOT2CFG}" > boot.config
}
customize_cmd cust_comconsole

# Copied from nanobsd.sh
cust_allow_ssh_root() {
    sed -i '' \
        -e '/PermitEmptyPasswords/s/.*/PermitEmptyPasswords yes/' \
	-e '/PermitRootLogin/s/.*/PermitRootLogin yes/' \
        ${NANO_WORLDDIR}/etc/ssh/sshd_config
}
customize_cmd cust_allow_ssh_root

setup_serial() {

    cd $NANO_WORLDDIR

    cat > boot/loader.conf <<"EOF2"
# Allow USB devices 30 seconds to quiesce (only on 8.x).
kern.cam.boot_delay="30000"
comconsole_speed="115200"
if_cxgb_enable="YES"
if_cxgbe_enable="YES"
if_em_enable="YES"
if_igb_enable="YES"
if_ix_enable="YES"
EOF2
}
customize_cmd setup_serial

last_orders() {
    cp $NANO_OBJ/_.disk.full ${FBSD_BRANCH##*/}.nanobsd.img
}
EOF

_svn_url=http://svn.freebsd.org/base/$FBSD_BRANCH
(
if [ -d $NANO_SRC/.svn ]
then
	cd $NANO_SRC
	svn cleanup .
	svn switch $_svn_url
	svn up
else
	mkdir -p $NANO_SRC
	cd $NANO_SRC
	svn co $_svn_url .
fi
)

for module in \
    cxgb cxgbe em ixgb ixgbe \
; do
	if [ -d $TMPDIR/src/sys/modules/$module ]
	then
		NANO_MODULES="$NANO_MODULES $module"
	fi
done
if [ -n "$NANO_MODULES" ]
then
	echo "NANO_MODULES='$NANO_MODULES'" >> $_nanobsd_conf
fi

case "$-" in
*x*)
	_nanobsd_flags=-x
	;;
esac

sh $_nanobsd_flags $NANOBSDDIR/nanobsd.sh -c $_nanobsd_conf $*
