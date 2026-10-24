"""Stays."""
import datetime as dt

MAX_NIGHTS = 28


class Stays:
    def __init__(self, pets):
        self.pets = pets
        self._s = {}
        self._n = 0

    def _check(self, pet, checkin, nights, skip=None):
        self.pets.species(pet)
        if nights > MAX_NIGHTS:
            raise ValueError("stay too long")
        end = checkin + dt.timedelta(nights)
        for k, (p, c, n, _) in self._s.items():
            if k != skip and p == pet and checkin < c + dt.timedelta(n) and c < end:
                raise ValueError("stays overlap")

    def book(self, pet, checkin, nights, meds=False):
        self._check(pet, checkin, nights)
        self._n += 1
        self._s[self._n] = (pet, checkin, nights, meds)
        return self._n

    def get(self, sid):
        return self._s[sid]

    def checkout(self, sid):
        _, c, n, _ = self._s[sid]
        return c + dt.timedelta(n)

    def ids(self):
        return list(self._s)

    def count(self):
        return len(self._s)

    def of_pet(self, pet):
        return [k for k, v in self._s.items() if v[0] == pet]

    def on_night(self, day):
        return [k for k, (_, c, n, _) in self._s.items() if c <= day < c + dt.timedelta(n)]

    def occupancy(self, day):
        return len(self.on_night(day))

    def pets_on(self, day):
        return sorted(self._s[k][0] for k in self.on_night(day))

    def cancel(self, sid):
        del self._s[sid]

    def extend(self, sid, n):
        p, c, old, m = self._s[sid]
        self._check(p, c, old + n, skip=sid)
        self._s[sid] = (p, c, old + n, m)

    def nights_total(self, pet):
        return sum(self._s[k][2] for k in self.of_pet(pet))
