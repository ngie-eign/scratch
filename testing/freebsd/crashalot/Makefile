PROG=	crashalot

MAN=

WARNS=	6

NO_WERROR=	I know this is bad code

crash-dummy-tests:
	@cd ${.CURDIR} && ${MAKE} -s obj
	@rm -f *.txt
.for O in -O0 -O1 -O2 -O
.for cc in clang33 clang34 clang35 clang gcc gcc49 gcc5
.for t in obj clean all
	@cd ${.CURDIR} && ${MAKE} -s ${t} CC=${cc} DEBUG_FLAGS="-g ${O}"
.endfor
	@objdump -x ${PROG} > objdump.${cc}.${O}.txt
.for db in gdb gdb66 gdb79
	@-cd ${.OBJDIR} && ${db} -batch -x ${.CURDIR}/gdb.script ./${PROG} > run.${cc}.${O}.${db}.txt 2>&1
.endfor
.endfor
.endfor
	@tar --exclude '*.tgz' --exclude '${PROG}*' \
	    -czpf ${.TARGET}-report.tgz .

.include <bsd.prog.mk>
