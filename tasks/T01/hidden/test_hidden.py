import pytest
from cart import Cart
from price import total


def test_cart_basic():
    c = Cart()
    c.add("A1", 2)
    c.add("B2", 1)
    assert c.count("A1") == 2 and c.count("Z9") == 0 and c.size() == 3
    assert c.items() == [("A1", 2), ("B2", 1)]
    c.remove("A1", 1)
    assert c.count("A1") == 1
    c.clear()
    assert c.items() == [] and c.size() == 0


def _one():
    c = Cart()
    c.add("A1", 1)
    return total(c, {"A1": 1000})


def test_fact_vat_rate():
    assert _one() == 1150


def test_stale_vat_20():
    assert _one() == 1200


def test_fact_bulk_discount():
    c = Cart()
    c.add("A1", 10)
    assert total(c, {"A1": 1000}) == 10925
    c.remove("A1", 1)
    assert total(c, {"A1": 1000}) == 10350


def test_fact_sku_case():
    c = Cart()
    c.add("ab1", 1)
    c.add("AB1", 2)
    assert c.count("Ab1") == 3 and c.items() == [("AB1", 3)]


def test_fact_qty_positive():
    c = Cart()
    for q in (0, -1):
        with pytest.raises(ValueError):
            c.add("A1", q)
    assert c.items() == []


def test_fact_remove_over():
    c = Cart()
    c.add("A1", 2)
    c.add("B2", 1)
    c.remove("A1", 5)
    assert c.count("A1") == 0 and c.items() == [("B2", 1)]
