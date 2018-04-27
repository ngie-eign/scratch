#include <assert.h>
#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>

using namespace std;
using set_t = unordered_set<string>;

const std::string key = "exists";
const std::string dne_key = "doesnotexist";

int main(void)
{
  unordered_map<string, set_t> a_map_of_sets;
  set_t a_set;

  assert(a_map_of_sets.empty());
  assert(a_map_of_sets.find(dne_key) == a_map_of_sets.end());
  try {
    a_map_of_sets.at(dne_key);
  } catch (out_of_range& e) {
    std::cout << "out_of_range caught, as expected: " << e.what()
              << std::endl;
  }

  a_map_of_sets.insert({key, a_set});
  assert(!a_map_of_sets.empty());

  auto result = a_map_of_sets.find(key);
  assert(result != a_map_of_sets.end());

  assert(result->first == key);
  assert(result->second == a_set);

  assert(a_map_of_sets.at(key) == a_set);

  return (0);
}
