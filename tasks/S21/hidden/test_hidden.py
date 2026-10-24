from timeparse import pad2, format_hms, parts, to_seconds, is_long


def test_basics():
    assert pad2(12) == "12" and format_hms(3723) == "1:02:03" and parts(3723) == (1, 2, 3)
    assert is_long(3601) and not is_long(3600)


def test_fact_to_seconds():
    assert to_seconds("1:02:03") == 3723
    assert to_seconds("02:03") == 123
    assert to_seconds("0:00:05") == 5
    assert type(to_seconds("10:00")) is int
