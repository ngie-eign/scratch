PROGS+=	disabled_demo
PROGS+=	expect_nonfatal_failure_demo
PROGS+=	fixture_fail_demo
PROGS+=	pass_fail_demo
PROGS+=	setup_environment_fail_demo
PROGS+=	skip_demo
PROGS+=	teardown_environment_fail_demo

CXXFLAGS+=	-Werror -W -Wall -Wunused
CXXFLAGS+=	-std=c++11
CXXFLAGS+=	-DGTEST_HAS_PTHREAD=1 -DGTEST_IS_THREADSAFE=1
CXXFLAGS+=	-DGTEST_LINKED_AS_SHARED_LIBRARY=1

ifdef GITDIR
CXXFLAGS+=	-I${GITDIR}/googlemock/include
CXXFLAGS+=	-I${GITDIR}/googletest/include
LDFLAGS+=	-L${GITDIR}/lib
else
CXXFLAGS+=	-I/usr/local/include
LDFLAGS+=	-L/usr/local/lib
endif

CPP_LIB?=

#LDLIBS+=	-lgtest -lgtest_main
LDLIBS+=	-lgtest -lgtest_main -lpthread ${CPP_LIB}

all: ${PROGS}

clean:
	rm -f *.core ${PROGS}
