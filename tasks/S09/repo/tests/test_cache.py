from cache import Cache


def test_put_get():
    c = Cache()
    c.put("a", 1)
    assert c.get("a") == 1
