#include <sys/param.h>
#include <sys/module.h>
#include <sys/systm.h>
#include <sys/kernel.h>
#include <sys/sysctl.h>

MALLOC_DECLARE(M_BAD_MEMORY);

MALLOC_DEFINE(M_BAD_MEMORY, "bad_memory", "Bad memory test malloc zone");

static int
load_bad_memory(struct module *m, int what, void *arg)
{

	return (0);
}

static void
double_free_cb(void)
{
	void *buf;

	buf = malloc(1, M_BAD_MEMORY, 0);
	KASSERT(buf != NULL, "malloc failed");

	free(buf, M_BAD_MEMORY);
	free(buf, M_BAD_MEMORY);
}

static void
out_of_bounds_cb(void)
{
	char *buf;

	buf = (char*)-1;

	*buf = 'a';
}

static void
uninitialized_cb(void)
{
	char *buf;

	buf = NULL;

	*buf = 'a';
}

static struct callback_t {
	const char	*name;
	void (*fn)(void);
} callbacks[] = {
	{ "double_free", double_free_cb, },
	{ "out_of_bounds", out_of_bounds_cb, },
	{ "uninitialized", uninitialized_cb, },
};

static int
sysctl_test_bad_memory_operation(SYSCTL_HANDLER_ARGS)
{
	char *operation;
	int error;
	unsigned int i;

	error = sysctl_handle_string(oidp, &operation, operation, req);
	if (error)
		return (error);

	for (i = 0; i < nitems(callbacks); i++)
		if (strcmp(callbacks[i].name, operation) == 0)
			callbacks[i].fn();

	return (EINVAL);
}

SYSCTL_DECLARE(_test); /* XXX: move this somewhere else */
SYSCTL_DECLARE(_test_bad_memory);

SYSCTL_PROC(_test_bad_memory, OID_AUTO, operation, CTLTYPE_STRING|CTLFLAG_RW,
    NULL, 0, sysctl_test_bad_memory_operation, "A",
    "Perform an operation with the module to force a failure state in the "
    "kernel; supported operations are: 'double_free', 'out_of_bounds', and "
    "'uninitialized'");

static moduledata_t bad_memory = {
	"bad_memory",
	load_bad_memory,
	NULL,
};
