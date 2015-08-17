# Makefile for taking local customizations and packages and installing them by
# default on the base system with minimal effort.
#
# Invoke like:
#
# sudo make HOME=/home/ngie install

.MAIN: install

HOST!=	hostname | sed -E -e 's/\..*//g'

DIRS=	./
.if !empty(HOST) && exists(../${HOST}/)
DIRS+=	../${HOST}/
.endif

DOTFILES!=	find ${DIRS:tw:C/$/${HOME}\/dot.*/g} -maxdepth 0

${HOME}/.shrc: Makefile
	(cat /usr/share/skel/dot.shrc; echo; echo '[ -f $$HOME/.shrc-local ] && . $$HOME/.shrc-local') > $@

EXCLUDE=	Makefile|PACKAGES|/dot\.*|${HOME}|/scratch|/usr/src|-local\$$
install-dotfiles: \
    ${HOME}/.shrc
.for dir in ${DIRS}
	cd ${dir} && find . -type f | egrep -v "${EXCLUDE}" | \
	    cpio -dumpv /
.endfor
.for dotfile in ${DOTFILES}
.if exists(${dotfile}/)
	cp -pRf ${dotfile} ${HOME}/.
	rm -Rf ${HOME}/${dotfile:T:C/^dot//}
	mv ${HOME}/${dotfile:T} ${HOME}/${dotfile:T:C/^dot//}
.else
	cp -p ${dotfile} ${HOME}/${dotfile:T:C/^dot//}
.endif
.endfor

PACKAGES!=	grep -hv '\#' ${DIRS:tw:C/$/PACKAGES/g}

install-packages:
.if !defined(NO_PACKAGES) && !empty(PACKAGES)
	pkg install -y ${PACKAGES}
.endif

install: \
    install-dotfiles \
    install-packages
