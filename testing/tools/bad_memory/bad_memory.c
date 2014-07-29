#include <sys/param.h>
#include <sys/kernel.h>
#include <sys/systm.h>
#include <sys/malloc.h>
#include <sys/module.h>
#include <sys/sysctl.h>

#include "test_sysctl.h"

MALLOC_DECLARE(M_BAD_MEMORY);
MALLOC_DEFINE(M_BAD_MEMORY, "bad_memory", "Bad memory test malloc zone");

static void
double_free_cb(void)
{
	void *buf;

	buf = malloc(1, M_BAD_MEMORY, M_WAITOK);
	KASSERT(buf != NULL, "malloc failed");

	free(buf, M_BAD_MEMORY);
	free(buf, M_BAD_MEMORY);
}

static void
failed_allocation_cb(void)
{

	malloc((unsigned long)-1, M_BAD_MEMORY, M_NOWAIT);
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
	{ "failed_allocation", failed_allocation_cb, },
	{ "out_of_bounds", out_of_bounds_cb, },
	{ "uninitialized", uninitialized_cb, },
};

static int
sysctl_test_bad_memory_operation(SYSCTL_HANDLER_ARGS)
{
	char operation[20];
	int error;
	unsigned int i;

	/* Only handle the request once */
	if (req->oldptr != NULL)
		return (0);

	error = sysctl_handle_string(oidp, operation, sizeof(operation), req);
	if (error)
		return (error);

	for (i = 0; i < nitems(callbacks); i++) {
		if (strcmp(callbacks[i].name, operation) == 0) {
			printf("Running callback for %s\n", operation);
			callbacks[i].fn();
		}
	}

	return (EINVAL);
}

/*
 * XXX: needs some work because of unresolved symbols
 *
 * Should look at some of the drivers that employ hw.* to
 * build their sysctl trees automagically
 */
#if 0
SYSCTL_DECL(_test_bad_memory);
static SYSCTL_NODE(_test_bad_memory, OID_AUTO, bad_memory, CTLFLAG_RD, 0,
    "bad_memory testing sysctl node");

SYSCTL_PROC(_test_bad_memory, OID_AUTO, operation, CTLTYPE_STRING|CTLFLAG_RW,
    0, 0, sysctl_test_bad_memory_operation, "A",
    "Perform an operation with the module to force a failure state in the "
    "kernel related to memory allocation/dereferencing; supported operations "
    "are: 'double_free', 'out_of_bounds', and 'uninitialized'");
#else
SYSCTL_PROC(_test, OID_AUTO, bad_memory_operation, CTLTYPE_STRING|CTLFLAG_RW,
    NULL, 0, sysctl_test_bad_memory_operation, "A",
    "Perform an operation with the module to force a failure state in the "
    "kernel related to memory allocation/dereferencing; supported operations "
    "are: 'double_free', 'out_of_bounds', and 'uninitialized'");
#endif

static moduledata_t bad_memory_moddata = {
	"bad_memory",
	NULL,
	NULL,
};

MODULE_VERSION(bad_memory, 1);
DECLARE_MODULE(bad_memory, bad_memory_moddata, SI_SUB_EXEC, SI_ORDER_ANY);
MODULE_DEPEND(memguard_malloc_helper, test_sysctl, 1, 1, 1);
