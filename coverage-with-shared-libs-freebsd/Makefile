SUBDIR+=	lib
SUBDIR+=	bin

check:

CLEANFILES+=	coverage.info

get-coverage:
	LD_LIBRARY_PATH=${.OBJDIR}/lib ${.OBJDIR}/bin/foo
	lcov --capture --directory ${.OBJDIR} --output-file ${.OBJDIR}/coverage.info
	genhtml ${.OBJDIR}/coverage.info --output-directory output

cleancoverage: .PHONY
	rm -Rf ${.OBJDIR}/output
cleandir: cleancoverage

.include <bsd.subdir.mk>
