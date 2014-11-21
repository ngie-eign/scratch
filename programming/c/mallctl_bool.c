#include <err.h>
#include <libgen.h>
#include <malloc_np.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

int
main(int argc, char **argv)
{
	size_t len;
	bool bool_value;

	len = sizeof(bool_value);

	if (argc != 2) {
		fprintf(stderr, "usage: %s key\n", basename(argv[0]));
		fflush(stderr);
		exit(1);
	}

	if (mallctl(argv[1], &bool_value, &len, NULL, 0) == -1)
		err(2, "mallctl failed");

	printf("%s: %s\n", argv[1], bool_value ? "true" : "false");

	exit(0);
}
