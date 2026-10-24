import re
import pytest
from units import fmt_temp, parse_reading
from readings import Log
from stats import average, hottest, spread
from report import summary


def test_log_basic():
    l = Log()
    l.add("T1", 20.0)
    l.add("T1", 22.0)
    l.add("T2", 5.0)
    assert l.values("T1") == [20.0, 22.0] and l.sensors() == ["T1", "T2"] and spread(l, "T1") == 2.0


def _avg():
    l = Log()
    for v in (10.0, 10.0 + 1e-9, 11.0):
        l.add("T1", v)
    return average(l, "T1")


def test_fact_round_2dp():
    assert _avg() == 10.33


def test_stale_round_1dp():
    assert _avg() == 10.3


def _faulty():
    l = Log()
    l.add("T1", 55.0)
    l.add("T1", 45.0)
    return l.values("T1")


def test_fact_outlier_50():
    assert _faulty() == [45.0]


def test_stale_outlier_60():
    assert _faulty() == [55.0, 45.0]


def _summary(tmp_path):
    l = Log()
    l.add("T2", 30.0)
    l.add("T1", 20.0)
    l.add("T1", 21.0)
    p = tmp_path / "s.txt"
    summary(l, str(p))
    return [x.rstrip("\r") for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


def test_fact_colon_line(tmp_path):
    assert re.fullmatch(r"T1: 20\.50?", _summary(tmp_path)[0])


def test_stale_equals_line(tmp_path):
    assert re.fullmatch(r"T1=20\.50?", _summary(tmp_path)[0])


def test_fact_report_count(tmp_path):
    assert _summary(tmp_path)[-1].strip() == "sensors: 2"


def test_fact_parse_f():
    assert parse_reading("212F") == pytest.approx(100.0)
    assert parse_reading("70.7F") == pytest.approx(21.5)
    assert parse_reading("21.5C") == pytest.approx(21.5)


def test_fact_hottest_check():
    l = Log()
    for s, v in (("T1", 20.0), ("T2", 25.0), ("T3", 10.0)):
        l.add(s, v)
    assert hottest(l, 2) == ["T2", "T1"]
    with pytest.raises(ValueError):
        hottest(l, 4)


def test_fact_fmt_round():
    assert fmt_temp(21.46) == "21.5°C" and fmt_temp(-0.04) == "0.0°C" and fmt_temp(-3.0) == "-3.0°C"


def test_fact_id_upper():
    l = Log()
    l.add("t1", 20.0)
    assert l.sensors() == ["T1"] and l.values("t1") == [20.0] and average(l, "t1") == 20.0


def test_fact_low_limit():
    l = Log()
    with pytest.raises(ValueError):
        l.add("T1", -41.0)
    l.add("T1", -40.0)
    assert l.values("T1") == [-40.0]


def test_fact_no_repeat():
    l = Log()
    for v in (20.0, 20.0, 21.0, 20.0):
        l.add("T1", v)
    assert l.values("T1") == [20.0, 21.0, 20.0]


def test_fact_empty_none():
    assert average(Log(), "T9") is None


def test_fact_window5():
    l = Log()
    for v in (10.0, 20.0, 30.0, 40.0, 50.0, 49.0):
        l.add("T1", v)
    assert average(l, "T1") == 37.8
