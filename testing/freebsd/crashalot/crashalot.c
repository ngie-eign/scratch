#include <sys/cdefs.h>
#include <stdlib.h>
#include <string.h>

int
main(void)
{
	char *a_good_pointer_gone_bad = (char*)0x20;

	*a_good_pointer_gone_bad = '\0';

	return (0);
}
