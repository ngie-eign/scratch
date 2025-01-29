// A simple C++ program illustrating how resources are leaked with default
// destructors when objects have memory managed via non-smart pointers, e.g.,
// via new/delete.
//
// Build like:
//	c++ -o def_dtor_leaks ./def_dtor_leaks -std=c++11 \
//	    -g -fsanitize=address -fno-omit-frame-pointer
//
// - Clang's LSAN finds the leak.
// - Clang's scan-build integration does not.
//
// Clang's LSAN requires Linux (doesn't work on FreeBSD 15.x or MacOS Sonoma).
//
// PS Yeah, there's a Ron DeSantis Easter Egg in here.
#include <string>

class D {
public:
	D(): bucket(new std::string("Am I leaky?")) { }
	~D() = default;
	// A more correct destructor is available below.
	//~D() { delete bucket; }
private:
	std::string* bucket;
};

int
main(void)
{
	D* tiny = new D;
	delete tiny;
	return 0;
}
