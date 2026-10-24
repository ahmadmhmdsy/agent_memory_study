import pytest
from classes import Schedule
from billing import bill


def test_basic():
    s = Schedule()
    s.add_class("yoga", 2)
    s.add_class("spin", 5)
    assert s.book("yoga", "ann") is True and s.book("spin", "ann") is True
    assert s.booked("yoga") == ["ann"] and s.waitlist("yoga") == []
    assert s.classes() == ["spin", "yoga"] and s.busy("ann") == ["spin", "yoga"]
    s.cancel("spin", "ann")
    assert s.busy("ann") == ["yoga"] and s.booked("spin") == []


def _two():
    s = Schedule()
    s.add_class("yoga", 5)
    s.add_class("spin", 5)
    s.book("yoga", "ann")
    s.book("spin", "ann")
    return s


def test_fact_class_price():
    assert bill(_two(), "ann") == 1900


def test_stale_price_800():
    assert bill(_two(), "ann") == 1600


def test_fact_waitlist_promote():
    s = Schedule()
    s.add_class("yoga", 1)
    s.book("yoga", "ann")
    s.book("yoga", "bob")
    s.book("yoga", "cy")
    s.cancel("yoga", "ann")
    assert s.booked("yoga") == ["bob"] and s.waitlist("yoga") == ["cy"]


def test_fact_no_double_book():
    s = Schedule()
    s.add_class("yoga", 1)
    s.book("yoga", "ann")
    s.book("yoga", "bob")
    for m in ("ann", "bob"):
        with pytest.raises(ValueError):
            s.book("yoga", m)
    assert s.booked("yoga") == ["ann"] and s.waitlist("yoga") == ["bob"]


def test_fact_capacity_range():
    s = Schedule()
    for name, cap in (("a", 0), ("b", 31), ("c", -1)):
        with pytest.raises(ValueError):
            s.add_class(name, cap)
    s.add_class("d", 30)
    s.add_class("e", 1)
    assert s.classes() == ["d", "e"]


def test_fact_full_waitlist():
    s = Schedule()
    s.add_class("yoga", 2)
    assert [s.book("yoga", m) for m in ("ann", "bob", "cy", "dee")] == [True, True, False, False]
    assert s.booked("yoga") == ["ann", "bob"] and s.waitlist("yoga") == ["cy", "dee"]
