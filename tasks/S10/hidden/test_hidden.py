from paging import clamp, count_pages, page


def test_clamp_count():
    assert clamp(-1, 0, 3) == 0
    assert count_pages(5, 2) == 3 and count_pages(4, 2) == 2 and count_pages(0, 3) == 0


def test_fact_zero_based_pages():
    items = [1, 2, 3, 4, 5]
    assert page(items, 0, 2) == [1, 2]
    assert page(items, 1, 2) == [3, 4]
    assert page(items, 2, 2) == [5]
    assert page(items, 3, 2) == []
