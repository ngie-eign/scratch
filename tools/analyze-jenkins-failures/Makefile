JENKINS_JOB_NAME=	FreeBSD_HEAD-tests
JENKINS_JOB_URL=	https://jenkins.freebsd.org/job/${JENKINS_JOB_NAME}

# Why 869? See: https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=200546
BUILD_START?=	869
.ifndef BUILD_END
BUILD_END!=	curl -s ${JENKINS_JOB_URL}/lastCompletedBuild/testReport/ | \
		grep '<title>' | \
		sed -e 's,.*<title>${JENKINS_JOB_NAME} \#,,g' \
		    -e 's,Test Results.*</title>.*,,g'
.endif

BUILD_NUMBERS!=	seq ${BUILD_START} ${BUILD_END}

.for bnum in ${BUILD_NUMBERS}
${bnum}.xml:
	curl -s ${JENKINS_JOB_URL}/${bnum}/testReport/ > ${.TARGET}
XML+=	${bnum}.xml
.endfor

TEST_RESULTS_DB=	test_results.db
${TEST_RESULTS_DB}: ${XML}
	@rm -f ${.TARGET}
.for bnum in ${BUILD_NUMBERS}
	@python ./analyze_log.py \
	    --build ${bnum} \
	    --test-results-database ${.TARGET} \
	    --xml-file ${bnum}.xml
.endfor

all: ${TEST_RESULTS_DB}
	@python ./summarize_test_failures.py \
	    --test-results-database ${.ALLSRC}

clean:
	rm -f ${XML} ${TEST_RESULTS_DB}
