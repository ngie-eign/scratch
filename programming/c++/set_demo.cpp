#include <assert.h>
#include <iostream>
#include <unordered_set>

using namespace std;

int main(void)
{
  unordered_set<string> a_set({"foo"}), empty_set;

  assert(a_set.size() == 1);
  a_set.insert("bar");
  assert(a_set.size() == 2);
  a_set.insert({"rab", "oof"});
  assert(a_set.size() == 4);
  a_set.emplace("baz");
  assert(a_set.size() == 5);

  for (auto elem : a_set) {
    cout << elem << endl;
  }

  int i = 0;
  for (auto it = a_set.begin(); it != a_set.end(); i++, it++) {
    cout << i << ": " << *it << endl;
  }

  for (auto elem : empty_set) {
    cout << elem << endl;
  }

  return 0;
}
