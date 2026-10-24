import pytest
from split import Trip
from settle import summary


def test_basic():
    t = Trip()
    t.add_expense("ann", 300, ["ann", "bob", "cy"])
    assert t.balance("ann") == 200 and t.balance("bob") == -100 and t.balance("zed") == 0
    assert t.people() == ["ann", "bob", "cy"] and t.total() == 300
    assert summary(t) == ["ann: 200", "bob: -100", "cy: -100"]
    t.undo()
    assert t.total() == 0 and t.balance("ann") == 0


def _odd():
    t = Trip()
    t.add_expense("ann", 100, ["ann", "bob", "cy"])
    return t


def test_fact_leftover_order():
    t = _odd()
    assert t.balance("ann") == 67 and t.balance("bob") == -33 and t.balance("cy") == -34


def test_stale_leftover_alpha():
    t = _odd()
    assert t.balance("ann") == 66 and t.balance("cy") == -33


def test_fact_hide_zero():
    t = Trip()
    t.add_expense("bob", 500, ["ann", "bob"])
    t.add_expense("cy", 300, ["cy", "dee"])
    t.add_expense("dee", 300, ["cy", "dee"])
    assert summary(t) == ["ann: -250", "bob: 250"]


def test_fact_amount_positive():
    t = Trip()
    for a in (0, -100, 2.5):
        with pytest.raises(ValueError):
            t.add_expense("ann", a, ["ann", "bob"])
    assert t.people() == [] and t.balance("ann") == 0


def test_fact_people_valid():
    t = Trip()
    for people in ([], ["ann", "ann"]):
        with pytest.raises(ValueError):
            t.add_expense("ann", 100, people)
    assert t.people() == []


def test_fact_undo_empty():
    t = Trip()
    with pytest.raises(IndexError):
        t.undo()
    t.add_expense("ann", 100, ["bob"])
    t.undo()
    with pytest.raises(IndexError):
        t.undo()
