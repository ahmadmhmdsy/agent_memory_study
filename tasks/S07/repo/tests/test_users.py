from users import is_valid_email


def test_email():
    assert is_valid_email("a@b.com")
