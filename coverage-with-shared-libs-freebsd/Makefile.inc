.include <bsd.own.mk>

CLEANFILES+=	${OBJS:C/\.o$/.gcda/g} ${OBJS:C/\.o$/.gcno/g}
CLEANFILES+=	${SOBJS:C/\.o$/.gcda/g} ${SOBJS:C/\.o$/.gcno/g}

CFLAGS+=	--coverage
LDFLAGS+=	--coverage
