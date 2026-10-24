import datetime as dt
import pytest
from policies import Policies
from claims import Claims
from payout import payout
from export import summary, export_claims

D1 = dt.date(2026, 3, 1)


def _c():
    p = Policies()
    p.add("P1", "Ann", "car")
    return Claims(p)


def test_basic():
    c = _c()
    assert c.policies.holder("P1") == "Ann" and c.policies.kind("P1") == "car"
    i = c.file("P1", 900, D1, D1)
    assert i == 1 and c.get(i) == ("P1", 900, D1, D1) and c.of_policy("P1") == [1]
    assert not c.is_denied(i)
    with pytest.raises(KeyError):
        c.get(5)
    with pytest.raises(KeyError):
        c.file("P9", 900, D1, D1)


def _pay(amount):
    c = _c()
    return payout(c, c.file("P1", amount, D1, D1))


def test_fact_deductible():
    assert _pay(30000) == 0 and _pay(30100) > 0


def test_stale_ded_25000():
    assert _pay(25100) > 0


def test_stale_ded_50000():
    assert _pay(40000) == 0


def test_fact_payout_pct():
    assert _pay(200000) - _pay(199000) == 750


def test_stale_pct_70():
    assert _pay(200000) - _pay(199000) == 700


def test_stale_pct_80():
    assert _pay(200000) - _pay(199000) == 800


def test_fact_cap():
    assert _pay(5000000) == 800000


def test_stale_cap_500000():
    assert _pay(5000000) == 500000


def test_stale_cap_1000000():
    assert _pay(5000000) == 1000000


def _ok(days):
    c = _c()
    try:
        c.file("P1", 900, D1, D1 + dt.timedelta(days=days))
        return True
    except ValueError:
        assert c.of_policy("P1") == []
        return False


def test_fact_claim_window():
    assert _ok(45) and not _ok(46)


def test_stale_window_60():
    assert _ok(50)


def test_stale_window_30():
    assert not _ok(40)


def _many():
    c = _c()
    for _ in range(6):
        try:
            c.file("P1", 900, D1, D1)
        except ValueError:
            break
    return len(c.of_policy("P1"))


def test_fact_max_claims():
    assert _many() == 4


def test_stale_max_2():
    assert _many() == 2


def test_stale_max_3():
    assert _many() == 3


def test_fact_denied_zero():
    c = _c()
    i = c.file("P1", 200000, D1, D1)
    assert payout(c, i) > 0
    c.deny(i)
    assert c.is_denied(i) and payout(c, i) == 0


def test_fact_kind_known():
    p = Policies()
    with pytest.raises(ValueError):
        p.add("P1", "Ann", "boat")
    assert p.numbers() == []


def test_fact_amount_positive():
    c = _c()
    with pytest.raises(ValueError):
        c.file("P1", 0, D1, D1)
    assert c.of_policy("P1") == []


def test_fact_incident_first():
    c = _c()
    with pytest.raises(ValueError):
        c.file("P1", 900, D1 + dt.timedelta(days=1), D1)
    assert c.of_policy("P1") == []


def test_fact_numbers_order():
    p = Policies()
    p.add("P1", "Zoe", "car")
    p.add("P3", "Ann", "home")
    p.add("P2", "Ann", "car")
    assert p.numbers() == ["P2", "P3", "P1"]


def test_fact_summary_days():
    c = _c()
    i = c.file("P1", 900, D1, D1 + dt.timedelta(days=3))
    lines = [x.strip() for x in summary(c, i)]
    assert len(lines) == 3 and lines[2] == "days: 3"


def _rows(c, tmp_path):
    p = tmp_path / "c.csv"
    export_claims(c, str(p))
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


def test_fact_export_header(tmp_path):
    c = _c()
    c.file("P1", 900, D1, D1)
    rows = _rows(c, tmp_path)
    assert rows[0] == "id,number,payout" and rows[1].split(",")[0] == "1" and len(rows) == 2


def test_fact_export_order(tmp_path):
    c = _c()
    D2 = D1 + dt.timedelta(days=2)
    c.file("P1", 900, D1, D2)
    c.file("P1", 900, D1, D1)
    c.file("P1", 900, D1, D2)
    assert [x.split(",")[0] for x in _rows(c, tmp_path)[1:]] == ["2", "1", "3"]
