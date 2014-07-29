TOPDIR?=	${.CURDIR:H}
.export TOPDIR

CFLAGS+=	-I${TOPDIR}/tools/test_sysctl
