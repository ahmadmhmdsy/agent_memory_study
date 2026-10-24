from grades import clamp


def test_clamp():
    assert clamp(101) == 100
