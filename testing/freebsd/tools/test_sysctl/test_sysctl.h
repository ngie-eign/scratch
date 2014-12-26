#ifndef	__TEST_SYSCTL_H__
#define	__TEST_SYSCTL_H__

#include <sys/cdefs.h>

SYSCTL_DECL(_test);

/* See also: FreeBSD PR # 192257 */
static inline int
_modevent_noop(struct module *m __unused, int what __unused, void *arg __unused)
{

	return (0);
}

#endif
