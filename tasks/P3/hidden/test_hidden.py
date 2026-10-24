from textstats import word_count, top_words, unique_words, char_count, sentence_count, summary
import textstats


def test_unique_and_chars():
    assert unique_words("A a b") == 2
    assert char_count("a b") == 3
    assert char_count("a b\tc", spaces=False) == 3


def test_stopwords():
    assert "the" in textstats.STOPWORDS
    assert top_words("the cat the cat the dog", 2) == ["cat", "dog"]


def test_sentence_count():
    assert sentence_count("Hi. How are you?! Fine") == 3
    assert sentence_count("One.") == 1


def test_summary():
    s = summary("The cat sat. The cat ran!")
    assert s["words"] == 6 and s["sentences"] == 2 and s["top"][0] == "cat"


def test_fact_reading_time():
    from textstats import reading_time
    assert reading_time("word " * 450) == 3
    assert reading_time("word " * 200) == 1
    assert reading_time("word " * 201) == 2
    assert reading_time("") == 0
    assert reading_time("word " * 250, wpm=100) == 3
