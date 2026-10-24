from datetime import timedelta


def parse_tags(s):
    out = []
    for t in s.split(","):
        t = t.strip().lower()
        if t and t not in out:
            out.append(t)
    return out


def days_left(due, today):
    n = 0
    d = today
    while d < due:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return n
