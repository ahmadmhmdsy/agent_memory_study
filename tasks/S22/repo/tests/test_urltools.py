from urltools import scheme


def test_scheme():
    assert scheme("https://a.com/x") == "https"
