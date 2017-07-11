SUBDIR+=	lib
SUBDIR+=	bin

check:

CLEANFILES+=	coverage.info

CLEANDIRS+=	output

# Pair your compiler and gcov wisely.
GCOV?=		gcov

get-coverage: .PHONY
	LD_LIBRARY_PATH=${.OBJDIR}/lib ${.OBJDIR}/bin/foo
	lcov --gcov-tool ${GCOV} --capture \
	    --directory ${.OBJDIR} --output-file \
	    ${.OBJDIR}/coverage.info
	genhtml ${.OBJDIR}/coverage.info --output-directory output

.include <bsd.subdir.mk>

cleandir: clean-coverage
clean-coverage: .PHONY
	rm -Rf ${CLEANDIRS}
	rm -f ${CLEANFILES}
