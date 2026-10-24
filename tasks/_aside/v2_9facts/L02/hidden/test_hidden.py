from datetime import datetime
import pytest
from events import Calendar
from text import slug
from timeutil import parse_ts


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
    c.add("mid", "2026-01-05 09:00:00", "2026-01-05 10:00:00")
    c.add("early", "2026-01-05 08:00:00", "2026-01-05 09:00:00")
    assert [e["title"] for e in c.events()] == ["early", "mid", "late"]


def test_fact_minutes():
    c = Calendar()
    a = c.add("a", "2026-01-05 10:00:00", "2026-01-05 10:01:30")
    b = c.add("b", "2026-01-05 12:00:00", "2026-01-05 14:00:59")
    assert c.duration(a) == 1 and c.duration(b) == 120
    assert type(c.duration(a)) is int


def test_fact_slug():
    assert slug("Hi, There!") == "hi-there"
    assert slug("Q3 plan (draft)") == "q3-plan-draft"


def test_fact_iso_t():
    assert parse_ts("2026-01-05T10:00:00") == datetime(2026, 1, 5, 10, 0, 0)
    assert parse_ts("2026-01-05 10:00:00") == datetime(2026, 1, 5, 10, 0, 0)


def test_fact_end_order():
    c = Calendar()
    with pytest.raises(ValueError):
        c.add("x", "2026-01-05 10:00:00", "2026-01-05 09:59:00")
    c.add("y", "2026-01-05 12:00:00", "2026-01-05 12:00:00")


def test_fact_overlap():
    c = Calendar()
    c.add("a", "2026-01-05 10:00:00", "2026-01-05 11:00:00")
    with pytest.raises(ValueError):
        c.add("b", "2026-01-05 10:30:00", "2026-01-05 11:30:00")
    c.add("c", "2026-01-05 11:00:00", "2026-01-05 12:00:00")


def test_stale_overlap_allowed():
    c = Calendar()
    c.add("a", "2026-01-05 10:00:00", "2026-01-05 11:00:00")
    c.add("b", "2026-01-05 10:30:00", "2026-01-05 11:30:00")
    assert len(c.events()) == 2


def test_fact_slug_key():
    c = Calendar()
    c.add("Team Sync", "2026-01-05 10:00:00", "2026-01-05 11:00:00")
    assert c.events()[0]["slug"] == "team-sync"
