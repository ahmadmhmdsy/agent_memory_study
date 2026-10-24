from settings import load


def test_load_basic():
    assert load("a = 1\n# c\n\nb=two") == {"a": "1", "b": "two"}
