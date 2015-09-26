#include <sys/param.h>
#include <err.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "errno_list.h"

/*
 * Get the error number for an errno
 */

int
main(int argc, char *argv[])
{
	int errnum, i;

	if (argc != 2) {
		fprintf(stderr, "usage: errno <err-num>\n");
		exit(1);
	}

	for (i = 0; i < nitems(errno_list); i++) {
		if (strcmp(errno_list[i].errno_s, argv[1]) == 0) {
			printf("%d\n", errno_list[i].errno_i);
			exit(0);
		}
	}

	errx(1, "error number for %s not found", argv[1]);
}
