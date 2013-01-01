# Makefile for taking local customizations and ports and installing them by
# default on the base system with minimal effort.
#
# Invoke like:
#
# sudo make HOME=/home/gcooper install
#
# Garrett Cooper, April 2012

# SECTION: FreeBSD customized overlay

.MAIN: install

HOST!=	hostname | sed -E -e 's/\..*//g'

.if empty(HOST)
.error you must define HOST (could not be automatically divined)
.elif !exists(../${HOST}/)
.error directory for ${HOST} does not exist
.endif

DOTFILES!=	find ./${HOME}/dot.* ../${HOST}${HOME}/dot.* -maxdepth 0

${HOME}/.shrc: Makefile
	(cat /usr/share/skel/dot.shrc; echo; echo '[ -f $$HOME/.shrc-local ] && . $$HOME/.shrc-local') > $@

EXCLUDE=	Makefile|PORTS|/dot\.*|${HOME}|/usr/src|-local\$$
install-dotfiles: \
    ${HOME}/.shrc
.for dir in ../${HOST}/ .
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

# SECTION: Ports installation

PORTS!=		grep -hv '\#' ../${HOST}/PORTS PORTS

PORTSDIR?=	/usr/ports

install-ports:
.if !defined(NO_PORTS)
.for port in ${PORTS}
	cd ${PORTSDIR}/${port}; \
	if ${MAKE} check-already-installed >/dev/null; then \
		${MAKE} config-recursive \
		    -DDISABLE_VULNERABILITIES; \
		${MAKE} fetch-recursive \
		    -DDISABLE_VULNERABILITIES; \
	fi
.endfor
.for port in ${PORTS}
	cd ${PORTSDIR}/${port}; \
	if ${MAKE} check-already-installed >/dev/null; then \
		echo "Building ${port}"; \
		${MAKE} clean all deinstall install clean \
		    -DDISABLE_VULNERABILITIES; \
	fi
.endfor
.endif

install: \
    install-dotfiles \
    install-ports
