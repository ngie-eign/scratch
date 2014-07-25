#include <sys/types.h>
#include <sys/sysctl.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

unsigned long maxsockbuf;

static void
set_maxsockbuf_len(void)
{
	void* oldp;
	size_t oldlen;

	assert(sysctlbyname("kern.ipc.maxsockbuf",
	    NULL, &oldlen, NULL, 0) == 0);

	oldp = malloc(oldlen);
	assert(oldp);

 	assert(sysctlbyname("kern.ipc.maxsockbuf",
	    oldp, &oldlen, NULL, 0) == 0);

	memcpy(&maxsockbuf, oldp, oldlen);
}


int
main(void)
{
	set_maxsockbuf_len();

	printf("maxsockbuf=%d\n", maxsockbuf);

	return (0);
}
