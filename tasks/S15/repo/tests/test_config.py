from config import parse_bool


def test_parse_bool():
    assert parse_bool("yes") is True
