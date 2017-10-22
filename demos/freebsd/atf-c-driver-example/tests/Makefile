BINDIR=		${TESTSDIR}

PROGS+=		mylibrary_helper

SRCS.mylibrary_helper=		mylibrary_helper.c

# NOTE: this shouldn't be done normally; you should run `make buildincludes`,
# then `make installincludes`, and finally set CFLAGS/LDFLAGS appropriately.
CFLAGS+=	-I${.CURDIR:H}/library

LDFLAGS+=	-L${.OBJDIR:H}/library

LDADD+=		-lmylibrary

ATF_TESTS_SH=	t_mylibrary

.include <bsd.test.mk>
