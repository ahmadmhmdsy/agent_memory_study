import pytest
from todo import TodoList
from view import summary


def test_basic():
    t = TodoList()
    assert t.add("milk", 2) == 1 and t.add("bread", 2) == 2
    t.done(1)
    assert t.open_items() == ["bread"] and t.done_items() == ["milk"]
    assert summary(t) == "1 open, 1 done"
    t.rename(2, "rye")
    assert t.open_items() == ["rye"]
    t.remove(1)
    assert t.done_items() == [] and t.open_items() == ["rye"]


def _four():
    t = TodoList()
    for title, p in (("a", 1), ("b", 3), ("c", 2), ("d", 3)):
        t.add(title, p)
    return t


def test_fact_urgent_order():
    assert _four().by_priority() == ["b", "d", "c", "a"]


def test_stale_urgent_1():
    assert _four().by_priority() == ["a", "c", "b", "d"]


def test_fact_all_done():
    t = TodoList()
    assert summary(t) == "all done"
    t.add("x", 1)
    t.done(1)
    assert summary(t) == "all done"
    t.add("y", 2)
    t.add("z", 2)
    assert summary(t) == "2 open, 1 done"


def test_fact_priority_range():
    t = TodoList()
    for p in (0, 4, -1):
        with pytest.raises(ValueError):
            t.add("x", p)
    assert t.open_items() == []


def test_fact_title_nonempty():
    t = TodoList()
    for title in ("", "   "):
        with pytest.raises(ValueError):
            t.add(title, 1)
    assert t.open_items() == []


def test_fact_done_unknown():
    t = TodoList()
    with pytest.raises(KeyError):
        t.done(5)
    t.add("x", 1)
    with pytest.raises(KeyError):
        t.done(2)
    assert t.open_items() == ["x"]
