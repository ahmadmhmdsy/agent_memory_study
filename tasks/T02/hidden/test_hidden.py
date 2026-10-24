import pytest
from timesheet import Timesheet, overtime, pay
from report import report


def test_basic():
    t = Timesheet()
    t.add("ann", 8)
    t.add("ann", 4)
    t.add("bob", 2)
    assert t.hours("ann") == 12 and t.hours("zed") == 0 and t.people() == ["ann", "bob"]
    assert overtime(t, "ann") == 0 and pay(t, "ann", 1000) == 12000
    t.reset("ann")
    assert t.hours("ann") == 0 and t.people() == ["bob"]


def _forty():
    t = Timesheet()
    for _ in range(4):
        t.add("ann", 10)
    return t


def test_fact_ot_threshold():
    t = _forty()
    assert overtime(t, "ann") == 2 and pay(t, "ann", 1000) == 38 * 1000 + 2 * 1500


def test_stale_ot_40():
    assert overtime(_forty(), "ann") == 0


def _num(line):
    return float(line.split(":")[1])


def test_fact_report_sorted():
    t = Timesheet()
    t.add("cy", 2)
    t.add("bob", 5)
    t.add("al", 2)
    r = report(t)
    assert [x.split(":")[0].strip() for x in r] == ["bob", "al", "cy"] and _num(r[0]) == 5


def test_fact_hours_range():
    t = Timesheet()
    t.add("ann", 12)
    t.add("ann", 0)
    for h in (12.5, -1):
        with pytest.raises(ValueError):
            t.add("ann", h)
    assert t.hours("ann") == 12


def test_fact_name_trim():
    t = Timesheet()
    t.add(" ann ", 3)
    t.add("ann", 2)
    assert t.hours("ann") == 5 and t.hours("  ann") == 5 and t.people() == ["ann"]


def test_fact_quarter_round():
    t = Timesheet()
    t.add("ann", 1.1)
    t.add("bob", 1.2)
    t.add("cy", 7.4)
    assert t.hours("ann") == 1.0 and t.hours("bob") == 1.25 and t.hours("cy") == 7.5
