"""CSV export."""
import csv

from pricing import charge


def export_trips(trips, path):
    ids = sorted(trips.finished(), key=lambda k: (trips.get(k)["rider"], k))
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "rider", "minutes", "charge"])
        for k in ids:
            w.writerow([k, trips.get(k)["rider"], trips.minutes(k), charge(trips, k)])
