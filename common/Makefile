# Makefile for taking local customizations and ports and installing them by
# default on the base system with minimal effort.
#
# Invoke like:
#
# sudo make HOME=/home/gcooper install
#
# Garrett Cooper, April 2012

# SECTION: FreeBSD customized overlay

HOST!=	hostname | sed -E -e 's/\..*//g'

.if empty(HOST)
.error you must define HOST (could not be automatically divined)
.elif !exists(../${HOST}/)
.error directory for ${HOST} does not exist
.endif

DOTFILES!=	find ./${HOME}/dot.* ../${HOST}${HOME}/dot.* -maxdepth 0

${HOME}/.shrc: Makefile
	(cat /usr/share/skel/dot.shrc; echo; echo '[ -f .shrc-local ] && . .shrc-local') > $@

install-dotfiles: \
    ${HOME}/.shrc
.for dir in ../${HOST}/ .
.for ddir in / /usr/src
	args="--exclude *PORTS*"; \
	[ ${ddir} != "/usr/src" ] && args="$$args --exclude '*${HOME}*' --exclude '*/usr/src/*'"; \
	tmpfile=/tmp/sentinel.$$$$; \
	(tar $$args --exclude '*/dot.*' -cpf - -C ${dir} . && : > $$tmpfile) | \
	tar -xpvf - -C ${ddir}; \
	rm -f $$tmpfile
.endfor
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

# It's less annoying running config-recursive up front and the
# fetch-recursive call up front is a weaksauce attempt at working around the
# great firewall of EMC..
.if defined(NO_PORTS)
install-ports:
	@:
.else
install-ports:
.for port in ${PORTS}
	@name=`${MAKE} -C /usr/ports/${port} package-name`; \
	[ -d /var/db/pkg/$$name ] || \
		(cd /usr/ports/${port} && \
		 ${MAKE} config-recursive && \
		 while ! ${MAKE} fetch-recursive; do : ; done)
.endfor
.for port in ${PORTS}
	@name=`${MAKE} -C /usr/ports/${port} package-name`; \
	[ -d /var/db/pkg/$$name ] || \
		(echo "Building ${port}"; \
		 cd /usr/ports/${port} && \
		 ${MAKE} clean all deinstall install clean)
.endfor
.endif

install: \
    install-dotfiles \
    install-ports
