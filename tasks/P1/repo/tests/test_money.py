from money import parse_amount, format_amount


def test_parse_plain():
    assert parse_amount("12.34") == 1234


def test_format():
    assert format_amount(1234) == "$12.34"
