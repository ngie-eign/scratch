#include <string.h>

#include "mylibrary.h"

/*
 * This API looks for MAGIC_KEY
 *
 * @returns 0 if MAGIC_KEY is found
 * @returns 1 if MAGIC_KEY was not found
 */
int
my_api(const char *key)
{

	if (strcmp(key, MAGIC_KEY) == 0)
		return (0);
	return (1);
}
