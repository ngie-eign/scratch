.include <bsd.own.mk>

CLEANFILES+=	${OBJS:C/\.o$/.gcda/g} ${OBJS:C/\.o$/.gcno/g}
CLEANFILES+=	${SOBJS:C/\.o$/.gcda/g} ${SOBJS:C/\.o$/.gcno/g}

CFLAGS+=	--coverage
#.if ${COMPILER_TYPE} == "clang"
#CFLAGS+=	-fprofile-arcs -ftest-coverage
.if ${COMPILER_TYPE} == "gcc"
LDADD+=		-lgcov
.endif
