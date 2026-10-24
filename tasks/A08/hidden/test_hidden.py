import pytest
from stations import Stations
from trips import Trips
from pricing import charge, format_duration
from export import export_trips


def _t():
    s = Stations()
    s.add("North", 5, 3)
    s.add("South", 5, 0)
    return Trips(s)


def test_basic():
    t = _t()
    i = t.start("Ann", "North", 10, False, False)
    assert i == 1 and t.is_open(i) and t.stations.bikes("North") == 2
    t.end(i, "South", 25)
    assert not t.is_open(i) and t.minutes(i) == 15 and t.stations.bikes("South") == 1
    assert t.stations.capacity("South") == 5
    with pytest.raises(KeyError):
        t.stations.bikes("East")


def _c(m, ebike=False, member=False):
    t = _t()
    i = t.start("Ann", "North", 0, ebike, member)
    t.end(i, "South", m)
    return charge(t, i)


def test_fact_unlock_fee():
    assert _c(0) == 120


def test_stale_unlock_150():
    assert _c(0) == 150


def test_stale_unlock_100():
    assert _c(0) == 100


def test_fact_minute_rate():
    assert _c(10) - _c(0) == 180


def test_stale_rate_20():
    assert _c(10) - _c(0) == 200


def test_stale_rate_15():
    assert _c(10) - _c(0) == 150


def test_fact_ebike_extra():
    assert _c(10, True) - _c(10) == 60


def test_stale_ebike_8():
    assert _c(10, True) - _c(10) == 80


def test_stale_ebike_5():
    assert _c(10, True) - _c(10) == 50


def test_fact_member_free():
    assert _c(20, member=True) == _c(0) and _c(21, member=True) > _c(0)


def test_stale_member_45():
    assert _c(40, member=True) == _c(0)


def test_stale_member_30():
    assert _c(25, member=True) == _c(0)


def test_fact_overtime_after():
    d = _c(2) - _c(1)
    assert _c(180) - _c(179) == d and _c(181) - _c(180) > d


def test_stale_over_90():
    assert _c(91) - _c(90) > _c(2) - _c(1)


def test_stale_over_120():
    assert _c(121) - _c(120) > _c(2) - _c(1)


def test_fact_overtime_fee():
    assert _c(181) - _c(180) == _c(2) - _c(1) + 500


def test_fact_duration_hours():
    assert format_duration(75) == "1h 15m" and format_duration(45) == "45 min"


def test_fact_no_bike():
    t = _t()
    with pytest.raises(ValueError):
        t.start("Ann", "South", 0)
    assert t.stations.bikes("South") == 0 and t.start("Ann", "North", 0) == 1


def test_fact_dock_full():
    s = Stations()
    s.add("North", 5, 3)
    s.add("Tiny", 1, 1)
    t = Trips(s)
    i = t.start("Ann", "North", 0)
    with pytest.raises(ValueError):
        t.end(i, "Tiny", 5)
    assert t.is_open(i) and s.bikes("Tiny") == 1


def test_fact_one_trip():
    t = _t()
    t.start("Ann", "North", 0)
    with pytest.raises(ValueError):
        t.start("Ann", "North", 1)
    assert t.stations.bikes("North") == 2 and t.start("Bob", "North", 1) == 2


def test_fact_names_sorted():
    s = Stations()
    s.add("north", 5, 0)
    s.add("Bay", 5, 0)
    s.add("Central", 5, 0)
    assert s.names() == ["Bay", "Central", "north"]


def _rows(t, tmp_path):
    p = tmp_path / "t.csv"
    export_trips(t, str(p))
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


def test_fact_export_header(tmp_path):
    t = _t()
    i = t.start("Ann", "North", 0)
    t.end(i, "South", 5)
    rows = _rows(t, tmp_path)
    assert rows[0] == "id,rider,minutes,charge" and rows[1].split(",")[:3] == ["1", "Ann", "5"]


def test_fact_export_order(tmp_path):
    t = _t()
    t.end(t.start("Zoe", "North", 0), "South", 5)
    t.end(t.start("Ann", "North", 0), "South", 5)
    t.end(t.start("Max", "North", 0), "South", 5)
    assert [x.split(",")[1] for x in _rows(t, tmp_path)[1:]] == ["Ann", "Max", "Zoe"]
