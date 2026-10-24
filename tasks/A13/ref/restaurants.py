"""Restaurants and menus."""


class Restaurants:
    def __init__(self):
        self._r = {}

    def add(self, name):
        self._r[name] = {}

    def add_dish(self, name, dish, price):
        self._r[name][dish] = price

    def price(self, name, dish):
        return self._r[name][dish]

    def dishes(self, name):
        m = self._r[name]
        return sorted(m, key=lambda d: (m[d], d))

    def remove(self, name):
        del self._r[name]

    def names(self):
        return sorted(self._r)
