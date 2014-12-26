#include <stdio.h>

void
foo(void)
{
	static int i = 0;

	printf("%d\n", i++);
}

int
main(void)
{

	foo();
	foo();

	return (0);
}
