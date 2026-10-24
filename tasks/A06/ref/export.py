"""CSV export."""
import csv

from meters import _num


def export_readings(readings, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["meter", "day", "kwh"])
        for m in sorted(readings.meters.ids(), key=_num):
            for d, v in sorted(readings.history(m)):
                w.writerow([m, d.isoformat(), v])
