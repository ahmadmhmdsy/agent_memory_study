from paging import clamp


def test_clamp():
    assert clamp(5, 0, 3) == 3
