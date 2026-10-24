"""Customers."""


class Customers:
    def __init__(self):
        self._c = []

    def add(self, name):
        self._c.append(name)

    def has(self, name):
        return name in self._c

    def names(self):
        return sorted(self._c)

    def remove(self, name):
        if name not in self._c:
            raise KeyError(name)
        self._c.remove(name)
