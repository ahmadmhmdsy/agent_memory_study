"""Times and CSV export."""
import csv


def fmt_time(minutes):
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def export_programme(talks, path):
    ids = sorted(talks.ids(), key=lambda k: (talks.get(k)[3], talks.get(k)[2]))
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["start", "room", "title"])
        for k in ids:
            title, _, room, start, _ = talks.get(k)
            w.writerow([fmt_time(start), room, title])
