/**
 * A simple demo program which illustrates that the default copy and move
 * constructors/operators perform shallow copies.
 */

#include <iostream>
#include <string>
#include <utility>
#include <vector>

using string_vector = std::vector<std::string>;

class VectorWrapper {
    public:
	VectorWrapper(const string_vector &v)
	    : _vec(v)
	{
	}
	VectorWrapper(const VectorWrapper &other) = default;
	VectorWrapper(VectorWrapper &&other) = default;

	VectorWrapper &operator=(VectorWrapper &other) = default;
	VectorWrapper &operator=(VectorWrapper &&other) = default;

	bool operator==(const VectorWrapper &other)
	{

		return (this->_vec == other._vec);
	}

	bool operator!=(const VectorWrapper &other)
	{

		return (this->_vec != other._vec);
	}

	size_t size() { return _vec.size(); }

    private:
	string_vector _vec;
};

int
main()
{
	VectorWrapper vw({ "a", "b", "cdef", "ghiJK" });

	VectorWrapper vw2 = vw;

	std::cout << "## Default copy behavior: copying vw to vw2" << std::endl;
	std::cout << "vw.size() => " << vw.size() << std::endl;
	std::cout << "vw2.size() => " << vw2.size() << std::endl;

	std::cout << "vw == vw2? " << (vw == vw2 ? "yes" : "no") << std::endl;

	std::cout << std::endl;

	VectorWrapper vw3 = std::move(vw2);

	std::cout << "## Default move behavior: moving vw2 to vw3" << std::endl;
	std::cout << "vw.size() => " << vw.size() << std::endl;
	std::cout << "vw2.size() => " << vw2.size() << std::endl;
	std::cout << "vw3.size() => " << vw3.size() << std::endl;

	std::cout << "vw == vw2? " << (vw == vw2 ? "yes" : "no") << std::endl;
	std::cout << "vw == vw3? " << (vw == vw3 ? "yes" : "no") << std::endl;
	std::cout << "vw2 == vw3? " << (vw2 == vw3 ? "yes" : "no") << std::endl;
}
