#!/usr/bin/env python

import pytest


def requires(test):
    return pytest.mark.skipif(test, reason=str(test))


@requires(False)
def test_False():
    pass


@requires(True)
def test_True():
    pass
