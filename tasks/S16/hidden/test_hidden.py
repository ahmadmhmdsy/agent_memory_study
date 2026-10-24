from scores import clamp_score, best, average


def test_clamp_best():
    assert clamp_score(-3) == 0 and best([3, 9, 4]) == 9


def test_fact_truncated_average():
    r = average([1, 2])
    assert r == 1 and type(r) is int
    assert average([2, 3, 3]) == 2
    assert average([99, 100]) == 99
    assert type(average([4, 6])) is int
