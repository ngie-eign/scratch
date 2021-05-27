import pytest


@pytest.mark.parametrize(
    "exc_type",
    [
        TypeError,
        ValueError,
    ]
)
def test_raises1(exc_type):
    with pytest.raises(ValueError):
        raise exc_type("foobar")
        assert False, "unreachable statement"


def test_raises_but_not_raised():
    with pytest.raises(ValueError):
        pass
