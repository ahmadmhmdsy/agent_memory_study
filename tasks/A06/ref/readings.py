"""Meter readings."""
from meters import _num


class Readings:
    def __init__(self, meters):
        self.meters = meters
        self._h = {}

    def record(self, mid, day, value):
        self.meters.is_social(mid)
        h = self._h.get(mid, [])
        if h and day <= h[-1][0]:
            raise ValueError("reading must be on a later day")
        if h and value < h[-1][1]:
            raise ValueError("reading lower than the last one")
        self._h[mid] = h + [(day, value)]

    def history(self, mid):
        self.meters.is_social(mid)
        return list(self._h.get(mid, []))

    def latest(self, mid):
        h = self.history(mid)
        return h[-1] if h else None

    def first(self, mid):
        h = self.history(mid)
        return h[0] if h else None

    def _at(self, mid, day):
        for d, v in self.history(mid):
            if d == day:
                return v
        raise KeyError(day)

    def usage(self, mid, start, end):
        return self._at(mid, end) - self._at(mid, start)

    def count(self, mid):
        return len(self.history(mid))

    def meters_read(self, day):
        return sorted((m for m, h in self._h.items() if any(d == day for d, _ in h)), key=_num)

    def undo(self, mid):
        if not self._h.get(mid):
            raise KeyError(mid)
        self._h[mid].pop()

    def days(self, mid):
        return [d for d, _ in self.history(mid)]

    def last_day(self):
        days = [d for h in self._h.values() for d, _ in h]
        return max(days) if days else None
