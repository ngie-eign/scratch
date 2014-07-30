#include <sys/param.h>
#include <sys/kernel.h>
#include <sys/systm.h>
#include <sys/module.h>
#include <sys/queue.h>
#include <sys/sysctl.h>
#include <vm/uma.h>

#include "test_sysctl.h"

static uma_zone_t zone;
static long item_offset;
static unsigned long item_size = 256;
static int allocate;
static int destroy_zone_after_use = 1;
static uint32_t align;
static unsigned int allocation_attempts = 1;

static void
destroy_zone(void)
{

	if (zone == NULL)
		return;

	printf("%s called\n", __func__);

	uma_zdestroy(zone);
	zone = NULL;
}

static int
evhand(struct module *m __unused, int what, void *arg __unused)
{

	if (what == MOD_UNLOAD)
		destroy_zone();

	return (0);
}

static int
sysctl_memguard_uma_helper_allocate(SYSCTL_HANDLER_ARGS)
{
	struct entry {
		char *buf;
		SLIST_ENTRY(entry) entries;
	} *np, *np_temp;

	char *buf;
	int error, val;
	unsigned int i;

	error = 0;

	if (req->oldptr != NULL || req->oldlen != 0)
		goto end;

	error = sysctl_handle_int(oidp, &val, 0, req);
	if (error || req->newptr == NULL)
		goto end;

	if (zone == NULL) {
		zone = uma_zcreate("memguard_uma_helper", item_size,
		    NULL, NULL, NULL, NULL, align, UMA_ZONE_VM);
		if (zone == NULL) {
			error = ENOMEM;
			goto end;
		}
	}

	SLIST_HEAD(, entry) head = SLIST_HEAD_INITIALIZER(head);
	SLIST_INIT(&head);

	for (i = 1; i <= allocation_attempts; i++) {
		printf("%s: allocation attempt %u/%u\n", __func__, i,
		    allocation_attempts);
		buf = uma_zalloc(zone, M_NOWAIT);
		if (buf == NULL) {
			printf("%s: uma_zalloc failed\n", __func__);
			break;
		}

		np = malloc(sizeof(struct entry), M_TEMP, M_NOWAIT);
		if (np == NULL) {
			uma_zfree(zone, buf);
			printf("%s: malloc for SLIST entry failed\n",
			    __func__);
			break;
		}

		buf[item_offset] = 'a';
		np->buf = buf;

		SLIST_INSERT_HEAD(&head, np, entries);
	}

	if (0 < allocation_attempts) {

		i = 1;

		SLIST_FOREACH_SAFE(np, &head, entries, np_temp) {
			printf("%s: deallocating item %u/%u\n", __func__, i,
			    allocation_attempts);

			SLIST_REMOVE(&head, np, entry, entries);

			uma_zfree(zone, np->buf);
			free(np, M_TEMP);
			i++;
		}

	}

	if (destroy_zone_after_use)
		destroy_zone();

end:
	allocate = 0;

	return (0);
}

SYSCTL_ULONG(_test, OID_AUTO, memguard_uma_helper_item_size,
    CTLTYPE_ULONG|CTLFLAG_RW, &item_size, 0,
    "Size to reserve for a zone keg uma_zalloc(9)");

SYSCTL_UINT(_test, OID_AUTO, memguard_uma_helper_allocation_attempts,
    CTLTYPE_UINT|CTLFLAG_RW, &allocation_attempts, 0,
    "Number of attempts for allocating and freeing memory");

SYSCTL_UINT(_test, OID_AUTO, memguard_uma_helper_align,
    CTLTYPE_UINT|CTLFLAG_RW, &align, 0,
    "Value to pass to uma_zcreate for `align`; see uma.h for more details");

SYSCTL_UINT(_test, OID_AUTO, memguard_uma_helper_destroy_zone_after_allocate,
    CTLTYPE_INT|CTLFLAG_RW, &destroy_zone_after_use, 0,
    "Automatically destroy zone after allocate operation completes");

SYSCTL_LONG(_test, OID_AUTO, memguard_uma_helper_item_offset,
    CTLTYPE_LONG|CTLFLAG_RW, &item_offset, 0,
    "Virtual offset to seek to in the item to test memory access protection "
    "support");

SYSCTL_PROC(_test, OID_AUTO, memguard_uma_helper_allocate,
    CTLTYPE_INT|CTLFLAG_RW, NULL, 0,
    sysctl_memguard_uma_helper_allocate, "I",
    "Allocate memory according to other related (size, number of attempts, "
    "overallocation)");

static moduledata_t memguard_uma_helper_moddata = {
	"memguard_uma_helper",
	evhand,
	NULL,
};

MODULE_VERSION(memguard_uma_helper, 1);
DECLARE_MODULE(memguard_uma_helper, memguard_uma_helper_moddata,
    SI_SUB_EXEC, SI_ORDER_ANY);
MODULE_DEPEND(memguard_malloc_helper, test_sysctl, 1, 1, 1);
