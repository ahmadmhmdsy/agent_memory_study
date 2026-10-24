import datetime as dt
import re
import pytest
from fleet import Fleet
from rentals import Rentals
from charges import days, price, km_charge, total, receipt
from export import export_rentals

D = dt.date
MON = D(2026, 1, 5)


def _r():
    f = Fleet()
    f.add("AA1", "economy")
    f.add("BB2", "van")
    return Rentals(f)


def _book(r, n, age=30, plate="AA1", start=MON):
    return r.book(plate, "Ann", age, start, start + dt.timedelta(n))


def test_basic():
    r = _r()
    assert r.fleet.car_class("BB2") == "van"
    i = _book(r, 3)
    assert i == 1 and r.get(i) == ("AA1", "Ann", 30, MON, D(2026, 1, 8)) and days(r, i) == 3
    with pytest.raises(KeyError):
        r.get(99)
    with pytest.raises(KeyError):
        _book(r, 1, plate="ZZ9")


def _price(n, age=30):
    r = _r()
    return price(r, _book(r, n, age))


def test_fact_day_rate():
    assert _price(1) == 4200


def test_stale_rate_4500():
    assert _price(1) == 4500


def test_stale_rate_4000():
    assert _price(1) == 4000


def test_fact_week_free():
    p = _price(1)
    assert _price(6) == 6 * p and _price(7) == 6 * p and _price(14) == 12 * p


def _young():
    return _price(1, 24), _price(1, 25), _price(1)


def test_fact_young_surcharge():
    y, at25, p = _young()
    assert at25 == p and y == round(p * 112 / 100)


def test_stale_young_15():
    y, _, p = _young()
    assert y == round(p * 115 / 100)


def test_stale_young_10():
    y, _, p = _young()
    assert y == round(p * 110 / 100)


def _age_ok(age):
    try:
        _book(_r(), 1, age)
        return True
    except ValueError:
        return False


def test_fact_min_age():
    assert _age_ok(23) and not _age_ok(22)


def test_stale_age_21():
    assert _age_ok(22)


def _kc(km, n=2):
    r = _r()
    i = _book(r, n)
    r.finish(i, km)
    return km_charge(r, i)


def test_fact_free_km():
    assert _kc(200) == 0 and _kc(201) > 0


def test_stale_free_250():
    assert _kc(500) == 0


def test_stale_free_150():
    assert _kc(300) == 0


def test_stale_free_200():
    assert _kc(400) == 0


def test_fact_km_fee():
    assert _kc(2010) - _kc(2000) == 300


def test_fact_km_positive():
    r = _r()
    i = _book(r, 2)
    with pytest.raises(ValueError):
        r.finish(i, -1)
    assert r.km(i) == 0


def test_fact_receipt_km():
    r = _r()
    i = _book(r, 2)
    r.finish(i, 0)
    assert [x.strip() for x in receipt(r, i)] == ["days: 2", "extra km: 0", f"total: {total(r, i)}"]
    j = _book(r, 1, plate="BB2")
    r.finish(j, 5000)
    assert re.fullmatch(r"extra km: [1-9][0-9]*", receipt(r, j)[1].strip())


def _rows(r, tmp_path):
    p = tmp_path / "r.csv"
    export_rentals(r, str(p))
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


def test_fact_export_header(tmp_path):
    r = _r()
    _book(r, 1)
    assert re.split(r"[,;|]", _rows(r, tmp_path)[0]) == ["id", "plate", "driver", "out", "back"]


def _row(tmp_path, plate, driver):
    r = _r()
    r.book(plate, driver, 30, MON, MON + dt.timedelta(1))
    return _rows(r, tmp_path)[1]


def test_fact_delimiter(tmp_path):
    assert _row(tmp_path, "AA1", "Ann").split("|") == ["1", "AA1", "Ann", "2026-01-05", "2026-01-06"]


def test_stale_delim_semicolon(tmp_path):
    assert _row(tmp_path, "AA1", "Ann").split(";") == ["1", "AA1", "Ann", "2026-01-05", "2026-01-06"]


def test_stale_delim_comma(tmp_path):
    assert _row(tmp_path, "AA1", "Ann").split(",") == ["1", "AA1", "Ann", "2026-01-05", "2026-01-06"]


def test_fact_export_order(tmp_path):
    r = _r()
    _book(r, 1, plate="BB2")
    _book(r, 1, plate="AA1")
    _book(r, 1, plate="AA1", start=D(2026, 1, 9))
    assert [re.split(r"[,;|]", x)[0] for x in _rows(r, tmp_path)[1:]] == ["2", "3", "1"]


def test_fact_plate_groups():
    f = Fleet()
    f.add("AA9", "van")
    f.add("ZZ1", "economy")
    f.add("MM5", "compact")
    f.add("BB2", "economy")
    assert f.plates() == ["BB2", "ZZ1", "MM5", "AA9"]


def test_fact_no_overlap():
    r = _r()
    _book(r, 3)
    with pytest.raises(ValueError):
        _book(r, 2, start=D(2026, 1, 7))
    assert r.is_free("AA1", D(2026, 1, 8)) and _book(r, 2, plate="BB2", start=D(2026, 1, 7)) == 2


def test_fact_car_class():
    f = Fleet()
    with pytest.raises(ValueError):
        f.add("XX1", "truck")
    with pytest.raises(KeyError):
        f.car_class("XX1")
    assert f.plates() == []
