"""Trip charges."""

UNLOCK = 120
RATE = 18
EBIKE = 6
MEMBER_FREE = 20
OVER_AFTER = 180
OVER_FEE = 500


def charge(trips, tid):
    v = trips.get(tid)
    m = trips.minutes(tid)
    paid = max(0, m - MEMBER_FREE) if v["member"] else m
    c = UNLOCK + paid * RATE
    if v["ebike"]:
        c += m * EBIKE
    if m > OVER_AFTER:
        c += OVER_FEE
    return c


def format_duration(minutes):
    if minutes >= 60:
        return f"{minutes // 60}h {minutes % 60}m"
    return f"{minutes} min"


def revenue(trips):
    return sum(charge(trips, k) for k in trips.finished())
