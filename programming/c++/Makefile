PROGS+=	default_copy_move_behavior_demo
PROGS+=	default_destructor_demo
PROGS+=	map_demo
PROGS+=	regex_demo
PROGS+=	set_demo
PROGS+=	string_trim_demo
PROGS+=	time_demo

CXXFLAGS+=	-g -O0 -W -Wall -Wunused -Werror -std=c++20

CPP_LIB?=

ifneq (${CPP_LIB},)
LDLIBS+=	${CPP_LIB}
endif

all: ${PROGS}

clean:
	rm -f ${PROGS}
