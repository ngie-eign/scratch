#include <assert.h>
#include <stdio.h>

static char buf[128];

int
main(void)
{
	unsigned int i;

	for (i = 0; i < sizeof(buf) / sizeof(*buf); i++)
		assert(buf[i] == 0);
	printf("All values were 0\n");
	return (0);
}
