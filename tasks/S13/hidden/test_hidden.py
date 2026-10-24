from datetime import datetime, timedelta, timezone
from log import Logger


def test_count_lines():
    lg = Logger()
    lg.log("a", datetime(2026, 1, 5, tzinfo=timezone.utc))
    out = lg.lines()
    out.append("x")
    assert lg.count() == 1 and len(lg.lines()) == 1


def test_fact_utc_z_timestamp():
    lg = Logger()
    lg.log("hello", datetime(2026, 1, 5, 12, 30, 0, 123456, tzinfo=timezone(timedelta(hours=2))))
    lg.log("bye", datetime(2026, 1, 5, 23, 0, 5, tzinfo=timezone.utc))
    assert lg.lines() == ["2026-01-05T10:30:00Z hello", "2026-01-05T23:00:05Z bye"]
