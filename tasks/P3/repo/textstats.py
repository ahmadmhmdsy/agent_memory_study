"""Text statistics."""
import re
from collections import Counter


def words(text):
    return re.findall(r"[a-z']+", text.lower())


def word_count(text):
    return len(words(text))


def top_words(text, n=3):
    return [w for w, _ in Counter(words(text)).most_common(n)]
