#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void
segfault_handler(int signo)
{

	printf("Would have segfaulted\n");
	exit(1);
}

int
main(int argc, char **argv)
{
	char *null = NULL;

	signal(SIGSEGV, segfault_handler);

	if (argc > 1 && strcmp(argv[1], "strlen"))
		printf("len: %zu\n", strlen(null));
	else
		printf("cmp: %d\n", strcmp(null, ""));

	exit(0);
}
