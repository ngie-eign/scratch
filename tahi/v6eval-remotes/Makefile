# New ports collection makefile for:	v6eval-remotes
# Date created:		Sat Oct  6 14:49:45 PDT 2012
# Whom:			Garrett Cooper <yanegomi@gmail.com>
#
# $FreeBSD$
#

PORTNAME=	v6eval-remotes
PORTVERSION=	3.0
CATEGORIES=	net ipv6
MASTER_SITES=	http://www.tahi.org/release/v6eval/

MAINTAINER=	yanegomi@gmail.com
COMMENT=	IPv6 Conformance Test Platform

RUN_DEPENDS=	${SITE_PERL}/Expect.pm:${PORTSDIR}/lang/p5-Expect \
		${LOCALBASE}/v6eval/bin/pktbuf:${PORTSDIR}/net/v6eval

USE_PERL5=	yes
NO_MANCOMPRESS=	yes
#MAN1PREFIX=	${PREFIX}/v6eval
#MAN3PREFIX=	${PREFIX}/lib/perl5/${PERL_VERSION}
#MAN1=		pktctl.1.gz pktsend.1.gz
#MAN3=		V6evalRemote.3 V6evalTool.3
MAKE_JOBS_UNSAFE=	yes
SUB_FILES=	pkg-message

.include <bsd.port.pre.mk>

post-install:
	@${CAT} ${PKGMESSAGE}

.include <bsd.port.post.mk>
