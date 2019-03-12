// Based on chosen answer from the following Stack Overflow question:
// https://stackoverflow.com/questions/216823/whats-the-best-way-to-trim-stdstring

#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

namespace {

inline void
ltrim(std::string& s)
{
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](int c) {
        return !std::isspace(c);
    }));
}

inline void
rtrim(std::string& s)
{
    s.erase(std::find_if(s.rbegin(), s.rend(), [](int c) {
        return !std::isspace(c);
    }).base(), s.end());
}

std::string
trim(const std::string& str)
{
    std::string str_copy(str);

    ltrim(str_copy);
    rtrim(str_copy);

    return (str_copy);
}

} // namespace

int
main(void)
{
	std::vector<std::string> test_strings{
		"   \t\r\n",
		"   foobar",
		"foobar \n",
	};

	for (auto& test_string : test_strings) {
		std::string copy_test_string = trim(test_string);
		std::cout << "Before: '" << test_string << "'" << std::endl
			  << "After:  '" << copy_test_string << "'"
			  << std::endl << std::endl;
	}

	return (0);
}
