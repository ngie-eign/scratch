
atf_test_case test_mylibrary
test_mylibrary_head()
{
	:
}

test_mylibrary_body()
{
	atf_check -s exit:0 $(atf_get_srcdir)/mylibrary_helper 'hello world!'
}

atf_test_case test_mylibrary_a
test_mylibrary_a_head()
{
	:
}

test_mylibrary_a_body()
{
	atf_check -s exit:1 $(atf_get_srcdir)/mylibrary_helper 'hello world!!!'
}


atf_test_case test_mylibrary_2
test_mylibrary_2_head()
{
	:
}

test_mylibrary_2_body()
{
	atf_check -s exit:1 $(atf_get_srcdir)/mylibrary_helper " hello world!"
}

atf_test_case test_mylibrary_3
test_mylibrary_3_head()
{
	:
}

test_mylibrary_3_body()
{
	atf_check -s exit:1 $(atf_get_srcdir)/mylibrary_helper ""
}

atf_init_test_cases()
{

	atf_add_test_case test_mylibrary
	atf_add_test_case test_mylibrary_a
	atf_add_test_case test_mylibrary_2
	atf_add_test_case test_mylibrary_3
}
