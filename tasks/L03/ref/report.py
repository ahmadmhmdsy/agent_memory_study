def bar(n):
    return "#" * n


def format_row(name, avg):
    if len(name) > 20:
        name = name[:17] + "..."
    return f"{name:<20}{avg:>6.1f}"


def letter(avg):
    if avg is None:
        return "-"
    for cut, g in ((90, "A"), (80, "B"), (70, "C"), (60, "D")):
        if avg >= cut:
            return g
    return "F"


def pct(part, whole):
    return round(100 * part / whole, 1)
