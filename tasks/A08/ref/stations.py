"""Docking stations."""


class Stations:
    def __init__(self):
        self._s = {}

    def add(self, name, capacity, bikes):
        if bikes > capacity:
            raise ValueError("more bikes than docks")
        self._s[name] = [capacity, bikes]

    def bikes(self, name):
        return self._s[name][1]

    def capacity(self, name):
        return self._s[name][0]

    def names(self):
        return sorted(self._s, key=str.lower)

    def take(self, name):
        if self._s[name][1] == 0:
            raise ValueError("no bikes")
        self._s[name][1] -= 1

    def dock(self, name):
        c, b = self._s[name]
        if b >= c:
            raise ValueError("station full")
        self._s[name][1] += 1

    def remove(self, name):
        del self._s[name]

    def empty(self):
        return sorted(n for n, (_, b) in self._s.items() if b == 0)

    def total_bikes(self):
        return sum(b for _, b in self._s.values())

    def add_bikes(self, name, n):
        c, b = self._s[name]
        if b + n > c:
            raise ValueError("more bikes than docks")
        self._s[name][1] = b + n

    def free_docks(self, name):
        c, b = self._s[name]
        return c - b
