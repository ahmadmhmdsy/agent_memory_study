from ranking import mean, median, unique_scores


def test_mean_median():
    assert mean([2, 4]) == 3
    assert median([5, 1, 3]) == 3
    assert median([1, 2, 3, 4]) == 2.5


def test_fact_unique_descending():
    assert unique_scores([2, 9, 5, 9, 2]) == [9, 5, 2]
    assert unique_scores([1, 3, 2]) == [3, 2, 1]
