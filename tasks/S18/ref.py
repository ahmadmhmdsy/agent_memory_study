def shout(s):
    return s.upper() + "!"


def capitalize_words(s):
    return " ".join(w[:1].upper() + w[1:] for w in s.split())


def reverse_words(s):
    return " ".join(reversed(s.split()))


def truncate(s, n):
    return s if len(s) <= n else s[:n - 1] + "\u2026"


def count_vowels(s):
    return sum(ch in "aeiou" for ch in s.lower())
