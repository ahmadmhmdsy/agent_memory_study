from stack import Stack


def test_push():
    s = Stack()
    s.push(1)
    assert s.items == [1]
