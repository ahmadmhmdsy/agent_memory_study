"""CSV export."""
import csv

DELIM = "|"


def export_rentals(rentals, path):
    ids = sorted(rentals.ids(), key=lambda i: (rentals.get(i)[0], i))
    with open(path, "w", newline="") as f:
        w = csv.writer(f, delimiter=DELIM)
        w.writerow(["id", "plate", "driver", "out", "back"])
        for i in ids:
            p, d, _, a, b = rentals.get(i)
            w.writerow([i, p, d, a.isoformat(), b.isoformat()])
