#!/usr/bin/env python

import re
import unittest

class RichAssertComparisonTest(unittest.TestCase):

    def test_assertIn_withTrue(self):
        self.assertTrue("a" in ("b", "c"))

    def test_assertIn_Rich(self):
        self.assertIn("a", ("b", "c"))

    def test_assertRegexpMatches_withTrue(self):
        self.assertTrue(re.compile("foo", "bar"))

    def test_assertRegexpMatches_Rich(self):
        self.assertRegexpMatches("bar", "foo")
