# TODO: interrogate vm.memguard.num_alloc and vm.memguard.minsize_reject
# TODO: test out multiple options with vm.memguard.options

original_desc=$(sysctl -n vm.memguard.desc)
original_minsize=$(sysctl -n vm.memguard.minsize)
original_options=$(sysctl -n vm.memguard.options)

test_driver="memguard_malloc_helper"
test_sysctl_prefix="test.$test_driver"
malloc_size=8192

# inuse memuse highuse requests
#
# XXX: does not handle multiple malloc(9) arenas with varying sizes.
get_stats()
{
	local malloc_size=$1

	vmstat -m | awk '
BEGIN { not_found = 1 }
$1 == "memguard_malloc_helper" && $NF == "'$malloc_size'" {
	print $2 $3 $4 $5
	not_found = 0
	exit
}
END { exit(not_found) }
'
}

skip_if_invariants_enabled()
{
	if [ "$(sysctl -n kern.features.invariant_support)" = "1" ]; then
		atf_skip "results in [non-immediate] INVARIANTS panic"
	fi
}

set_test_sysctl()
{
	atf_check -o not-empty sysctl ${test_sysctl_prefix}_$1=$2
}

set_memguard_sysctl()
{
	atf_check -o not-empty sysctl vm.memguard.$1="$2"
}

reset_memguard_sysctls()
{
	set_memguard_sysctl desc "$original_desc"
	set_memguard_sysctl minsize $original_minsize
	set_memguard_sysctl options $original_options
}

set_memguard_desc()
{
	set_memguard_sysctl desc $test_driver
}

set_memguard_options()
{
	set_memguard_sysctl options $1
}

load_test_driver()
{
	kldstat -m $test_driver || atf_check kldload $test_driver
}

unload_test_driver()
{
	kldunload $test_driver
}

atf_test_case test_MG_GUARD_AROUND_negative
test_MG_GUARD_AROUND_negative_head()
{
	:
}

test_MG_GUARD_AROUND_negative_body()
{
	skip_if_invariants_enabled

	set_memguard_desc
	set_memguard_options 1

	load_test_driver

	set_test_sysctl slab_size 1
	set_test_sysctl slab_offset -1
	set_test_sysctl allocate 1
}

test_MG_GUARD_AROUND_negative_cleanup()
{
	reset_memguard_sysctls
	unload_test_driver
}

atf_test_case test_MG_GUARD_AROUND_positive
test_MG_GUARD_AROUND_positive_head()
{
	:
}

test_MG_GUARD_AROUND_positive_body()
{
	skip_if_invariants_enabled

	set_memguard_desc
	set_memguard_options 1

	load_test_driver

	set_test_sysctl slab_size 1
	set_test_sysctl slab_offset 2
	set_test_sysctl allocate 1
	reset_memguard_desc
}

test_MG_GUARD_AROUND_positive_cleanup()
{
	reset_memguard_sysctls
	unload_test_driver
}

atf_test_case test_MG_GUARD_AROUND_and_MG_GUARD_ALLLARGE
test_MG_GUARD_AROUND_and_MG_GUARD_ALLLARGE_head()
{
	:
}

test_MG_GUARD_AROUND_and_MG_GUARD_ALLLARGE_body()
{
	skip_if_invariants_enabled

	set_memguard_desc
	set_memguard_options 3

	load_test_driver

	set_test_sysctl slab_size $malloc_size
	set_test_sysctl slab_offset $(( $malloc_size + 1 ))
	set_test_sysctl allocate 1
}

test_MG_GUARD_AROUND_and_MG_GUARD_ALLLARGE_cleanup()
{
	reset_memguard_sysctls
	unload_test_driver
}

#
# memguard_arena and memguard_physlimit are read-only tunables:
#
#306         /*
#307          * When we pass our memory limit, reject sub-page allocations.
#308          * Page-size and larger allocations will use the same amount
#309          * of physical memory whether we allocate or hand off to
#310          * uma_large_alloc(), so keep those.
#311          */
#312         if (vmem_size(memguard_arena, VMEM_ALLOC) >= memguard_physlimit &&
#313             req_size < PAGE_SIZE) {
#314                 addr = (vm_offset_t)NULL;
#315                 memguard_fail_pgs++;
#316                 goto out;
#317         }

atf_test_case test_fail_kva
test_fail_kva_head()
{
	:
}

test_fail_kva_body()
{
	atf_skip "TODO: write this testcase"

	set_memguard_desc
	set_memguard_options 3

	load_test_driver

	sysctl vm.memguard.fail_kva
}

atf_test_case test_fail_pgs
test_fail_pgs_head()
{
	:
}

test_fail_pgs_body()
{

	atf_skip "TODO: write this testcase"

	set_memguard_desc
	set_memguard_options 3

	load_test_driver

	sysctl vm.memguard.fail_pgs
}

atf_test_case test_minsize
test_minsize_head()
{
	:
}

test_minsize_body()
{
	skip_if_invariants_enabled

	set_memguard_desc
	set_memguard_options 3

	old_minsize_reject=$(sysctl -n vm.memguard.minsize_reject)

	load_test_driver

	set_memguard_sysctl minsize 2

	set_test_sysctl slab_size 1
	set_test_sysctl allocate 1

	minsize_reject=$(sysctl -n vm.memguard.minsize_reject)

	if [ $(( $old_minsize_reject + 1 )) -ne $minsize_reject ]; then
		atf_fail "$old_minsize_reject + 1 != $minsize_reject"
	fi
}

test_minsize_cleanup()
{
	reset_memguard_sysctls
	unload_test_driver
}

atf_init_test_cases()
{
	atf_add_test_case test_MG_GUARD_AROUND_negative
	atf_add_test_case test_MG_GUARD_AROUND_positive
	atf_add_test_case test_MG_GUARD_AROUND_and_MG_GUARD_ALLLARGE
	#atf_add_test_case test_fail_kva
	#atf_add_test_case test_fail_pgs
	atf_add_test_case test_minsize
}
