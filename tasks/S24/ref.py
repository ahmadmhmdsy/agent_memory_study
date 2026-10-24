import re
from collections import Counter

STOP = {"the", "a", "an", "and", "of", "to", "in"}


def words(text):
    return re.findall(r"[a-z]+", text.lower())


def counts(text):
    return dict(Counter(words(text)))


def top_words(text, n):
    return [w for w, _ in sorted(counts(text).items(), key=lambda kv: (-kv[1], kv[0]))[:n]]


def rare_words(text, max_count=1):
    return sorted(w for w, c in counts(text).items() if c <= max_count and w not in STOP)


def unique_count(text):
    return len(counts(text))
