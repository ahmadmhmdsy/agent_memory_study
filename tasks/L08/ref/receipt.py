from rates import fee


def fmt_duration(minutes):
    d, rest = divmod(minutes, 1440)
    h, m = divmod(rest, 60)
    return f"{d}d {h:02d}h {m:02d}m" if d else f"{h}h {m:02d}m"


def write_receipt(plate, minutes, path):
    c = fee(minutes)
    with open(path, "w", encoding="utf8") as f:
        f.write(f"Plate: {plate}\n")
        f.write(f"Time: {fmt_duration(minutes)}\n")
        f.write(f"Total: ${c // 100}.{c % 100:02d}\n")
