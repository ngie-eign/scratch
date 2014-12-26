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

static char operation[sizeof("failed_allocation") + 1];
static int do_operation;

static int
sysctl_test_bad_memory_operation(SYSCTL_HANDLER_ARGS)
{
	int error;
	unsigned int i;

	error = sysctl_handle_string(oidp, operation, sizeof(operation), req);
	if (error)
		operation[0] = '\0';

	if (error || req->newptr == NULL || req->newlen == 0)
		return (error);

	for (i = 0; i < nitems(callbacks); i++) {
		if (strcmp(callbacks[i].name, operation) == 0) {
			memcpy(operation, callbacks[i].name,
			    sizeof(operation));
			return (0);
		}
	}

	return (EINVAL);
}

static int
sysctl_test_bad_memory_do_operation(SYSCTL_HANDLER_ARGS)
{
	int error;
	unsigned int i;

	error = 0;

	if (req->oldptr != NULL || req->oldlen != 0)
		goto end;

	error = sysctl_handle_int(oidp, &do_operation, sizeof(do_operation),
	    req);
	if (error || req->newptr == NULL)
		goto end;

	for (i = 0; i < nitems(callbacks); i++) {
		if (strcmp(callbacks[i].name, operation) == 0) {
			printf("Running callback for %s\n", operation);
			callbacks[i].fn();
			goto end;
		}
	}
	error = EINVAL;

end:
	do_operation = 0;
	return (error);
}

SYSCTL_PROC(_test, OID_AUTO, bad_memory_operation, CTLTYPE_STRING|CTLFLAG_RW,
    NULL, 0, sysctl_test_bad_memory_operation, "A",
    "Perform an operation with the module to force a failure state in the "
    "kernel related to memory allocation/dereferencing");

SYSCTL_PROC(_test, OID_AUTO, bad_memory_do_operation, CTLTYPE_INT|CTLFLAG_RW,
    NULL, 0, sysctl_test_bad_memory_do_operation, "I",
    "Operations to perform on the kernel: 'double_free', 'out_of_bounds', and "
    "'uninitialized'");

static moduledata_t bad_memory_moddata = {
	"bad_memory",
	_modevent_noop,
	NULL,
};

MODULE_VERSION(bad_memory, 1);
DECLARE_MODULE(bad_memory, bad_memory_moddata, SI_SUB_EXEC, SI_ORDER_ANY);
MODULE_DEPEND(memguard_malloc_helper, test_sysctl, 1, 1, 1);
