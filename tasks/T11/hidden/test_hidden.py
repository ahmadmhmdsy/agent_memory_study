import pytest
from contacts import Contacts
from export import to_csv


def test_basic():
    c = Contacts()
    c.add("ann", "0501234567")
    c.add("bob", "0521112222")
    assert c.phone("ann") == "0501234567" and c.phone("zed") is None
    assert c.names() == ["ann", "bob"] and c.search("A") == ["ann"]
    c.remove("ann")
    assert c.count() == 1 and to_csv(c) == ["name,phone", "bob,0521112222"]


def test_fact_min_digits():
    c = Contacts()
    c.add("ann", "123456789")
    with pytest.raises(ValueError):
        c.add("bob", "12345678")
    assert c.phone("ann") == "123456789" and c.phone("bob") is None


def test_stale_digits_7():
    c = Contacts()
    c.add("bob", "12345678")
    assert c.phone("bob") == "12345678"


def test_fact_csv_quote():
    c = Contacts()
    c.add("Lee, Ann", "123456789")
    assert to_csv(c) == ["name,phone", '"Lee, Ann",123456789']


def test_fact_phone_digits():
    c = Contacts()
    c.add("ann", "050-123 4567")
    assert c.phone("ann") == "0501234567"


def test_fact_phone_chars():
    c = Contacts()
    for p in ("050.123.4567", "+972501234567", "05012x4567"):
        with pytest.raises(ValueError):
            c.add("ann", p)
    assert c.phone("ann") is None


def test_fact_add_replaces():
    c = Contacts()
    c.add("ann", "111111111")
    c.add("ann", "222222222")
    assert c.phone("ann") == "222222222" and c.names() == ["ann"]
