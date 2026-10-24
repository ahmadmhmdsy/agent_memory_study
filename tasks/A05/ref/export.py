"""CSV export."""
import csv

from bills import total


def export_tabs(tabs, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "table", "guests", "total"])
        for i in tabs.ids():
            w.writerow([i, tabs.table(i), tabs.guests(i), total(tabs, i)])
