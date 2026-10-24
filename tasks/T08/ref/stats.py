"""Grade statistics."""

PASS = 60


def average(gb, student):
    s = gb.scores(student)
    if not s:
        return None
    if len(s) >= 3:
        s = sorted(s)[1:]
    return (2 * sum(s) + len(s)) // (2 * len(s))


def passed(gb, student):
    a = average(gb, student)
    return a is not None and a >= PASS
