#include "mylibrary.h"

int
main(int argc, char **argv)
{

	if (1 < argc)
		return (my_api((const char*)argv[1]));
	return (1);
}
