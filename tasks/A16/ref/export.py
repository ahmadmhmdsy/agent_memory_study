"""Member cards and CSV export."""
import csv

from points import is_gold


def card(purchases, name):
    m = purchases.members
    return [f"member: {name}", f"points: {m.points(name)}",
            "tier: gold" if is_gold(purchases, name) else "tier: basic"]


def export_members(purchases, path):
    m = purchases.members
    names = sorted(m.names(), key=lambda n: (-m.points(n), n))
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "points"])
        for n in names:
            w.writerow([n, m.points(n)])
