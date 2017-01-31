.include <bsd.own.mk>

CLEANFILES+=	${OBJS:C/\.o$/.gcda/g} ${OBJS:C/\.o$/.gcno/g}
CLEANFILES+=	${SOBJS:C/\.o$/.gcda/g} ${SOBJS:C/\.o$/.gcno/g}

CFLAGS+=	--coverage
#.if ${COMPILER_TYPE} == "clang"
# XXX: base system compiler was bugged -- don't do this:
# https://reviews.freebsd.org/D9168
#LDADD+=		/usr/lib/libprofile_rt.a
#.elif ${COMPILER_TYPE} == "gcc"
# XXX: this should be implied by --coverage according to gcc(1) -- don't do
# this: https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=216021
#LDADD+=		-lgcov
#.endif
