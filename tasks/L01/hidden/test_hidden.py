import re
import pytest
from money import fmt_cents, invoice_total, parse_cents
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
    assert _lines(tmp_path)[1:3] == ["A\t2", "B\t5"]


def test_stale_semicolon_csv(tmp_path):
    assert _lines(tmp_path)[1] == "A;2"


def test_fact_header_upper(tmp_path):
    assert re.split(r"[\t;,]", _lines(tmp_path)[0]) == ["SKU", "QTY"]


def test_stale_header_lower(tmp_path):
    assert re.split(r"[\t;,]", _lines(tmp_path)[0]) == ["sku", "qty"]


def test_fact_fmt_sep():
    assert fmt_cents(123450) == "1,234.50" and fmt_cents(100000000) == "1,000,000.00"
    assert fmt_cents(5) == "0.05" and fmt_cents(99999) == "999.99"


def test_fact_qty_positive():
    s = Store()
    s.add("A", 5)
    for bad in (0, -1, 1.5):
        with pytest.raises(ValueError):
            s.remove("A", bad)
    assert s.qty("A") == 5


def test_fact_csv_footer(tmp_path):
    assert re.split(r"[\t;,]", _lines(tmp_path)[-1]) == ["total", "7"]


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


def test_fact_parse_dollar():
    assert parse_cents("$1,234.50") == 123450
    assert parse_cents("2.5") == 250


def test_fact_bulk():
    assert invoice_total([(100, 10)], 0) == 900
    assert invoice_total([(100, 9)], 0) == 900


def test_stale_bulk_5pct():
    assert invoice_total([(100, 10)], 0) == 950


def test_fact_rate_range():
    for bad in (1.5, -0.1):
        with pytest.raises(ValueError):
            invoice_total([(100, 1)], bad)
    assert invoice_total([(100, 1)], 1) == 200
