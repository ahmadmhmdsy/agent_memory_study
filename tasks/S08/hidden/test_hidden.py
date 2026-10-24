from temps import is_freezing, count_above, average


def test_freezing_count():
    assert is_freezing(0) and not is_freezing(0.5)
    assert count_above([1, 5, 9], 4) == 2


def test_fact_average_kelvin():
    assert average([0, 10]) == 278.15
    assert average([20.5]) == 293.65
