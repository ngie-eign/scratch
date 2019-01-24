/*
 * Standard zombie process example program.
 */

#include <err.h>
#include <stdio.h>
#include <unistd.h>

int
main(void)
{
	pid_t child;

	switch (child = fork()) {
	case -1:
		err(1, "fork");
	case 0:
		_exit(1);
	default:
		printf("The child's PID is %d\n", child);
		for (;;)
			sleep(1);
	}
	return (0);
}
