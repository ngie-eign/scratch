// regex demo program
//
// 1. Matcher is an unnecessary wrapper class, just for the purpose of also
//    demoing vector initialization, class definitions, etc, with C++.
// 2. The for-loops for regex_search and regex_match differ on purpose. The
//    goal is to show how range-loops and more traditional iteration loops
//    work.

#include <iostream>
#include <regex>
#include <string>

using namespace std;

namespace {

// For some odd reason it's called `subject` in C++. Wat?
const string subject = "The quick fox jumped over the lazy dog";
const string subject2 = subject + "\nBut really: why was the fox quick?";

class Matcher {
public:
	Matcher(const string _needle) : needle(_needle) {}
	// NB: purposely open.
	string needle;
};

void
do_re_test(const string &haystack, const string& needle, regex_constants::match_flag_type flags)
{
	// smatch - string iterator; cmatch is for `char *`.
	static unsigned test_num = 0;

	cout << "==== TEST (" << ++test_num << "/";
	if (flags & regex_constants::basic)
		cout << "basic";
	else if (flags & regex_constants::extended)
		cout << "extended";
	else if (flags & regex_constants::egrep)
		cout << "egrep";
	else
		cout << "ECMAScript";
	cout << ") ====" << endl;

        try {
		cmatch carr_matches;
		smatch str_matches;
		regex needle_re(needle.c_str(), flags);

		auto found = regex_search(haystack.c_str(), carr_matches,
		    needle_re);
		cout << (found ? "Found" : "Did not find") << " '" << needle
		     << "' in haystack: '" << haystack << "'." << endl;
		if (found) {
			for (unsigned i = 0; i < carr_matches.size(); i++) {
				cout << "  [" << i << "]: '" << carr_matches[i]
				     << "'" << endl;
			}
		}

		auto matched = regex_match(haystack, str_matches, needle_re);
		cout << "'" << needle << "' "
		     << (matched ? "matched" : "did not match")
		     << " haystack: '" << haystack << "'." << endl;
		if (matched) {
			unsigned i = 0;
			for (auto& match_str: str_matches) {
				cout << "  [" << i << "]: '" << match_str
				     << "'" << endl;
				i++;
			}
		}
        } catch (class regex_error& e) {
		cerr << "Could not compile regex for needle='" << needle <<
		        "': " << e.what() << endl;
		return;
	}
}

} // namespace

int
main(void)
{
	vector<Matcher> matcher_objs = {
		// Positive cases
		Matcher("fox"),
		Matcher(".+fox.+"),
		Matcher("The.+"),
		Matcher("^The .+"),
		Matcher("dog"),
		Matcher(R"RE(([^[:space:]]+) dog)RE"),
		Matcher(R"RE((^\S+) dog)RE"),
		Matcher(R"RE(jumped[[:space:]]+([^[:space:]]+))RE"),
		Matcher(R"RE(jumped[[:space:]]+\\([^[:space:]]+\\))RE"),
		Matcher(R"RE(([\s]+))RE"),
		Matcher(R"RE(([\w]+))RE"),
		Matcher(R"RE((\w+))RE"),
		Matcher(R"RE(([^\n]+))RE"),
		Matcher(R"RE(\\([^\n]+\\))RE"),
		// Negative cases
		Matcher("fox quickens"),
		Matcher(".+"),
		Matcher("Never matches")
	};
	vector<string> subjects = {
		subject,
		subject2
	};

	for (auto& matcher_obj : matcher_objs) {
		auto& needle = matcher_obj.needle;
		for (auto& haystack: subjects) {
			do_re_test(
			    haystack,
			    needle,
			    static_cast<regex_constants::match_flag_type>(regex_constants::ECMAScript)
			);
			do_re_test(
			    haystack,
			    needle,
			    static_cast<regex_constants::match_flag_type>(regex_constants::extended)
			);
			do_re_test(
			    haystack,
			    needle,
			    static_cast<regex_constants::match_flag_type>(regex_constants::basic)
			);
			do_re_test(
			    haystack,
			    needle,
			    static_cast<regex_constants::match_flag_type>(regex_constants::egrep)
			);
		}
	}

	return (0);
}
