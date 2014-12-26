#include <sys/mman.h>
#include <err.h>
#include <inttypes.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>


static char *input_file;
static int unlink_input_file = -1;

static void
cleanup(void)
{


	if (unlink_input_file == 1)
		unlink(input_file);

}

int
main(int argc, char **argv)
{
	FILE *input_fp;
	char **endptr;
	long long pages;
	off_t offset;
	size_t len;
	long page_size;
	int flags, optch, prot;

	endptr = NULL;
	flags = 0;
	input_file = NULL;
	input_fp = NULL;
	offset = 0;
	pages = 1;
	prot = 0;
	page_size = sysconf(_SC_PAGE_SIZE);

	while ((optch = getopt(argc, argv, "f:i:l:o:p:s:uU")) != -1) {
		switch (optch) {
		case 'f':
			if (strcmp(optarg, "fixed") == 0)
				flags |= MAP_FIXED;
			else if (strcmp(optarg, "shared") == 0)
				flags |= MAP_SHARED;
			else if (strcmp(optarg, "private") == 0)
				flags |= MAP_PRIVATE;
			else
				errx(1, "unknown flag: %s", optarg);
			break;
		case 'i':
			if ((input_file = strdup(optarg)) == NULL)
				err(1, "strdup failed");
			break;
		case 'l':
			if ((len = (size_t)strtoimax(optarg, endptr, 10)) ==
			    (size_t)-1)
				err(1, "invalid number: %s", optarg);
			else if (endptr != '\0')
				errx(1, "invalid number: %s", optarg);
			else if (len % page_size != 0)
				errx(1, "length (%ju) isn't a multiple of %ld",
				    len, page_size);
			break;
		case 'o':
			if ((offset = (off_t)strtoimax(optarg, endptr, 10)) == -1)
				err(1, "invalid number: %s", optarg);
			else if (endptr != '\0')
				errx(1, "invalid number: %s", optarg);
			else if (offset % page_size != 0)
				errx(1, "offset (%ju) isn't a multiple of %ld",
				    offset, page_size);
			break;
		case 'p':
			if (strcmp(optarg, "read") == 0)
				prot |= PROT_READ;
			else if (strcmp(optarg, "write") == 0)
				prot |= PROT_WRITE;
			else if (strcmp(optarg, "exec") == 0)
				prot |= PROT_EXEC;
			else if (strcmp(optarg, "none") == 0)
				prot = PROT_NONE;
			else
				errx(1, "unknown protocol: %s", optarg);
			break;
		case 's':
			if ((pages = strtoll(optarg, endptr, 10)) == -1)
				err(1, "invalid number: %s", optarg);

			else if (endptr != '\0')
				errx(1, "invalid number: %s", optarg);

			break;
		case 'u':
			unlink_input_file = 1;
			break;
		case 'U':
			unlink_input_file = 0;
			break;
		default:
			errx(1, "unhandled option: %c", optch);
			break;
		}
	}

	if (input_file == NULL) {
		char buf[BUFSIZ];
		char template[] = "tmp.XXXXXXXX";
		size_t read_amount;
		int fd;

		if ((fd = mkstemp(template)) == -1)
			err(1, "failed to create a temporary file");

		if ((input_fp = fdopen(fd, "w+b")) == NULL)
			err(1, "fdopen(\"%s\", \"wb\") failed", template);

		while (!feof(stdin)) {
			if ((read_amount = fread(buf, 1, sizeof(buf), stdin))
			    != 0) {
				buf[BUFSIZ - 1] = '\0';
				if (fwrite(buf, 1, read_amount, input_fp) !=
				    read_amount)
					err(1, "fwrite failed");
			} else if (ferror(stdin)) {
				warn("An error occurred when reading from stdin\n");
				break;
			}
		}

		if ((input_file = strdup(template)) == NULL)
			err(1, "strdup failed");

		if (unlink_input_file == -1)
			unlink_input_file = 1;

		fflush(input_fp);
		fclose(input_fp);
	}

	len = pages * page_size;

	printf("pages = %lld; len = %zu; offset = %ju\n", pages, len, offset);

	if (atexit(cleanup) == -1)
		err(2, "failed to call atexit with cleanup(..)");



	exit(0);
}
