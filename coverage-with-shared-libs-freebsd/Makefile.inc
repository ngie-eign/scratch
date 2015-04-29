.include <bsd.own.mk>

CLEANFILES+=	${OBJS:C/\.o$/.gcda/g} ${OBJS:C/\.o$/.gcno/g}
CLEANFILES+=	${SOBJS:C/\.o$/.gcda/g} ${SOBJS:C/\.o$/.gcno/g}

CFLAGS+=	--coverage
.if ${COMPILER_TYPE} == "clang"
# XXX: better automate this
_CLANG_PRIVATE_LIBS!=	clang -print-search-dirs | grep libraries: | sed -e 's,.*=,,' -e 's,:.*,,g'
LDADD+=		${_CLANG_PRIVATE_LIBS}/lib/freebsd/libclang_rt.profile-x86_64.a
.elif ${COMPILER_TYPE} == "gcc"
# XXX: this should be implied by --coverage according to gcc(1)
LDADD+=		-lgcov
.endif
