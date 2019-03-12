PROGS+=	disabled_demo
PROGS+=	expect_nonfatal_failure_demo
PROGS+=	fixture_fail_demo
PROGS+=	pass_fail_demo
PROGS+=	setup_environment_fail_demo
PROGS+=	skip_demo
PROGS+=	teardown_environment_fail_demo

CXXFLAGS+=	-Wall -Wunused -std=c++11

ifdef GITDIR
CXXFLAGS+=	-I${GITDIR}/googlemock/include
CXXFLAGS+=	-I${GITDIR}/googletest/include
LDFLAGS+=	-L${GITDIR}/lib
else
CXXFLAGS+=	-I/usr/local/include
LDFLAGS+=	-L/usr/local/lib
endif

#LDLIBS+=	-lgtest -lgtest_main
LDLIBS+=	-lgtest -lgtest_main -lpthread

all: ${PROGS}

clean:
	rm -f *.core ${PROGS}
