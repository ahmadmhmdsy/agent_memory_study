def bar(n):
    return "#" * n


def format_row(name, avg):
    if len(name) > 20:
        name = name[:17] + "..."
    return f"{name:<20}{avg:>6.1f}"
