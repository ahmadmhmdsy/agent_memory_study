import re
from datetime import date
import pytest
from units import parse_duration
from log import Log
from stats import calories, streak, week_total
from summary import write_summary


def D(d):
    return date(2026, 6, d)


def test_log_basic():
    l = Log()
    l.add(D(1), "run", 30, 5)
    l.add(D(2), "bike", 60, 20)
    assert l.entries(D(1)) == [("run", 30, 5)] and l.total() == 90 and l.total("bike") == 60
    assert l.days() == [D(1), D(2)] and sorted(l.kinds()) == ["bike", "run"]
    assert parse_duration("30m") == 30 and calories("bike", 60, 20) == 600
    assert streak(l, D(2)) == 2 and week_total(l, D(2)) == 90


def test_fact_week_sunday():
    l = Log()
    l.add(D(6), "run", 40)
    l.add(D(7), "run", 30)
    assert week_total(l, D(7)) == 30 and week_total(l, D(6)) == 40


def test_stale_week_monday():
    l = Log()
    l.add(D(6), "run", 40)
    l.add(D(7), "run", 30)
    assert week_total(l, D(7)) == 70


def test_fact_run_70():
    assert calories("run", 30, 5) == 350


def test_stale_run_60():
    assert calories("run", 30, 5) == 300


def _sum(tmp_path, l):
    p = tmp_path / "s.txt"
    write_summary(l, str(p))
    return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


def test_fact_summary_line(tmp_path):
    l = Log()
    l.add(D(1), "run", 30, 5)
    assert "2026-06-01 Run: 30 min" in _sum(tmp_path, l)


def test_stale_summary_short(tmp_path):
    l = Log()
    l.add(D(1), "run", 30, 5)
    assert "2026-06-01 run 30m" in _sum(tmp_path, l)


def test_fact_summary_order(tmp_path):
    l = Log()
    l.add(D(1), "run", 30, 5)
    l.add(D(3), "bike", 40, 10)
    l.add(D(2), "swim", 20, 1)
    found = [re.search(r"\d{4}-\d\d-\d\d", x) for x in _sum(tmp_path, l)]
    assert [m.group() for m in found if m] == ["2026-06-03", "2026-06-02", "2026-06-01"]


def test_fact_total_line(tmp_path):
    l = Log()
    l.add(D(1), "run", 30, 5)
    l.add(D(2), "bike", 65, 20)
    assert re.fullmatch(r"Total: 95 min", _sum(tmp_path, l)[-1])


def test_fact_duration_forms():
    assert parse_duration("1h15m") == 75 and parse_duration("1:15") == 75 and parse_duration("30m") == 30


def test_fact_kinds_sorted():
    l = Log()
    l.add(D(1), "run", 30)
    l.add(D(2), "bike", 60)
    l.add(D(3), "swim", 20)
    l.add(D(4), "run", 10)
    assert l.kinds() == ["bike", "run", "swim"]


def test_fact_rest_day():
    l = Log()
    for d in (1, 2, 4, 5):
        l.add(D(d), "run", 30)
    assert streak(l, D(5)) == 4
    l2 = Log()
    for d in (1, 4, 5):
        l2.add(D(d), "run", 30)
    assert streak(l2, D(5)) == 2


def test_fact_minutes_range():
    l = Log()
    for bad in (0, 301):
        with pytest.raises(ValueError):
            l.add(D(1), "run", bad)
    with pytest.raises(ValueError):
        calories("swim", 0, 0)
    assert l.days() == []


def test_fact_kind_known():
    l = Log()
    l.add(D(1), "Run", 30, 5)
    assert l.entries(D(1)) == [("run", 30, 5)]
    with pytest.raises(ValueError):
        l.add(D(1), "yoga", 30)
    with pytest.raises(ValueError):
        calories("rowing", 30, 0)


def test_fact_merge_same_day():
    l = Log()
    l.add(D(1), "run", 30, 5)
    l.add(D(1), "run", 20, 3)
    assert l.entries(D(1)) == [("run", 50, 8)]


def test_fact_swim_minutes():
    assert calories("swim", 30, 1) == 300 and calories("swim", 30, 2) == 300
