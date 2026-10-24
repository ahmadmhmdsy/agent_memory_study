from bank import Account


def test_new():
    assert Account().balance == 0
