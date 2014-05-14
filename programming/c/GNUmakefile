CFLAGS+=	-Wall

PROGRAMS:=	$(subst .c,,$(wildcard *.c))

.PHONY: all
all: $(PROGRAMS)

.PHONY: clean
clean:
	rm -f $(PROGRAMS) *.exe*

.PHONY: test
test::
	@for p in $(PROGRAMS); do \
		echo $$p START; \
		if uname -a | grep -iq cygwin; then \
			./$$p.exe; \
		else \
			./$$p; \
		fi; \
		echo $$p END; \
	done
