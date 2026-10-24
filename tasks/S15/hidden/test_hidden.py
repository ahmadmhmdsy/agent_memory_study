from config import parse_bool, load, get


def test_bool_load():
    assert parse_bool(" ON ") is True and parse_bool("no") is False
    assert load("a = 1\n# c\n\nb=two") == {"a": "1", "b": "two"}


def test_get_default():
    assert get(load("a=1"), "zzz", "d") == "d"


def test_fact_case_insensitive_get():
    cfg = load("Port = 8080\nhost=x")
    assert get(cfg, "PORT") == "8080"
    assert get(cfg, "port") == "8080"
    assert get(cfg, "HOST") == "x"
