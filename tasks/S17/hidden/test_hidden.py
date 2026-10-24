import pytest
from stack import Stack


def test_basics():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()
    s.push(1)
    s.push(2)
    assert len(s) == 2 and s.pop() == 2 and not s.is_empty()
    s.clear()
    assert s.is_empty() and s.to_list() == []


def test_fact_peek():
    s = Stack()
    assert s.peek() is None
    s.push(1)
    s.push(2)
    assert s.peek() == 2 and len(s) == 2
