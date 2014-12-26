#include <sys/param.h>
#include <sys/kernel.h>
#include <sys/module.h>
#include <sys/sysctl.h>

#include "test_sysctl.h"

/* XXX: move these next few lines somewhere else? */
SYSCTL_DECL(_test);
#ifdef SYSCTL_ROOT_NODE
SYSCTL_ROOT_NODE(OID_AUTO, test, CTLFLAG_RW, 0, "Testing");
#else
SYSCTL_NODE(, OID_AUTO, test, CTLFLAG_RW, 0, "Testing");
#endif

static moduledata_t test_sysctl_moddata = {
	"test_sysctl",
	_modevent_noop,
	NULL,
};

MODULE_VERSION(test_sysctl, 1);
DECLARE_MODULE(test_sysctl, test_sysctl_moddata, SI_SUB_EXEC, SI_ORDER_ANY);
