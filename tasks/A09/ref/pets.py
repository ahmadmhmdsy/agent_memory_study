"""The pets."""


class Pets:
    def __init__(self):
        self._p = {}

    def add(self, name, species, kg):
        if species not in ("dog", "cat"):
            raise ValueError(f"bad species {species!r}")
        if name in self._p:
            raise ValueError(f"{name} is already there")
        self._p[name] = [species, kg]

    def species(self, name):
        return self._p[name][0]

    def kg(self, name):
        return self._p[name][1]

    def set_kg(self, name, kg):
        self._p[name][1] = kg

    def names(self):
        return sorted(self._p)

    def remove(self, name):
        del self._p[name]

    def dogs(self):
        return sorted(n for n, v in self._p.items() if v[0] == "dog")

    def cats(self):
        return sorted(n for n, v in self._p.items() if v[0] == "cat")

    def count(self):
        return len(self._p)
