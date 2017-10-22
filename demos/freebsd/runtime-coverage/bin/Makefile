
PROG=		foo

CFLAGS+=	-I${.CURDIR:H}/lib

LDADD+=		-lfoo
LDFLAGS+=	-L${.OBJDIR:H}/lib
LDFLAGS+=	-Wl,-rpath-link,${.OBJDIR:H}/lib

MAN=

.include <bsd.prog.mk>
