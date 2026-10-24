from parsing import strip_all


def test_strip_all():
    assert strip_all([" a ", "b "]) == ["a", "b"]
