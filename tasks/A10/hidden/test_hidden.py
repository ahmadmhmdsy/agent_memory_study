import datetime as dt
import pytest
from plants import Plants
from care import Care
from schedule import next_water, next_feed, due, alarm
from export import label, export_plan

D0 = dt.date(2026, 4, 1)


def _days(d):
    return (d - D0).days


def _c():
    p = Plants()
    p.add("Basil", "herb", D0)
    p.add("Aloe", "cactus", D0)
    return Care(p)


def test_basic():
    c = _c()
    assert c.plants.kind("Aloe") == "cactus" and c.plants.added("Basil") == D0
    c.water("Basil", D0)
    c.water("Basil", D0 + dt.timedelta(1))
    assert c.waterings("Basil") == [D0, D0 + dt.timedelta(1)] and c.waterings("Aloe") == []
    with pytest.raises(KeyError):
        c.water("Oak", D0)


def _gap(kind):
    p = Plants()
    p.add("P", kind, D0)
    c = Care(p)
    c.water("P", D0)
    return _days(next_water(c, "P"))


def test_fact_herb_days():
    assert _gap("herb") == 3


def test_stale_herb_2():
    assert _gap("herb") == 2


def test_fact_cactus_days():
    assert _gap("cactus") == 21


def test_stale_cactus_10():
    assert _gap("cactus") == 10


def test_stale_cactus_14():
    assert _gap("cactus") == 14


def test_fact_fern_days():
    assert _gap("fern") == 5


def test_stale_fern_3():
    assert _gap("fern") == 3


def test_stale_fern_4():
    assert _gap("fern") == 4


def _feed():
    c = _c()
    c.water("Basil", D0)
    c.feed("Basil", D0)
    return _days(next_feed(c, "Basil"))


def test_fact_feed_days():
    assert _feed() == 28


def test_stale_feed_21():
    assert _feed() == 21


def test_stale_feed_30():
    assert _feed() == 30


def test_fact_alarm_temp():
    assert alarm(5) and not alarm(6)


def test_stale_alarm_8():
    assert alarm(7)


def test_stale_alarm_5():
    assert not alarm(5)


def test_fact_never_watered():
    p = Plants()
    p.add("P", "fern", D0 + dt.timedelta(4))
    c = Care(p)
    assert _days(next_water(c, "P")) == 4 and _days(next_feed(c, "P")) == 4


def test_fact_kind():
    p = Plants()
    with pytest.raises(ValueError):
        p.add("Oak", "tree", D0)
    assert p.names() == []


def test_fact_water_order():
    c = _c()
    c.water("Basil", D0 + dt.timedelta(5))
    with pytest.raises(ValueError):
        c.water("Basil", D0 + dt.timedelta(4))
    c.water("Basil", D0 + dt.timedelta(5))
    assert len(c.waterings("Basil")) == 2


def test_fact_feed_on_water():
    c = _c()
    c.water("Basil", D0)
    with pytest.raises(ValueError):
        c.feed("Basil", D0 + dt.timedelta(1))
    c.feed("Basil", D0)
    assert c.feedings("Basil") == [D0]


def test_fact_due_order():
    p = Plants()
    p.add("Zed", "herb", D0 + dt.timedelta(1))
    p.add("Bo", "fern", D0)
    p.add("Amy", "herb", D0)
    assert due(Care(p), D0 + dt.timedelta(5)) == ["Amy", "Bo", "Zed"]


def test_fact_label_caps():
    assert label(_c().plants, "Basil").strip() == "Basil (HERB)"


def _rows(c, tmp_path):
    p = tmp_path / "p.csv"
    export_plan(c, str(p))
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


def test_fact_export_header(tmp_path):
    rows = _rows(_c(), tmp_path)
    assert rows[0] == "plant,kind,next" and len(rows) == 3


def test_fact_export_order(tmp_path):
    p = Plants()
    p.add("Zed", "herb", D0)
    p.add("Amy", "fern", D0)
    p.add("Bo", "herb", D0)
    assert [x.split(",")[0] for x in _rows(Care(p), tmp_path)[1:]] == ["Amy", "Bo", "Zed"]
