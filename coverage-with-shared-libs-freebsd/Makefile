SUBDIR+=	lib
SUBDIR+=	bin

check:

# Pair your compiler and gcov wisely.
GCOV?=		gcov

CLEANFILES+=	coverage.info

get-coverage:
	LD_LIBRARY_PATH=${.OBJDIR}/lib ${.OBJDIR}/bin/foo
	lcov --gcov-tool ${GCOV} --capture \
	    --directory ${.OBJDIR} --output-file \
	    ${.OBJDIR}/coverage.info
	genhtml ${.OBJDIR}/coverage.info --output-directory output

cleancoverage: .PHONY
	rm -Rf ${.OBJDIR}/output
cleandir: cleancoverage

.include <bsd.subdir.mk>
