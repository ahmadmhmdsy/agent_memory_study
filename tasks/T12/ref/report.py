"""Fuel report."""


def consumption(log):
    f = log.fills()
    if len(f) < 2:
        return None
    return round(sum(l for _, l in f[1:]) / (f[-1][0] - f[0][0]) * 100, 1)


def report(log):
    lines = [f"{o}: {l}" for o, l in log.fills()]
    c = consumption(log)
    if c is not None:
        lines.append(f"average: {c}")
    return lines
