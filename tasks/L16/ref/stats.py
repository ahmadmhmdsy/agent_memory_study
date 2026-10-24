from datetime import timedelta
from log import check_kind, check_minutes


def streak(log, today):
    days = set(log.days())
    n = gap = 0
    d = today
    while True:
        if d in days:
            n += 1
            gap = 0
        else:
            gap += 1
            if gap > 1 or n == 0:
                break
        d -= timedelta(days=1)
    return n


def week_total(log, day):
    start = day - timedelta(days=(day.weekday() + 1) % 7)
    return sum(m for i in range(7) for k, m, km in log.entries(start + timedelta(days=i)))


def calories(kind, minutes, km):
    k = check_kind(kind)
    check_minutes(minutes)
    return {"run": 70 * km, "bike": 30 * km, "swim": 10 * minutes}[k]
