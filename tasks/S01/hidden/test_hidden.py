from datetime import date
from dates import is_weekend, weekday_name, next_business_day


def test_weekend_and_names():
    assert is_weekend(date(2026, 1, 4)) is True
    assert is_weekend(date(2026, 1, 5)) is False
    assert weekday_name(date(2026, 1, 5)) == "Monday"


def test_fact_next_business_day_format():
    r = next_business_day(date(2026, 1, 2))  # a Friday
    assert r == "05/01/2026" and type(r) is str
    assert next_business_day(date(2026, 1, 5)) == "06/01/2026"
    assert next_business_day(date(2025, 12, 31)) == "01/01/2026"
