"""Rooms."""


class Rooms:
    def __init__(self):
        self._r = {}

    def add(self, name, seats):
        self._r[name] = seats

    def seats(self, name):
        return self._r[name]

    def names(self):
        return list(self._r)

    def remove(self, name):
        del self._r[name]

    def capacity(self):
        return sum(self._r.values())

    def count(self):
        return len(self._r)
