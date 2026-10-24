def fmt_hours(minutes):
    h, m = divmod(minutes, 60)
    return f"{m}m" if h == 0 else f"{h}:{m:02d}"


def write_report(sheet, path):
    ws = sorted(sheet.workers(), key=lambda w: (-sheet.minutes(w), w))
    with open(path, "w", encoding="utf8") as f:
        for w in ws:
            f.write(f"{w}: {round(sheet.minutes(w) / 60, 2):g} h\n")
