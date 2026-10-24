import pytest
from menu import Menu
from tabs import Tabs
from bills import subtotal, total, format_money, split, receipt
from export import export_tabs


def _t():
    m = Menu()
    m.add("Soup", 500)
    m.add("Tea", 200)
    m.add("Steak", 2500)
    return Tabs(m)


def test_basic():
    t = _t()
    assert t.menu.price("Tea") == 200
    with pytest.raises(KeyError):
        t.menu.price("Cake")
    i = t.open(3, 2)
    t.order(i, "Soup", 2)
    t.order(i, "Tea", 1)
    assert i == 1 and t.lines(i) == [("Soup", 2), ("Tea", 1)] and subtotal(t, i) == 1200 and t.is_open(i)


def _total(guests, staff=False):
    t = _t()
    i = t.open(1, guests, staff)
    t.order(i, "Steak", 4)
    return total(t, i)


def test_fact_service_pct():
    assert _total(8) == 11500


def test_stale_service_12():
    assert _total(8) == 11200


def test_stale_service_10():
    assert _total(8) == 11000


def test_fact_party_min():
    assert _total(5) > 10000 and _total(4) == 10000


def test_stale_party_8():
    assert _total(7) == 10000


def test_stale_party_6():
    assert _total(5) == 10000


def test_fact_staff_pct():
    assert _total(2, True) == 6000


def test_stale_staff_30():
    assert _total(2, True) == 7000


def test_stale_staff_50():
    assert _total(2, True) == 5000


def test_fact_service_after_discount():
    a = _total(2, True)
    b = _total(8) - 10000
    assert _total(8, True) == a + round(a * b / 10000)


def test_fact_money_format():
    assert format_money(1250) == "12.50 USD"


def test_stale_money_dollar():
    assert format_money(1250) == "$12.50"


def test_stale_money_plain():
    assert format_money(1250) == "12.50"


def _lines_ok(n):
    t = _t()
    i = t.open(1, 2)
    for _ in range(n - 1):
        t.order(i, "Tea", 1)
    try:
        t.order(i, "Tea", 1)
        return True
    except ValueError:
        assert len(t.lines(i)) == n - 1
        return False


def test_fact_max_lines():
    assert _lines_ok(40) and not _lines_ok(41)


def test_stale_lines_30():
    assert not _lines_ok(31)


def test_fact_menu_sorted():
    m = Menu()
    m.add("Tea", 200)
    m.add("Steak", 2500)
    m.add("Juice", 200)
    m.add("Soup", 500)
    assert m.items() == ["Juice", "Tea", "Soup", "Steak"]


def test_fact_split_fair():
    assert split(1000, 3) == [334, 333, 333] and split(1001, 4) == [251, 250, 250, 250]


def test_fact_receipt_merge():
    t = _t()
    i = t.open(1, 2)
    t.order(i, "Soup", 2)
    t.order(i, "Tea", 1)
    t.order(i, "Soup", 1)
    r = [x.strip() for x in receipt(t, i)]
    assert len(r) == 2 and r[0] == "3 x Soup"


def test_fact_qty_positive():
    t = _t()
    i = t.open(1, 2)
    for q in (0, -1):
        with pytest.raises(ValueError):
            t.order(i, "Tea", q)
    assert t.lines(i) == []


def test_fact_unknown_dish():
    t = _t()
    i = t.open(1, 2)
    with pytest.raises(KeyError):
        t.order(i, "Cake", 1)
    assert t.lines(i) == []


def test_fact_closed_tab():
    t = _t()
    i = t.open(1, 2)
    t.order(i, "Tea", 1)
    t.close(i)
    with pytest.raises(ValueError):
        t.order(i, "Tea", 1)
    assert not t.is_open(i) and t.lines(i) == [("Tea", 1)]


def test_fact_export_header(tmp_path):
    t = _t()
    t.open(1, 2)
    p = tmp_path / "t.csv"
    export_tabs(t, str(p))
    rows = [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]
    assert rows[0] == "id,table,guests,total" and rows[1].split(",")[0] == "1"
