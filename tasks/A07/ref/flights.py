"""Flights."""


class Flights:
    def __init__(self):
        self._f = {}

    def add(self, code, seats, fare):
        self._f[code] = (list(seats), fare)

    def seats(self, code):
        return list(self._f[code][0])

    def fare(self, code):
        return self._f[code][1]

    def codes(self):
        return sorted(self._f)

    def remove(self, code):
        del self._f[code]
