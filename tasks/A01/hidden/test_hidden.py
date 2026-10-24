import datetime as dt
import pytest
from stock import Stock, normalize_sku, needs_reorder
from orders import Orders
from pricing import price_line, order_total
from export import export_stock, export_orders
from report import top_skus

D = dt.date
A, B, C = "AA1", "BB2", "CC3"


def test_basic():
    s = Stock()
    s.add(A, 20)
    s.remove(A, 5)
    assert s.count(A) == 15 and s.count("ZZ9") == 0 and s.skus() == [A]
    o = Orders(s)
    oid = o.place(A, 3, D(2026, 1, 5))
    assert o.get(oid) == (A, 3, D(2026, 1, 5)) and s.count(A) == 12
    with pytest.raises(KeyError):
        o.get("nope")
    assert price_line(2, 150) == 300


def _reorder():
    s = Stock()
    s.add(A, 9)
    s.add(B, 7)
    s.add(C, 8)
    return needs_reorder(s)


def test_fact_reorder_level():
    assert _reorder() == [B]


def test_stale_reorder_10():
    assert _reorder() == [A, B, C]


def test_stale_reorder_5():
    assert _reorder() == []


def test_fact_bulk_discount():
    assert price_line(100, 100) == 9300 and price_line(99, 100) == 9900


def test_stale_bulk_10():
    assert price_line(100, 100) == 9000


def test_stale_bulk_5():
    assert price_line(100, 100) == 9500


def _day(tmp_path):
    s = Stock()
    s.add(A, 10)
    o = Orders(s)
    o.place(A, 2, D(2026, 1, 5))
    p = tmp_path / "o.csv"
    export_orders(o, str(p))
    rows = [x.rstrip("\r") for x in p.read_text().splitlines() if x.strip()]
    return rows[-1].split(",")[-1].strip()


def test_fact_date_format(tmp_path):
    assert _day(tmp_path) == "20260105"


def test_stale_date_iso(tmp_path):
    assert _day(tmp_path) == "2026-01-05"


def test_stale_date_dmy(tmp_path):
    assert _day(tmp_path) == "05/01/2026"


def _tax():
    return order_total(10, 100) - order_total(5, 100)


def test_fact_tax_rate():
    assert _tax() == 530


def test_stale_tax_8():
    assert _tax() == 540


def test_fact_shipping_fee():
    assert 2 * order_total(1, 5000) - order_total(2, 5000) == 300 and order_total(1, 5000) == 5600


def test_fact_max_stock():
    s = Stock()
    s.add(A, 1000)
    with pytest.raises(ValueError):
        s.add(A, 1)
    assert s.count(A) == 1000


def test_stale_max_500():
    s = Stock()
    with pytest.raises(ValueError):
        s.add(A, 600)


def test_fact_sku_strip():
    assert normalize_sku("ab-12 3") == "AB123"
    with pytest.raises(ValueError):
        normalize_sku("a!b")
    s = Stock()
    s.add("aa-1", 2)
    assert s.count("AA1") == 2


def test_fact_sku_case():
    s = Stock()
    s.add("aa1", 1)
    s.add("AA1", 2)
    assert s.count("Aa1") == 3 and s.skus() == [A]


def _stock_rows(tmp_path):
    s = Stock()
    s.add(B, 1)
    s.add(A, 2)
    p = tmp_path / "s.csv"
    export_stock(s, str(p))
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


def test_fact_export_header(tmp_path):
    assert _stock_rows(tmp_path)[0] == "sku,count"


def test_fact_export_sorted(tmp_path):
    assert _stock_rows(tmp_path)[1:] == ["AA1,2", "BB2,1"]


def test_fact_order_ids():
    s = Stock()
    s.add(A, 10)
    o = Orders(s)
    assert o.place(A, 1, D(2026, 1, 5)) == "O-0001" and o.place(A, 1, D(2026, 1, 5)) == "O-0002"


def test_fact_top_ties():
    s = Stock()
    for k in (A, B, C):
        s.add(k, 20)
    o = Orders(s)
    o.place(B, 5, D(2026, 1, 5))
    o.place(A, 5, D(2026, 1, 5))
    o.place(C, 7, D(2026, 1, 6))
    assert top_skus(o, 3) == [C, A, B] and top_skus(o, 1) == [C]


def test_fact_no_negative():
    s = Stock()
    s.add(A, 3)
    with pytest.raises(ValueError):
        s.remove(A, 4)
    with pytest.raises(ValueError):
        Orders(s).place(A, 4, D(2026, 1, 5))
    assert s.count(A) == 3


def test_fact_order_qty_positive():
    s = Stock()
    s.add(A, 3)
    o = Orders(s)
    for q in (0, -1):
        with pytest.raises(ValueError):
            o.place(A, q, D(2026, 1, 5))
    assert s.count(A) == 3


def test_fact_cancel_restock():
    s = Stock()
    s.add(A, 10)
    o = Orders(s)
    oid = o.place(A, 4, D(2026, 1, 5))
    o.cancel(oid)
    assert s.count(A) == 10
    with pytest.raises(KeyError):
        o.get(oid)
