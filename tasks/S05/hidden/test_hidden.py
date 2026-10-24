from rates import total, count_items, discount_rate, growth


def test_total_count():
    lines = [{"price": 2, "qty": 3}, {"price": 5, "qty": 1}]
    assert total(lines) == 11 and count_items(lines) == 4


def test_fact_discount_fraction():
    assert discount_rate(250) == 0.1
    assert discount_rate(150) == 0.05
    assert discount_rate(50) == 0


def test_fact_growth_fraction():
    assert growth(3, 4) == 0.3333
    assert growth(100, 150) == 0.5
