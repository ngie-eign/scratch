# New ports collection makefile for:	bmake
# Date created:				13 September 2009
# Whom:					Mikolaj Golub <to.my.trociny@gmail.com>
#
# $FreeBSD$
#

PORTNAME=	stelnet
PORTVERSION=	20100111
CATEGORIES=	net
MASTER_SITES=	http://www.crufty.net/ftp/pub/sjg/
DISTFILES=	stelnet-${PORTVERSION}.tar.gz

MAINTAINER=	gcooper@FreeBSD.org
COMMENT=	A secure telnet/telnetd

LICENSE=	BSD

WRKSRC=		${WRKDIR}/${PORTNAME}

BUILD_DEPENDS+=	bmake:${PORTSDIR}/devel/bmake
#LIB_DEPENDS+=	${PREFIX}/include/fwtk:${PORTSDIR}/security/fwtk
#RUN_DEPENDS+=	${PREFIX}/include/fwtk:${PORTSDIR}/security/fwtk

#MAN1=		bmake.1

#post-patch:	.SILENT
#	${REINPLACE_CMD} 's/^\.Nx/NetBSD/' ${WRKDIR}/bmake/bmake.1

#CFLAGS+=	-I${PREFIX}/fwtk
CFLAGS+=	-DUSE_TERMIO

.include <bsd.port.pre.mk>

# XXX: find the real utmpx rev.
.if ${OSVERSION} > 900043
CFLAGS+=	-DHAVE_UTMPX_H
.endif

MAKE_ENV+=	CFLAGS="${CFLAGS}" \
		PREFIX="${PREFIX}" \
		SRCTOP="${WRKSRC}/.."

post-patch:
	${REINPLACE_CMD} '/USE_FWTK/s/^/#/' ${WRKSRC}/Makefile.inc

do-build:
	cd ${WRKSRC} && ${MAKE_ENV} bmake all -DNO_FWTK

#do-install:
#	${INSTALL_PROGRAM} ${WRKDIR}/obj/bmake ${PREFIX}/bin
#	${INSTALL_MAN} ${WRKDIR}/bmake/bmake.1 ${MAN1PREFIX}/man/man1
#	${SH} ${WRKDIR}/mk/install-mk ${PREFIX}/share/mk
#	cd ${PREFIX} ;						\
#	    ${FIND} share/mk -type f -o -type l			\
#	    	| ${SORT}					\
#	    	>${WRKDIR}/PLIST.share-mk
#	cd ${PREFIX} ;						\
#	    ${FIND} share/mk/${_DATADIR} -type d		\
#	    	| ${SORT} -r | ${SED} -e 's/^/@dirrm /g'	\
#		>>${WRKDIR}/PLIST.share-mk
#	${ECHO_CMD} "r ${TMPPLIST}"			> ${WRKDIR}/ex.script
#	${ECHO_CMD} "/Insert PLIST.share-mk"		>> ${WRKDIR}/ex.script
#	${ECHO_CMD} "d"					>> ${WRKDIR}/ex.script
#	${ECHO_CMD} "r ${WRKDIR}/PLIST.share-mk"	>> ${WRKDIR}/ex.script
#	${ECHO_CMD} "x!"				>> ${WRKDIR}/ex.script
#	${CP} -p ${TMPPLIST} ${TMPPLIST}.pre-share-mk
#	cd ${WRKDIR} ; ex < ex.script

.include <bsd.port.post.mk>
