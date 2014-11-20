#include <err.h>
#include <malloc_np.h>
#include <stdbool.h>
#include <stdlib.h>

int
main(void)
{
	size_t len;
	bool is_debug;

	len = sizeof(is_debug);

	if (mallctl("config.debug", &is_debug, &len, NULL, 0) == -1)
		err(2, "mallctl failed");

	exit(is_debug == true ? 0 : 1);
}
