import pytest
from seats import Venue
from tickets import price, total


def test_basic():
    v = Venue(2, 3)
    v.reserve("A1", "ann")
    v.reserve("B2", "bob")
    assert v.holder("A1") == "ann" and v.holder("A2") is None and v.free_count() == 4
    assert v.seats_of("ann") == ["A1"] and v.taken() == ["A1", "B2"]
    v.release("A1")
    assert v.taken() == ["B2"] and price("B1") == 2500 and total(v, "bob") == 2500


def test_fact_row_a_price():
    v = Venue(2, 3)
    v.reserve("A1", "ann")
    v.reserve("A2", "ann")
    assert price("A2") == 4500 and price("B1") == 2500 and total(v, "ann") == 9000


def test_stale_row_a_4000():
    assert price("A2") == 4000


def test_fact_four_off():
    v = Venue(2, 3)
    for s in ("B1", "B2", "B3"):
        v.reserve(s, "ann")
    assert total(v, "ann") == 7500
    v.reserve("A1", "ann")
    assert total(v, "ann") == 10800


def test_fact_no_double_seat():
    v = Venue(2, 3)
    v.reserve("A1", "ann")
    with pytest.raises(ValueError):
        v.reserve("A1", "bob")
    assert v.holder("A1") == "ann" and v.seats_of("bob") == []


def test_fact_seat_exists():
    v = Venue(2, 3)
    for s in ("Z1", "A9"):
        with pytest.raises(KeyError):
            v.reserve(s, "ann")
    with pytest.raises(KeyError):
        v.holder("C1")
    assert v.free_count() == 6


def test_fact_release_free():
    v = Venue(2, 3)
    v.release("A1")
    v.reserve("A1", "ann")
    v.release("A1")
    v.release("A1")
    assert v.holder("A1") is None and v.free_count() == 6
