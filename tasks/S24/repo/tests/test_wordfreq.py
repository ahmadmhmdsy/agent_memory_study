from wordfreq import words


def test_words():
    assert words("Hi, hi!") == ["hi", "hi"]
