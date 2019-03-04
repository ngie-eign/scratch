PROGS+=	expect_nonfatal_failure_demo
PROGS+=	skip_demo

CXXFLAGS+=	-Wall -Wunused -std=c++11

LDFLAGS+=	-L/usr/local/lib

#LDLIBS+=	-lgtest -lgtest_main -lpthread
LDLIBS+=	-lgtest -lgtest_main

all: ${PROGS}

clean:
	rm -f *.core ${PROGS}
