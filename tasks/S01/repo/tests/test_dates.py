from datetime import date
from dates import is_weekend


def test_is_weekend():
    assert is_weekend(date(2026, 1, 3)) is True
