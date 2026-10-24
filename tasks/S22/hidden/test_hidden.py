from urltools import scheme, host, path, query_params, is_secure


def test_basics():
    u = "HTTPS://example.com/a/b?x=1"
    assert scheme(u) == "https" and host(u) == "example.com" and path(u) == "/a/b"
    assert path("http://e.com") == "/" and is_secure(u) and not is_secure("http://e.com")


def test_fact_query_params():
    assert query_params("http://e.com/p?a=1&b=x&a=2") == {"a": "2", "b": "x"}
    assert query_params("http://e.com/p") == {}
