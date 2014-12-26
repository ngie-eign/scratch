#include <stdio.h>
	
int
function_should_return_int(void)
{

	int i = 1;
}

int
main(void)
{
	int somevalue = function_should_return_int();

	printf("somevalue = %d\n", somevalue);

	return (0);
}
