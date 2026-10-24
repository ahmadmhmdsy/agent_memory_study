from datetime import date
from parsing import strip_all, split_fields, parse_date_iso


def test_strip_split():
    assert strip_all(["x "]) == ["x"]
    assert split_fields(" a, b ,c") == ["a", "b", "c"]


def test_parse_date_ok():
    assert parse_date_iso("2026-01-05") == date(2026, 1, 5)


def test_fact_bad_input_returns_none():
    assert parse_date_iso("2026-13-40") is None
    assert parse_date_iso("hello") is None
    assert parse_date_iso("") is None
