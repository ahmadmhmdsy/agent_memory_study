from wordfreq import words, counts, top_words, rare_words, unique_count

TEXT = "the cat and the dog and a cat bird"


def test_basics():
    assert counts("b a b") == {"b": 2, "a": 1}
    assert top_words("b a b c c", 2) == ["b", "c"]
    assert unique_count(TEXT) == 6


def test_fact_rare_words():
    assert rare_words(TEXT) == ["bird", "dog"]
    assert rare_words(TEXT, 2) == ["bird", "cat", "dog"]
