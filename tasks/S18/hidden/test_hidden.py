from strings import shout, capitalize_words, reverse_words, truncate, count_vowels


def test_basics():
    assert shout("a") == "A!"
    assert capitalize_words("hello big world") == "Hello Big World"
    assert reverse_words("a b c") == "c b a"
    assert count_vowels("AbE") == 2


def test_fact_truncate():
    assert truncate("abcdef", 4) == "abc\u2026"
    assert len(truncate("hello world", 5)) == 5
    assert truncate("abc", 4) == "abc"
    assert truncate("abcd", 4) == "abcd"
