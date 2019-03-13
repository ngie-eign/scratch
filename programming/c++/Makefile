PROGS+=	map_demo
PROGS+=	regex_demo
PROGS+=	set_demo
PROGS+=	string_trim_demo

CXXFLAGS+=	-g -W -Wall -Wunused -Werror -std=c++11

CPP_LIB?=

ifneq (${CPP_LIB},)
LDLIBS+=	${CPP_LIB}
endif

all: ${PROGS}

clean:
	rm -f ${PROGS}
