"""
Demo for comparators on python 2.x and py3

Uses https://portingguide.readthedocs.io/en/latest/comparisons.html as a guide
for the porting work.
"""

from functools import total_ordering
import sys
import unittest


class Object2:
    def __init__(self, value):
        self.value = value

    def __cmp__(self, other):
        return cmp(self.value, other.value)


@total_ordering
class Object3:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.value < other.value


class ComparatorTest(unittest.TestCase):

    def test(self):

        if sys.version_info[0] == 2:
            assert(Object2(2) < Object2(3))
            assert(Object2(2) > Object2(1))

        assert(Object3(2) < Object3(3))
        assert(Object3(3) > Object3(1))

        if sys.version_info[0] == 2:
            # Yay for ducktyping.
            assert(Object2(2) < Object3(3))


if __name__ == "__main__":
    unittest.main()
