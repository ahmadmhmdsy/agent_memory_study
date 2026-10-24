"""Parking garage."""
from tariff import fee


def _p(plate):
    return plate.replace(" ", "").upper()


class Garage:
    def __init__(self):
        self._in = {}
        self._stays = {}

    def enter(self, plate, minute):
        p = _p(plate)
        if p in self._in:
            raise ValueError("already inside")
        self._in[p] = minute

    def leave(self, plate, minute):
        p = _p(plate)
        if p not in self._in:
            raise KeyError(p)
        if minute < self._in[p]:
            raise ValueError("leave before entry")
        m = minute - self._in.pop(p)
        self._stays.setdefault(p, []).append(m)
        return m

    def inside(self):
        return sorted(self._in)

    def count(self):
        return len(self._in)

    def history(self, plate):
        return list(self._stays.get(_p(plate), []))

    def revenue(self):
        return sum(fee(m) for s in self._stays.values() for m in s)
