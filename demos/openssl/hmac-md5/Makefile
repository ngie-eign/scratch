LDADD+=	-lcrypto

PROGS=	hmac-md5-test1 hmac-md5-test3

all: .PHONY ${PROGS}

check: .PHONY
.for prog in ${PROGS} hmac-md5-test.py
	./${prog} --short
	./${prog} --long
.endfor

hmac-md5-test1: hmac-md5-test.c
	${CC} -o ${.TARGET} ${LDADD} ${.ALLSRC}

hmac-md5-test3: hmac-md5-test.c
	${CC} -o ${.TARGET} ${LDADD} ${.ALLSRC}
