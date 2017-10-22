# New ports collection makefile for:	ct
# Date created:		Mon Jan  6 23:04:16 GMT 2003
# Whom:			TANAKA Takashi <tanaka@tahi.org>
#
# $FreeBSD: head/net/ct/Makefile 292101 2012-02-23 07:10:05Z linimon $
#

PORTNAME=	ct
PORTVERSION=	2.1.2
CATEGORIES=	net ipv6
MASTER_SITES=	http://www.tahi.org/release/ct/

MAINTAINER=	yaneurabeya@gmail.com
COMMENT=	IPv6 Conformance Test Kit

RUN_DEPENDS=	${LOCALBASE}/v6eval/bin/pktbuf:${PORTSDIR}/net/v6eval

USE_PERL5=      yes
NO_BUILD=	yes

MAKE_ENV+=	"NUTTYPE=host"

.include <bsd.port.mk>
