PROG=	errno

MAN=

DPSRCS+=	errno_list.h

errno_list.h:
	echo "#include <sys/cdefs.h>" > ${.TARGET}
	echo "#include <errno.h>" > ${.TARGET}
	echo "" >> ${.TARGET}
	echo "struct errno_set {" >> ${.TARGET}
	echo "	int errno_i;" >> ${.TARGET}
	echo "	const char* errno_s;" >> ${.TARGET}
	echo "} errno_list[] = {" >> ${.TARGET}
	echo "#include <errno.h>" | \
	    ${CC} -dM -E -xc - | \
	    awk '/#define E[A-Z0-9]+ [0-9]+/ { print "\t{ .errno_s = __STRING(" $$2 "), .errno_i = " $$3 " }," }' \
	    >> ${.TARGET}
	echo "};" >> ${.TARGET}

CLEANFILES+=	errno_list.h

.include <bsd.prog.mk>
