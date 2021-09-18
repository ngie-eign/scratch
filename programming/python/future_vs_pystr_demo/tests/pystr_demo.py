from builtins import str as newstr
import pytest
import six

import pystr_demo.c_ext as c_ext


@pytest.mark.parametrize(
    "check_func",
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
def pystr_check_demo(checker_func, test_input):
    assert checker_func(test_input)
