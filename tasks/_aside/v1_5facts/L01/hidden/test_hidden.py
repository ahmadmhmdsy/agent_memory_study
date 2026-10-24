import pytest
from money import invoice_total
from store import Store
from report import low_stock
from io_csv import export_stock


def test_store_basic():
    s = Store()
    s.add("A", 5)
    s.add("A", 2)
    s.remove("A", 3)
    assert s.qty("A") == 4 and s.qty("Z") == 0


def test_fact_half_up():
    assert invoice_total([(5, 2)], 0.25) == 13
    assert invoice_total([(25, 2)], 0.25) == 63
    assert invoice_total([(250, 1)], 0.05) == 263
    assert isinstance(invoice_total([(100, 1)], 0.1), int)


def _lines(tmp_path):
    s = Store()
    s.add("B", 5)
    s.add("A", 2)
    p = tmp_path / "s.csv"
    export_stock(s, str(p))
    return [l.rstrip("\r") for l in p.read_text().splitlines() if l.strip()]


def test_fact_tab_csv(tmp_path):
    assert _lines(tmp_path) == ["sku\tqty", "A\t2", "B\t5"]


def test_stale_semicolon_csv(tmp_path):
    assert _lines(tmp_path)[0] == "sku;qty"


def test_fact_zero_removed():
    s = Store()
    s.add("A", 2)
    s.add("B", 1)
    s.remove("A", 2)
    assert s.skus() == ["B"] and s.qty("A") == 0


def test_fact_overdraw():
    s = Store()
    s.add("A", 2)
    with pytest.raises(ValueError):
        s.remove("A", 3)
    assert s.qty("A") == 2


def test_fact_low_stock_sorted():
    s = Store()
    s.add("b", 1)
    s.add("d", 3)
    s.add("c", 2)
    s.add("a", 3)
    s.add("e", 9)
    assert low_stock(s, 5) == ["b", "c", "a", "d"]
