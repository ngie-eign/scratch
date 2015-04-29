# Makefile for taking local customizations and packages and installing them by
# default on the base system with minimal effort.
#
# Invoke like:
#
# sudo make HOME=/home/ngie install

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

EXCLUDE=	Makefile|PACKAGES|/dot\.*|${HOME}|/scratch|/usr/src|-local\$$
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

# SECTION: Packages installation

PACKAGES!=	grep -hv '\#' ../${HOST}/PACKAGES PACKAGES

install-packages:
.if !defined(NO_PACKAGES) && !empty(PACKAGES)
	pkg install -y ${PACKAGES}
.endif

install: \
    install-dotfiles \
    install-packages
