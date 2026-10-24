from settings import load, get, get_int, get_bool, get_duration


def test_load_and_get():
    cfg = load("a = 1\n# c\nb=two")
    assert get(cfg, "a") == "1"
    assert get(cfg, "zz", 5) == 5


def test_quotes():
    cfg = load('n = "a b"\nm = \'x y\'')
    assert cfg["n"] == "a b" and cfg["m"] == "x y"


def test_get_int_bool():
    cfg = load("i = 42\nb1 = YES\nb2 = false\nb3 = 1")
    assert get_int(cfg, "i", 0) == 42
    assert get_int(cfg, "nope", 7) == 7
    assert get_bool(cfg, "b1", False) is True
    assert get_bool(cfg, "b2", True) is False
    assert get_bool(cfg, "b3", False) is True


def test_fact_duration_in_ms():
    cfg = load("a = 5s\nb = 250ms\nc = 2m\nd = 3\ne = 1h")
    expected = {"a": 5000, "b": 250, "c": 120000, "d": 3000, "e": 3600000}
    for key, ms in expected.items():
        r = get_duration(cfg, key)
        assert r == ms and type(r) is int, (key, r)
