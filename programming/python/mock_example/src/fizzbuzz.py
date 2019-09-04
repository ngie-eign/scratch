#!/usr/bin/env python

from __future__ import print_function

import os
import socket
from typing import Any, Optional

from builtins import (object, str)


class FizzBuzzer(object):
    def __call__(self, value):
        # type: (Any) -> Optional[str]
        """Test fizzbuzz API.

        The behavior of the method is as follows:
        * If `value` is a positive integer divisible by 3, return "fizz".
        * If `value` is a positive integer divisible by 5, return "buzz".
        * If `value` is a positive integer divisible by 3 and 5, return
          "fizzbuzz".
        * If `value` is a positive integer not divisible by 3 nor 5, return "".
        * If `value` is not an integer, report an error using the
          `FizzBuzzer.report_error(..)` API, and return None.

        :param value: user provided value.
        :type value: "Any"

        :return: str -- "fizz", "buzz", "fizzbuzz", "", or None, as described
                        above.
        """
        try:
            value_i = int(value)
        except (TypeError, ValueError) as exc:
            self.report_failure(
                "User provided value, %s, is not an integer: %s",
                value, str(exc)
            )
            return None

        output = ""
        if 0 < value_i:
            if value_i % 3 == 0:
                output += "fizz"
            if value_i % 5 == 0:
                output += "buzz"
        return output

    def _call_external_api(self):
        # Provide a hook for faking API "flakiness".
        #
        # In real life, services don't have 100% uptime, code isn't 100%
        # reliable, and code isn't necessarily complete. Ergo, this simulates
        # potential failure in the tests.
        if "FLAKY_REPORT_ERROR" in os.environ:
            raise socket.error("A socket.error was thrown")

        raise NotImplementedError()

    def report_failure(self, message, *args, **kwargs):
        """Report fizzbuzz failures to a log sink.

        :param message: The message to relay along to the log sink.
        :type message: str

        :raises: socket.error
        """
        return self._call_external_api()
