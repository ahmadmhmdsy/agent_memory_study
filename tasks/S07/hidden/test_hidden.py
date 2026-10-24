from users import is_valid_email, domain, Users


def test_email_domain():
    assert is_valid_email("x@y.org") and not is_valid_email("x@@y.org") and not is_valid_email("xy.org")
    assert domain("a@Ex.COM") == "ex.com"


def test_fact_username_storage():
    u = Users()
    u.add("Ann Lee")
    u.add(" Bo  Diaz ")
    assert u.names() == ["ann.lee", "bo.diaz"]
