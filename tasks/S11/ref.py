import re


def word_count(text):
    return len(text.split())


def clean(text):
    return re.sub(r"[^a-z0-9 ]", "", text.lower())


def slugify(title):
    return "_".join(clean(title).split())
