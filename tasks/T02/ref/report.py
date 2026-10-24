"""Hours report."""


def report(ts):
    rows = sorted(((-ts.hours(p), p) for p in ts.people()))
    return [f"{p}: {-h}" for h, p in rows]
