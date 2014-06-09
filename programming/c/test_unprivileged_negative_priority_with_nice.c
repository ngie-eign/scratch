#include <sys/resource.h>
#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include <unistd.h>

int
main(void)
{

	if (geteuid() == 0) {
		printf("is root\n");
		return (1);
	}

	assert(nice(-1) == -1);
	assert(errno == EPERM);

	return (0);
}
