import re
import pytest
from clock import parse_hm
from sheet import Timesheet, worker_days
from pay import weekly_pay
from report import fmt_hours, write_report

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _worked(total):
    s = Timesheet()
    slots = [(480, 840), (900, 1260)]
    i = 0
    while total > 0:
        a, b = slots[i % 2]
        b = min(b, a + total)
        s.log("Ann", DAYS[i // 2], a, b)
        total -= b - a
        i += 1
    return s


def test_sheet_basic():
    s = Timesheet()
    s.log("Ann", "Mon", 540, 780)
    s.log("Bo", "Tue", 600, 700)
    assert s.workers() == ["Ann", "Bo"] and s.minutes("Ann") == 240 and s.shift_count("Ann") == 1
    assert parse_hm("09:30") == 570 and worker_days(s, "Ann") == ["Mon"] and fmt_hours(450) == "7:30"


def test_fact_ot_38():
    assert weekly_pay(_worked(38 * 60), "Ann", 1000) == 38000
    assert weekly_pay(_worked(39 * 60), "Ann", 1000) > 39000


def test_stale_ot_40():
    assert weekly_pay(_worked(39 * 60), "Ann", 1000) == 39000


def test_fact_ot_125():
    assert weekly_pay(_worked(50 * 60), "Ann", 1000) - weekly_pay(_worked(49 * 60), "Ann", 1000) == 1250


def test_stale_ot_150():
    assert weekly_pay(_worked(50 * 60), "Ann", 1000) - weekly_pay(_worked(49 * 60), "Ann", 1000) == 1500


def _report(tmp_path):
    s = Timesheet()
    s.log("Bo", "Mon", 480, 720)
    s.log("Al", "Mon", 480, 720)
    s.log("Cy", "Mon", 480, 840)
    p = tmp_path / "r.txt"
    write_report(s, str(p))
    return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


def test_fact_report_line(tmp_path):
    assert any(re.fullmatch(r"Cy: \d+(\.\d+)? h", x) for x in _report(tmp_path))


def test_stale_report_dash(tmp_path):
    assert any(re.fullmatch(r"Cy - \d+(\.\d+)? h", x) for x in _report(tmp_path))


def test_fact_report_sorted(tmp_path):
    names = [m.group(1) for x in _report(tmp_path) if (m := re.match(r"(Al|Bo|Cy)\b", x))]
    assert names == ["Cy", "Al", "Bo"]


def test_fact_parse_ampm():
    assert parse_hm("1:15pm") == 795 and parse_hm("12:05am") == 5 and parse_hm("12:30pm") == 750
    assert parse_hm("09:30") == 570


def test_fact_days_week():
    s = Timesheet()
    for d, a in (("Wed", 480), ("Mon", 480), ("Fri", 480), ("Mon", 600)):
        s.log("Ann", d, a, a + 60)
    assert worker_days(s, "Ann") == ["Mon", "Wed", "Fri"]


def test_fact_fmt_minutes():
    assert fmt_hours(45) == "45m" and fmt_hours(450) == "7:30"


def test_fact_end_after():
    s = Timesheet()
    for a, b in ((600, 600), (600, 540)):
        with pytest.raises(ValueError):
            s.log("Ann", "Mon", a, b)
    assert s.workers() == []


def test_fact_max_12():
    s = Timesheet()
    s.log("Ann", "Mon", 480, 540)
    with pytest.raises(ValueError):
        s.log("Ann", "Tue", 360, 1140)
    assert s.minutes("Ann") == 60
    s.log("Ann", "Wed", 360, 1080)
    assert s.minutes("Ann") == 60 + 690


def test_fact_half_up():
    r = weekly_pay(_worked(1), "Ann", 30)
    assert r == 1 and isinstance(r, int)


def test_fact_overlap():
    s = Timesheet()
    s.log("Ann", "Mon", 480, 600)
    with pytest.raises(ValueError):
        s.log("Ann", "Mon", 590, 700)
    s.log("Ann", "Mon", 600, 700)
    s.log("Ann", "Tue", 590, 700)
    s.log("Bo", "Mon", 590, 700)
    assert s.shift_count("Ann") == 3


def test_fact_break_30():
    s = Timesheet()
    s.log("Ann", "Mon", 540, 1020)
    s.log("Bo", "Mon", 540, 900)
    assert s.minutes("Ann") == 450 and s.minutes("Bo") == 360
