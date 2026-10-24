from slug import word_count, clean, slugify


def test_count_clean():
    assert word_count(" x y ") == 2
    assert clean("Hi, You!") == "hi you"


def test_fact_underscore_slug():
    assert slugify("Hello World") == "hello_world"
    assert slugify("  Hi, there   friend! ") == "hi_there_friend"
