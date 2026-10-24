def is_blank(s):
    return not s.strip()


def plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def parse_tags(s):
    out = []
    for t in s.split(","):
        t = t.strip().lower()
        if t and t not in out:
            out.append(t)
    return out


def join_tags(tags):
    return ", ".join(tags)
