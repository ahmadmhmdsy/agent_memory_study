"""Labels and CSV export."""
import csv

from schedule import next_water


def label(plants, name):
    return f"{name} ({plants.kind(name).upper()})"


def export_plan(care, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["plant", "kind", "next"])
        for n in sorted(care.plants.names()):
            w.writerow([n, care.plants.kind(n), next_water(care, n).isoformat()])
