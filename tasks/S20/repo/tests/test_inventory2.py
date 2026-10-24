from inventory2 import Store


def test_add():
    s = Store()
    s.add("pen", 2)
    assert s.stock == {"pen": 2}
