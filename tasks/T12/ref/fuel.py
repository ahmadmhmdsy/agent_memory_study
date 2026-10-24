"""Fuel log."""

TANK = 60


class FuelLog:
    def __init__(self):
        self._f = []

    def add(self, odometer, litres):
        if self._f and odometer <= self._f[-1][0]:
            raise ValueError("odometer must increase")
        if not 0 < litres <= TANK:
            raise ValueError("litres out of range")
        self._f.append((odometer, litres))

    def fills(self):
        return list(self._f)

    def distance(self):
        return self._f[-1][0] - self._f[0][0] if self._f else 0

    def last(self):
        return self._f[-1] if self._f else None
