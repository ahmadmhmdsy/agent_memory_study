"""Rentals."""

MIN_AGE = 23


class Rentals:
    def __init__(self, fleet):
        self.fleet = fleet
        self._r = {}
        self._km = {}
        self._n = 0

    def _check(self, plate, age, pickup, ret, skip=None):
        self.fleet.car_class(plate)
        if age < MIN_AGE:
            raise ValueError("driver too young")
        if ret <= pickup:
            raise ValueError("return must be after pickup")
        for k, (p, _, _, a, b) in self._r.items():
            if k != skip and p == plate and pickup < b and a < ret:
                raise ValueError("car already rented")

    def book(self, plate, driver, age, pickup, ret):
        self._check(plate, age, pickup, ret)
        self._n += 1
        self._r[self._n] = (plate, driver, age, pickup, ret)
        return self._n

    def get(self, rid):
        return self._r[rid]

    def ids(self):
        return list(self._r)

    def finish(self, rid, km):
        self._r[rid]
        if km < 0:
            raise ValueError("km must be 0 or more")
        self._km[rid] = km

    def km(self, rid):
        self._r[rid]
        return self._km.get(rid, 0)

    def of_driver(self, driver):
        return [k for k, v in self._r.items() if v[1] == driver]

    def cancel(self, rid):
        del self._r[rid]
        self._km.pop(rid, None)

    def on_road(self, day):
        return sorted(p for p, _, _, a, b in self._r.values() if a <= day < b)

    def is_free(self, plate, day):
        return plate not in self.on_road(day)

    def days_rented(self, plate):
        return sum((b - a).days for p, _, _, a, b in self._r.values() if p == plate)

    def extend(self, rid, ret):
        p, d, age, a, _ = self._r[rid]
        self._check(p, age, a, ret, skip=rid)
        self._r[rid] = (p, d, age, a, ret)

    def drivers(self):
        return sorted({v[1] for v in self._r.values()})
