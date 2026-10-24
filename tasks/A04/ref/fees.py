"""Fees and bills."""
from collections import Counter

FEES = {"checkup": 5000, "filling": 12500, "cleaning": 8000}
NO_SHOW = 2500
KID_UNDER = 14


def fee(schedule, aid):
    pid, _, _, kind = schedule.get(aid)
    st = schedule.status(aid)
    if st == "missed":
        return NO_SHOW
    if st == "open":
        return 0
    f = FEES[kind]
    if schedule.patients.age(pid) < KID_UNDER:
        f = round(f / 2)
    return f


def bill(schedule, pid):
    return sum(fee(schedule, a) for a in schedule.of_patient(pid))


def revenue(schedule, day):
    return sum(fee(schedule, a) for a in schedule.day(day))


def busiest_day(schedule):
    c = Counter(schedule.get(a)[1] for a in schedule.ids())
    return min(c, key=lambda d: (-c[d], d)) if c else None
