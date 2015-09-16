#include <sys/param.h>
#include <sys/kernel.h>
#include <sys/kthread.h>
#include <sys/lock.h>
#include <sys/lockmgr.h>
#include <sys/module.h>
#include <sys/mutex.h>
#include <sys/sema.h>
#include <sys/systm.h>
#include <sys/unistd.h>

static struct proc *locking_tests_proc;
static struct mtx locking_tests_sync_mtx;
/* sema(9) use inspired by sys/kern/vfs_aio.c */
static struct sema locking_tests_sync_sem;

static void
locking_tests_helper_proc(void *_lock)
{
	struct lock *lock = _lock;
	int rc;

	/**
	 * 1. Validate the following invariants:
	 *  - The parent owns the lock exclusively.
	 *  - Trying to upgrade an exclusive lock must fail with EBUSY.
	 *  - Trying to make an exclusive lock shared must fail with EDEADLK.
	 */
	rc = lockstatus(lock);
	KASSERT(rc == LK_EXCLOTHER,
	    ("not locked exclusively by parent: %d", rc));

	/*
	 * XXX: Ah, nuance...
	 *
	 * LK_UPGRADE	Upgrade a shared lock to an exclusive lock. If
	 *
	 * Trying to upgrade a lock you don't own at all (either shared or
	 * exclusive) -> panic.
	 */
#if 0
	rc = lockmgr(lock, LK_NOWAIT|LK_UPGRADE, &locking_tests_sync_mtx);
	KASSERT(rc == EBUSY, ("did not fail with EBUSY: %d", rc));
#endif
	rc = lockmgr(lock, LK_NOWAIT|LK_SHARED, &locking_tests_sync_mtx);
	KASSERT(rc == EDEADLK, ("did not fail with EDEADLK: %d", rc));

	/* 1.: DONE */

	sema_post(&locking_tests_sync_sem);

	/**
	 * 2. Validate the following invariants:
	 *  - The child will block on LK_SHARED when LK_NOWAIT is not
	 *    specified.
	 *  - LK_SHARED is returned when lockstatus on the lock is queried.
	 *  - The lock can be upgraded via LK_UPGRADE.
	 */
	rc = lockmgr(lock, LK_SHARED, &locking_tests_sync_mtx);
	KASSERT(rc == 0, ("LK_SHARED call in child failed: %d", rc));

	rc = lockstatus(lock);
	KASSERT(rc == LK_SHARED, ("not share-locked in child: %d", rc));

	rc = lockmgr(lock, LK_UPGRADE, &locking_tests_sync_mtx);
	KASSERT(rc == 0, ("LK_UPGRADE call in child failed: %d", rc));

	/* 2.: DONE */

	sema_post(&locking_tests_sync_sem);

	/**
	 * 3. child: downgrade/release the lock.
	 */
	rc = lockmgr(lock, LK_DOWNGRADE, &locking_tests_sync_mtx);
	KASSERT(rc == 0,
	    ("LK_DOWNGRADE call in child failed: %d", rc));
	rc = lockmgr(lock, LK_RELEASE, &locking_tests_sync_mtx);
	KASSERT(rc == 0,
	    ("LK_RELEASE call in child failed: %d", rc));

	/* 3.: DONE */

	/**
	 * 4. Make sure downgrading the wakes up the parent
	 */
	rc = lockmgr(lock, LK_SHARED, &locking_tests_sync_mtx);
	KASSERT(rc == 0, ("LK_SHARED call in child failed: %d", rc));

	sema_post(&locking_tests_sync_sem);

	rc = lockmgr(lock, LK_UPGRADE, &locking_tests_sync_mtx);
	KASSERT(rc == 0,
	    ("LK_UPGRADE call in child failed: %d", rc));

	sema_post(&locking_tests_sync_sem);

	rc = lockmgr(lock, LK_DOWNGRADE, &locking_tests_sync_mtx);
	KASSERT(rc == 0,
	    ("LK_DOWNGRADE call in child failed: %d", rc));

	/* All good! */
	rc = 0;

	kproc_exit(rc);
}

static int
run_locking_tests(void)
{
	struct lock locking_tests_lock;
	struct lock *lock = &locking_tests_lock;
	int rc;

	/*
	 * XXX: apparently this isn't valid in lockinit, even though the docs
	 * suggest otherwise.
	 *
	 * LK_TIMELOCK	   Use timo during a sleep; otherwise, 0 is used.
	 */
#if 0
	lockinit(lock, 0, "locking_tests_lock", 0,
	    LK_CANRECURSE|LK_NODUP|LK_TIMELOCK);
#else
	lockinit(lock, 0, "locking_tests_lock", 0, LK_CANRECURSE|LK_NODUP);
#endif

	rc = lockmgr(lock, LK_SHARED, &locking_tests_sync_mtx);
	KASSERT(rc == 0, ("LK_SHARED call in parent failed: %d", rc));

	/* Make sure the lock is shared to begin with */
	rc = lockstatus(lock);
	KASSERT(rc == LK_SHARED,
	    ("not share-locked in parent: %d", rc));

	/* Upgrade the lock to LK_EXCLUSIVE via LK_UPGRADE */
	rc = lockmgr(lock, LK_UPGRADE, &locking_tests_sync_mtx);
	KASSERT(rc == 0, ("LK_UPGRADE call in child failed: %d", rc));

	rc = lockstatus(lock);
	KASSERT(rc == LK_EXCLUSIVE,
	    ("not locked exclusively in parent: %d", rc));

	/* Create the helper proc */
	rc = kproc_create(locking_tests_helper_proc, lock, &locking_tests_proc,
	    RFMEM|RFNOWAIT, 0, "locking_tests.helper");
	if (rc != 0)
		goto done;

	/**
	 * 2. Downgrade the lock from exclusive to shared.
	 */
	sema_wait(&locking_tests_sync_sem);
	rc = lockmgr(lock, LK_DOWNGRADE, &locking_tests_sync_mtx);
	KASSERT(rc == 0,
	    ("LK_DOWNGRADE call in parent failed: %d", rc));
	rc = lockmgr(lock, LK_RELEASE, &locking_tests_sync_mtx);
	KASSERT(rc == 0,
	    ("LK_RELEASE call in parent failed: %d", rc));

	/**
	 * 3. Make sure the child was able to upgrade the shared lock to an
	 *    exclusive lock
	 */
	sema_wait(&locking_tests_sync_sem);
	rc = lockstatus(lock);
	KASSERT(rc == LK_EXCLOTHER,
	    ("not locked exclusively by child: %d", rc));

	/**
	 * 4. Make sure the lock was released by the child.
	 */
	sema_wait(&locking_tests_sync_sem);
	rc = lockstatus(lock);
	KASSERT(rc == 0, ("lock is already owned: %d", rc));

	sema_wait(&locking_tests_sync_sem);

	rc = lockmgr(lock, LK_SHARED, &locking_tests_sync_mtx);
	KASSERT(rc == 0, ("LK_SHARED call in parent failed: %d", rc));

	/**
	 * 5. Make sure we get woken back up when the lock is LK_DOWNGRADED.
	 */



	/* All good! */
	rc = 0;

done:
	lockdestroy(lock);

	return (rc);
}

static int
locking_tests_handler(module_t mod, int what, void *arg)
{
	int rc;

	rc = 0;
	if (what == MOD_LOAD) {
		mtx_init(&locking_tests_sync_mtx, "locking_tests_mtx", NULL,
		    MTX_DEF|MTX_RECURSE);
		sema_init(&locking_tests_sync_sem, 0, "locking_tests_sem");

		/* XXX: use sysctl to trigger the tests instead */
		rc = run_locking_tests();

		sema_destroy(&locking_tests_sync_sem);
		mtx_destroy(&locking_tests_sync_mtx);
	}

	return (rc);
}

static moduledata_t locking_tests_moddata = {
	"locking_tests",
	locking_tests_handler,
	NULL,
};

MODULE_VERSION(locking_tests, 1);
DECLARE_MODULE(locking_tests, locking_tests_moddata, SI_SUB_EXEC, SI_ORDER_ANY);
