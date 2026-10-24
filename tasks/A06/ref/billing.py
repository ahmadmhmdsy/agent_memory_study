"""Bills."""

RATE1 = 16
BLOCK = 400
RATE2 = 22
STANDING = 1000
LATE = 6


def cost(kwh):
    return min(kwh, BLOCK) * RATE1 + max(0, kwh - BLOCK) * RATE2


def bill(readings, mid, start, end):
    b = cost(readings.usage(mid, start, end))
    if not readings.meters.is_social(mid):
        b += STANDING
    return b


def late_total(readings, mid, start, end):
    b = bill(readings, mid, start, end)
    return b + round(b * LATE / 100)


def statement(readings, mid, start, end):
    return [f"from: {start.isoformat()}", f"to: {end.isoformat()}",
            f"kWh: {readings.usage(mid, start, end)}", f"bill: {bill(readings, mid, start, end)}"]


def average_daily(readings, mid, start, end):
    return readings.usage(mid, start, end) // (end - start).days


def total_bills(readings, start, end):
    out = 0
    for m in readings.meters.ids():
        days = readings.days(m)
        if start in days and end in days:
            out += bill(readings, m, start, end)
    return out
