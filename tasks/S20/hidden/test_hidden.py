from inventory2 import Store


def make():
    s = Store()
    for n, q in [("pen", 2), ("cup", 5), ("bag", 1), ("ink", 9)]:
        s.add(n, q)
    return s


def test_basics():
    s = make()
    assert s.qty("pen") == 2 and s.qty("zzz") == 0
    assert s.names() == ["bag", "cup", "ink", "pen"] and s.total() == 17


def test_fact_low_stock():
    s = make()
    assert s.low_stock() == ["bag", "pen"]
    assert s.low_stock(6) == ["bag", "cup", "pen"]
