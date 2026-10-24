from money import parse_amount, format_amount, split, apply_discount, add_tax


def test_parse_variants():
    assert parse_amount("12.34") == 1234
    assert parse_amount("$12.34") == 1234
    assert parse_amount("7") == 700


def test_format_variants():
    assert format_amount(1234) == "$12.34"
    assert format_amount(5) == "$0.05"


def test_split():
    assert split(1000, 3) == [334, 333, 333]
    assert split(10, 4) == [3, 3, 2, 2]
    assert sum(split(12345, 7)) == 12345


def test_discount_plain():
    assert apply_discount(1000, 10) == 900
    assert apply_discount(2000, 25) == 1500


def test_tax_plain():
    assert add_tax(1000, 10) == 1100


def test_fact_discount_half_up_int():
    # 1005 less 10% is 904.5 cents: half-up gives 905 (banker's rounding gives 904).
    r = apply_discount(1005, 10)
    assert r == 905 and type(r) is int
    r = apply_discount(25, 10)  # 22.5
    assert r == 23 and type(r) is int


def test_fact_tax_half_up_int():
    r = add_tax(1050, 5)  # 1102.5
    assert r == 1103 and type(r) is int
    r = add_tax(10, 25)  # 12.5
    assert r == 13 and type(r) is int
