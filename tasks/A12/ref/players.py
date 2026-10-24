"""The players."""


class Players:
    def __init__(self):
        self._p = {}

    def add(self, name, rating):
        self._p[name] = rating

    def rating(self, name):
        return self._p[name]

    def set_rating(self, name, rating):
        self._p[name]
        self._p[name] = rating

    def names(self):
        return sorted(self._p, key=lambda n: (-self._p[n], n))

    def remove(self, name):
        del self._p[name]

    def count(self):
        return len(self._p)
