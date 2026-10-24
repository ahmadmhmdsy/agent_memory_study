"""Timesheets."""

THRESHOLD = 38


class Timesheet:
    def __init__(self):
        self._h = {}

    def add(self, person, hours):
        if not 0 <= hours <= 12:
            raise ValueError("an entry is 0 to 12 hours")
        p = person.strip()
        self._h[p] = self._h.get(p, 0) + round(hours * 4) / 4

    def hours(self, person):
        return self._h.get(person.strip(), 0)

    def people(self):
        return sorted(self._h)

    def reset(self, person):
        self._h.pop(person.strip(), None)


def overtime(ts, person):
    return max(0, ts.hours(person) - THRESHOLD)


def pay(ts, person, rate):
    ot = overtime(ts, person)
    return round((ts.hours(person) - ot) * rate + ot * rate * 1.5)
