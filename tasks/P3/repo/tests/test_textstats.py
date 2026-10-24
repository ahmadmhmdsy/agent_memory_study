from textstats import word_count, top_words


def test_word_count():
    assert word_count("One two, three!") == 3


def test_top_words():
    assert top_words("b a b c b a", 2) == ["b", "a"]
