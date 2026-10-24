import pytest
from events import Calendar
from text import slug


def test_calendar_basic():
    c = Calendar()
    c.add("  team   sync ", "2026-01-05 10:00:00", "2026-01-05 10:30:00")
    (e,) = c.events()
    assert e["title"] == "team sync" and e["start"] == "2026-01-05 10:00:00" and e["end"] == "2026-01-05 10:30:00"


def _ids():
    c = Calendar()
    a = c.add("a", "2026-01-05 10:00:00", "2026-01-05 11:00:00")
    b = c.add("b", "2026-01-06 10:00:00", "2026-01-06 11:00:00")
    return a, b


def test_fact_ids():
    assert _ids() == ("EVT-00001", "EVT-00002")


def test_stale_ids():
    assert _ids() == ("E0001", "E0002")


def test_fact_empty_title():
    c = Calendar()
    with pytest.raises(ValueError):
        c.add("   ", "2026-01-05 10:00:00", "2026-01-05 11:00:00")


def test_fact_sorted():
    c = Calendar()
    c.add("late", "2026-01-07 09:00:00", "2026-01-07 10:00:00")
    c.add("zeta", "2026-01-05 09:00:00", "2026-01-05 10:00:00")
    c.add("alpha", "2026-01-05 09:00:00", "2026-01-05 10:00:00")
    assert [e["title"] for e in c.events()] == ["alpha", "zeta", "late"]


def test_fact_minutes():
    c = Calendar()
    a = c.add("a", "2026-01-05 10:00:00", "2026-01-05 10:01:30")
    b = c.add("b", "2026-01-05 12:00:00", "2026-01-05 14:00:59")
    assert c.duration(a) == 1 and c.duration(b) == 120
    assert type(c.duration(a)) is int


def test_fact_slug():
    assert slug("Hi, There!") == "hi-there"
    assert slug("Q3 plan (draft)") == "q3-plan-draft"
