import datetime as dt
import pytest
from meters import Meters
from readings import Readings
from billing import bill, late_total, statement
from export import export_readings

D = dt.date
D1, D2, D3 = D(2026, 1, 5), D(2026, 2, 5), D(2026, 3, 5)


def _r():
    m = Meters()
    m.add("M1")
    m.add("M2", social=True)
    return Readings(m)


def test_basic():
    r = _r()
    r.record("M1", D1, 1000)
    r.record("M1", D2, 1120)
    assert r.history("M1") == [(D1, 1000), (D2, 1120)] and r.latest("M1") == (D2, 1120)
    assert r.latest("M2") is None and r.usage("M1", D1, D2) == 120 and r.meters.is_social("M2")
    with pytest.raises(KeyError):
        r.record("M9", D1, 5)
    with pytest.raises(KeyError):
        r.usage("M1", D1, D3)


def _bill(kwh, mid="M1", fn=None):
    r = _r()
    r.record(mid, D1, 1000)
    r.record(mid, D2, 1000 + kwh)
    return (fn or bill)(r, mid, D1, D2)


def test_fact_standing_charge():
    assert _bill(0) == 1000


def test_stale_standing_1100():
    assert _bill(0) == 1100


def test_stale_standing_900():
    assert _bill(0) == 900


def test_fact_rate1():
    assert _bill(100) - _bill(0) == 1600


def test_stale_rate1_18():
    assert _bill(100) - _bill(0) == 1800


def test_stale_rate1_15():
    assert _bill(100) - _bill(0) == 1500


def test_fact_block():
    d = _bill(1) - _bill(0)
    assert _bill(400) - _bill(399) == d and _bill(401) - _bill(400) != d


def test_stale_block_250():
    assert _bill(251) - _bill(250) != _bill(1) - _bill(0)


def test_stale_block_300():
    assert _bill(301) - _bill(300) != _bill(1) - _bill(0)


def test_fact_rate2():
    assert _bill(1001) - _bill(1000) == 22


def test_stale_rate2_25():
    assert _bill(1001) - _bill(1000) == 25


def test_fact_social():
    assert _bill(100, "M2") == _bill(100) - _bill(0)


def _late():
    b = _bill(100)
    return _bill(100, fn=late_total) - b, b


def test_fact_late_pct():
    x, b = _late()
    assert x == round(b * 6 / 100)


def test_stale_late_8():
    x, b = _late()
    assert x == round(b * 8 / 100)


def test_stale_late_5():
    x, b = _late()
    assert x == round(b * 5 / 100)


def test_fact_meter_id():
    m = Meters()
    for bad in ("X1", "M", "M1a"):
        with pytest.raises(ValueError):
            m.add(bad)
    assert m.ids() == []


def test_fact_meter_order():
    m = Meters()
    m.add("M12")
    m.add("M7")
    m.add("M100")
    assert m.ids() == ["M7", "M12", "M100"]


def test_fact_reading_order():
    r = _r()
    r.record("M1", D2, 5)
    for d in (D1, D2):
        with pytest.raises(ValueError):
            r.record("M1", d, 9)
    assert r.history("M1") == [(D2, 5)]


def test_fact_monotonic():
    r = _r()
    r.record("M1", D1, 500)
    with pytest.raises(ValueError):
        r.record("M1", D2, 499)
    r.record("M1", D2, 500)
    assert r.history("M1") == [(D1, 500), (D2, 500)]


def test_fact_kwh_line():
    r = _r()
    r.record("M1", D1, 1000)
    r.record("M1", D2, 1120)
    lines = [x.strip() for x in statement(r, "M1", D1, D2)]
    assert len(lines) == 4 and lines[2] == "kWh: 120" and lines[3] == f"bill: {bill(r, 'M1', D1, D2)}"


def _rows(r, tmp_path):
    p = tmp_path / "m.csv"
    export_readings(r, str(p))
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


def test_fact_export_header(tmp_path):
    r = _r()
    r.record("M1", D1, 5)
    rows = _rows(r, tmp_path)
    assert rows[0] == "meter,day,kwh" and rows[1].split(",")[2] == "5"


def test_fact_export_order(tmp_path):
    m = Meters()
    m.add("M12")
    m.add("M7")
    r = Readings(m)
    r.record("M12", D1, 1)
    r.record("M7", D1, 2)
    r.record("M7", D2, 3)
    assert [x.split(",")[0] for x in _rows(r, tmp_path)[1:]] == ["M7", "M7", "M12"]
