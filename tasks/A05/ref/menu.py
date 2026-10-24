"""The menu."""


class Menu:
    def __init__(self):
        self._p = {}

    def add(self, name, price):
        self._p[name] = price

    def price(self, name):
        return self._p[name]

    def items(self):
        return sorted(self._p, key=lambda n: (self._p[n], n))

    def remove(self, name):
        del self._p[name]

    def set_price(self, name, price):
        self._p[name]
        self._p[name] = price
