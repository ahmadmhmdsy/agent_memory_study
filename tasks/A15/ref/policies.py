"""Policies."""


class Policies:
    def __init__(self):
        self._p = {}

    def add(self, number, holder, kind):
        if kind not in ("car", "home"):
            raise ValueError(f"bad kind {kind!r}")
        self._p[number] = (holder, kind)

    def holder(self, number):
        return self._p[number][0]

    def kind(self, number):
        return self._p[number][1]

    def numbers(self):
        return sorted(self._p, key=lambda n: (self._p[n][0], n))

    def remove(self, number):
        del self._p[number]

    def count(self):
        return len(self._p)

    def of_holder(self, holder):
        return sorted(n for n, v in self._p.items() if v[0] == holder)

    def of_kind(self, kind):
        return sorted(n for n, v in self._p.items() if v[1] == kind)
