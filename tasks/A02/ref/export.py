"""CSV export."""
import csv


def export_bookings(bookings, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "room", "guest", "in", "out"])
        for i in bookings.ids():
            r, g, a, b = bookings.get(i)
            w.writerow([i, r, g, a.isoformat(), b.isoformat()])
