import pytest
from hotel import Hotel
from bill import bill


def test_basic():
    h = Hotel([101, 102])
    h.book(101, "ann", 5, 2)
    assert h.guest_in(101, 5) == "ann" and h.guest_in(101, 6) == "ann" and h.guest_in(101, 7) is None
    assert h.bookings("ann") == [(101, 5, 2)] and h.free_rooms(5) == [102]
    h.cancel(101, 5)
    assert h.free_rooms(5) == [101, 102] and h.guest_in(101, 5) is None


def _three():
    h = Hotel([101])
    h.book(101, "ann", 1, 3)
    return h


def test_fact_night_rate():
    assert bill(_three(), "ann") == 29700


def test_stale_rate_9000():
    assert bill(_three(), "ann") == 27000


def test_fact_seventh_free():
    h = Hotel([101, 102])
    h.book(101, "ann", 1, 7)
    assert bill(h, "ann") == 6 * 9900
    h.book(102, "ann", 1, 14)
    h.book(101, "bob", 20, 6)
    assert bill(h, "ann") == 18 * 9900 and bill(h, "bob") == 6 * 9900


def test_fact_no_overlap():
    h = Hotel([101, 102])
    h.book(101, "a", 5, 2)
    for first, n in ((6, 1), (4, 2)):
        with pytest.raises(ValueError):
            h.book(101, "b", first, n)
    h.book(101, "c", 7, 1)
    h.book(101, "d", 3, 2)
    h.book(102, "e", 5, 2)
    assert h.guest_in(101, 6) == "a" and h.bookings("b") == []


def test_fact_nights_range():
    h = Hotel([101, 102])
    for n in (0, 15, -1):
        with pytest.raises(ValueError):
            h.book(101, "ann", 1, n)
    h.book(101, "ann", 1, 14)
    h.book(102, "ann", 1, 1)
    assert h.bookings("ann") == [(101, 1, 14), (102, 1, 1)]


def test_fact_unknown_room():
    h = Hotel([101])
    with pytest.raises(KeyError):
        h.book(999, "ann", 1, 1)
    assert h.bookings("ann") == []
