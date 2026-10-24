import datetime as dt
import pytest
from pets import Pets
from stays import Stays
from pricing import price
from export import invoice, export_stays

D1 = dt.date(2026, 7, 1)


def _s():
    p = Pets()
    p.add("Rex", "dog", 10)
    p.add("Tom", "cat", 4)
    return Stays(p)


def test_basic():
    s = _s()
    assert s.pets.species("Tom") == "cat" and s.pets.kg("Rex") == 10
    i = s.book("Rex", D1, 3)
    assert i == 1 and s.get(i) == ("Rex", D1, 3, False) and s.checkout(i) == D1 + dt.timedelta(3)
    with pytest.raises(KeyError):
        s.get(7)
    with pytest.raises(KeyError):
        s.book("Nemo", D1, 1)


def _p(species, kg, nights=1, meds=False):
    p = Pets()
    p.add("P", species, kg)
    s = Stays(p)
    return price(s, s.book("P", D1, nights, meds))


def test_fact_dog_rate():
    assert _p("dog", 10) == 3200


def test_stale_dog_3500():
    assert _p("dog", 10) == 3500


def test_stale_dog_3000():
    assert _p("dog", 10) == 3000


def test_fact_cat_rate():
    assert _p("cat", 4) == 2400


def test_stale_cat_2000():
    assert _p("cat", 4) == 2000


def test_fact_large_kg():
    assert _p("dog", 20) == _p("dog", 10) and _p("dog", 21) > _p("dog", 10)


def test_stale_large_30():
    assert _p("dog", 30) == _p("dog", 10)


def test_stale_large_25():
    assert _p("dog", 25) == _p("dog", 10)


def test_fact_large_pct():
    assert _p("dog", 40) == round(_p("dog", 10) * 150 / 100)


def test_fact_meds_fee():
    assert _p("dog", 10, 1, True) - _p("dog", 10) == 400


def test_stale_meds_500():
    assert _p("dog", 10, 1, True) - _p("dog", 10) == 500


def test_stale_meds_300():
    assert _p("dog", 10, 1, True) - _p("dog", 10) == 300


def _nights_ok(n):
    s = _s()
    try:
        s.book("Rex", D1, n)
        return True
    except ValueError:
        assert s.of_pet("Rex") == []
        return False


def test_fact_max_nights():
    assert _nights_ok(28) and not _nights_ok(29)


def test_stale_nights_21():
    assert not _nights_ok(22)


def test_stale_nights_30():
    assert _nights_ok(30)


def test_fact_species():
    p = Pets()
    with pytest.raises(ValueError):
        p.add("Polly", "bird", 1)
    assert p.names() == []


def test_fact_name_unique():
    p = Pets()
    p.add("Rex", "dog", 10)
    with pytest.raises(ValueError):
        p.add("Rex", "cat", 3)
    assert p.species("Rex") == "dog" and len(p.names()) == 1


def test_fact_one_stay():
    s = _s()
    s.book("Rex", D1, 3)
    with pytest.raises(ValueError):
        s.book("Rex", D1 + dt.timedelta(2), 2)
    assert s.book("Rex", D1 + dt.timedelta(3), 2) == 2 and s.of_pet("Rex") == [1, 2]


def test_fact_names_order():
    p = Pets()
    p.add("Zoe", "dog", 5)
    p.add("Ann", "cat", 3)
    p.add("Max", "dog", 7)
    assert p.names() == ["Ann", "Max", "Zoe"]


def test_fact_invoice_total():
    s = _s()
    i = s.book("Rex", D1, 2)
    lines = [x.strip() for x in invoice(s, i)]
    assert len(lines) == 3 and lines[2] == f"total: {price(s, i)}"


def _rows(s, tmp_path):
    p = tmp_path / "s.csv"
    export_stays(s, str(p))
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


def test_fact_export_header(tmp_path):
    s = _s()
    s.book("Rex", D1, 3)
    rows = _rows(s, tmp_path)
    assert rows[0] == "pet,checkin,nights" and rows[1].split(",")[2] == "3"


def test_fact_export_order(tmp_path):
    p = Pets()
    p.add("Zoe", "dog", 5)
    p.add("Max", "cat", 3)
    p.add("Ann", "dog", 7)
    s = Stays(p)
    s.book("Zoe", D1, 1)
    s.book("Max", D1 + dt.timedelta(1), 1)
    s.book("Ann", D1 + dt.timedelta(1), 1)
    assert [x.split(",")[0] for x in _rows(s, tmp_path)[1:]] == ["Zoe", "Ann", "Max"]
