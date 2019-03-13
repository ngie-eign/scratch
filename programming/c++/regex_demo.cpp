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

// For some odd reason it's called `subject` in C++. Wat?
const string subject = "The quick fox jumped over the lazy dog";

class Matcher {
public:
	Matcher(const string _needle) : needle(_needle) {}
	// NB: purposely open.
	string needle;
};

int
main(void)
{
	vector<Matcher> matcher_objs = {
		// Positive cases
		Matcher("fox"),
		Matcher("The.+"),
		Matcher("^The .+"),
		Matcher("dog"),
		Matcher("jumped[[:space:]]+([^[:space:]]+)"),
		// Negative cases
		Matcher("fox quick"),
		Matcher("([^\n]+)"),
		Matcher("Never matches")
	};
	// smatch - string iterator; cmatch is for `char *`.
	cmatch carr_matches;
	smatch str_matches;

	for (auto& matcher_obj : matcher_objs) {
		auto& needle = matcher_obj.needle;
		regex needle_re(needle);

		auto found = regex_search(subject.c_str(), carr_matches, needle_re);
		cout << (found ? "Found" : "Did not find") << " '" << needle
		     << "' in subject: '" << subject << "'." << endl;
		if (found) {
			for (unsigned i = 0; i < carr_matches.size(); i++) {
				cout << "  [" << i << "]: '" << carr_matches[i]
				     << "'" << endl;
			}
		}

		auto matched = regex_match(subject, str_matches, needle_re);
		cout << "'" << needle << "' "
		     << (matched ? "matched" : "did not match") << " subject: '"
		     << subject << "'." << endl;
		if (matched) {
			int i = 0;
			for (auto& match_str: str_matches) {
				cout << "  [" << i << "]: '" << match_str
				     << "'" << endl;
				i++;
			}
		}
	}

	return (0);
}
