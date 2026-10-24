from scores import clamp_score


def test_clamp():
    assert clamp_score(120) == 100
