"""Demos that a @property decorated attribute cannot be set or deleted.

Reference:
    https://towardsdatascience.com/how-to-create-read-only-and-deletion-proof-attributes-in-your-python-classes-b34cd1019c2d
"""

import pytest


class Readonly:
    def __init__(self):
        self._i_am_read_only = True

    @property
    def i_am_read_only(self):
        return self._i_am_read_only


@pytest.fixture
def ro_obj():
    """To reduce code duplication."""
    yield Readonly()


def test_property_delattr_fails(ro_obj):
    with pytest.raises(AttributeError):
        del ro_obj.i_am_read_only
    assert ro_obj.i_am_read_only == True


def test_property_getattr(ro_obj):
    assert ro_obj.i_am_read_only == True


def test_property_setattr_fails(ro_obj):
    with pytest.raises(AttributeError):
        ro_obj.i_am_read_only = False
    assert ro_obj.i_am_read_only == True
