PROGS+=	disabled_demo
PROGS+=	expect_nonfatal_failure_demo
PROGS+=	fixture_fail_demo
PROGS+=	parameterized_test_demo
PROGS+=	pass_fail_demo
PROGS+=	setup_environment_fatal_fail_demo
PROGS+=	setup_environment_nonfatal_fail_demo
PROGS+=	setup_environment_skip_demo
PROGS+=	skip_demo
PROGS+=	teardown_environment_fail_demo
PROGS+=	typed_test_suite_demo

CXXFLAGS+=	-Werror -W -Wall -Wunused
CXXFLAGS+=	-std=c++11
CXXFLAGS+=	-DGTEST_HAS_PTHREAD
CXXFLAGS+=	-DGTEST_LINKED_AS_SHARED_LIBRARY
CXXFLAGS+=	-DGTEST_HAS_TYPED_TEST
CXXFLAGS+=	-DGTEST_HAS_TYPED_TEST_P

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
