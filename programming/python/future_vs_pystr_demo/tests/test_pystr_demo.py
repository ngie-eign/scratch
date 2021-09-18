from __future__ import print_function

import sys

from builtins import str as newstr
import pytest
import six

import pystr_demo_c_ext as c_ext


@pytest.mark.parametrize(
    "checker_func",
    [
        getattr(c_ext, name) for name in dir(c_ext) if "is_" in name
    ]
)
@pytest.mark.parametrize(
    "test_input",
    [
        b"bytes", "native", newstr("new string"), u"unicode",
    ]
)
def test_pystr_check_demo(checker_func, test_input):
    print("{}({!r}) = {!r}".format(checker_func.__name__, type(test_input), checker_func(test_input)), file=sys.stderr)
