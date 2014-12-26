.include <src.opts.mk>

SUBDIR+=	malloc_driver
SUBDIR+=	uma_driver

.if ${MK_TESTS} != "no"
SUBDIR+=	tests
.endif

.include <bsd.subdir.mk>
