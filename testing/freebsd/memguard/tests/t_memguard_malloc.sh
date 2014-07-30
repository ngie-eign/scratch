# TODO: interrogate vm.memguard.num_alloc and vm.memguard.minsize_reject
# TODO: test out multiple options with vm.memguard.options

malloc_size=16384

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

atf_test_case test_MG_GUARD_AROUND
test_MG_GUARD_AROUND_head()
{
	:
}

test_MG_GUARD_AROUND_body()
{
	atf_skip "TODO: write this testcase"

	atf_check -o  vmstat -m
}

atf_test_case test_MG_GUARD_ALLLARGE
test_MG_GUARD_ALLLARGE_head()
{
	:
}

test_MG_GUARD_ALLLARGE_body()
{

	atf_skip "TODO: write this testcase"

	atf_check -o match vmstat -m
}

atf_test_case test_MG_GUARD_NOFREE
test_MG_GUARD_NOFREE_head()
{
	:
}

test_MG_GUARD_NOFREE_body()
{
	atf_skip "TODO: write this testcase"

	vmstat -m
}

atf_test_case test_fail_kva
test_fail_kva_head()
{
	:
}

test_fail_kva_body()
{
	atf_skip "TODO: write this testcase"

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

	sysctl vm.memguard.fail_pgs
}

atf_test_case test_minsize
test_minsize_head()
{
	:
}

test_minsize_body()
{

	atf_skip "TODO: write this testcase"

	sysctl vm.memguard.minsize
}

atf_init_test_cases()
{
	atf_add_test_case test_MG_GUARD_AROUND
	atf_add_test_case test_MG_GUARD_ALLLARGE
	atf_add_test_case test_MG_GUARD_NOFREE
	atf_add_test_case test_fail_kva
	atf_add_test_case test_fail_pgs
	atf_add_test_case test_minsize
}
