def is_blank(s):
    return not s.strip()


def plural(n, word):
    if n == 1:
        return f"{n} {word}"
    if len(word) > 1 and word.endswith("y") and word[-2] not in "aeiou":
        return f"{n} {word[:-1]}ies"
    return f"{n} {word}s"


def parse_tags(s):
    out = []
    for t in s.split(","):
        t = t.strip().lower()
        if t and t not in out:
            out.append(t)
    return out


def join_tags(tags):
    return ", ".join(tags)
