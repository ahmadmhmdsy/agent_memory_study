"""The plants."""

KINDS = ("herb", "cactus", "fern")


class Plants:
    def __init__(self):
        self._p = {}

    def add(self, name, kind, day):
        if kind not in KINDS:
            raise ValueError(f"bad kind {kind!r}")
        self._p[name] = [kind, day]

    def kind(self, name):
        return self._p[name][0]

    def set_kind(self, name, kind):
        self._p[name]
        if kind not in KINDS:
            raise ValueError(f"bad kind {kind!r}")
        self._p[name][0] = kind

    def added(self, name):
        return self._p[name][1]

    def names(self):
        return list(self._p)

    def remove(self, name):
        del self._p[name]

    def of_kind(self, kind):
        return sorted(n for n, v in self._p.items() if v[0] == kind)

    def count(self):
        return len(self._p)

    def kinds(self):
        return sorted({v[0] for v in self._p.values()})
