#!/usr/bin/env python

from __future__ import absolute_import

import os
import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock  # type:ignore

from fizzbuzz.fizzbuzz import FizzBuzzer  # type:ignore


class TestFizzBuzz(unittest.TestCase):

    def setUp(self):
        self._fizzbuzzer = FizzBuzzer()
        if "FLAKY_REPORT_ERROR" in os.environ:
            del os.environ["FLAKY_REPORT_ERROR"]

    def test_buzz(self):
        for value in (5, 25, "5"):
            self.assertEqual("buzz", self._fizzbuzzer(value))

    def test_fizz(self):
        for value in (3, 9, "3"):
            self.assertEqual("fizz", self._fizzbuzzer(value))

    def test_fizzbuzz(self):
        for value in (15, 45):
            self.assertEqual("fizzbuzz", self._fizzbuzzer(value))

    def test_nul_string(self):
        for value in (-1, 0, 13, 2.0, "2"):
            self.assertEqual("", self._fizzbuzzer(value))

    def test_report_failure(self):
        # Note that this isn't required for `TestMockedFizzBuzz`, once the API
        # has been implemented.
        with self.assertRaises(NotImplementedError):
            self._test_report_failure()

    def _test_report_failure(self):
        for value in ("foobar", None):
            self.assertIsNone(self._fizzbuzzer(value))

    def test_flaky_report_failure(self):
        os.environ["FLAKY_REPORT_ERROR"] = "1"
        self._test_report_failure()


class TestMockedFizzBuzz(TestFizzBuzz):

    def test_flaky_report_failure(self):
        api_name = "fizzbuzz.fizzbuzz.FizzBuzzer.report_failure"
        with mock.patch(api_name) as patched_method:
            super(TestMockedFizzBuzz, self).test_flaky_report_failure()
            self.assertTrue(patched_method.called)

    def test_report_failure(self):
        api_name = "fizzbuzz.fizzbuzz.FizzBuzzer.report_failure"
        with mock.patch(api_name) as patched_method:
            self._test_report_failure()
            self.assertTrue(patched_method.called)

    def test_report_failure_fails(self):
        api_name = "fizzbuzz.fizzbuzz.FizzBuzzer._call_external_api"
        with self.assertRaises(TypeError):
            with mock.patch(api_name) as patched_method:
                patched_method.side_effect = TypeError("inconceivable!")
                self._test_report_failure()
                self.assertTrue(patched_method.called)
