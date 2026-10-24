"""The watering and feeding log."""


class Care:
    def __init__(self, plants):
        self.plants = plants
        self._w = {}
        self._f = {}

    def water(self, name, day):
        self.plants.kind(name)
        w = self._w.setdefault(name, [])
        if w and day < w[-1]:
            raise ValueError("watering before the last one")
        w.append(day)

    def waterings(self, name):
        self.plants.kind(name)
        return list(self._w.get(name, []))

    def feed(self, name, day):
        if day not in self.waterings(name):
            raise ValueError("feed only on a watering day")
        self._f.setdefault(name, []).append(day)

    def feedings(self, name):
        self.plants.kind(name)
        return list(self._f.get(name, []))

    def last_watered(self, name):
        w = self.waterings(name)
        return w[-1] if w else None

    def first_watered(self, name):
        w = self.waterings(name)
        return w[0] if w else None

    def count(self, name):
        return len(self.waterings(name))

    def undo_water(self, name):
        if not self._w.get(name):
            raise KeyError(name)
        self._w[name].pop()

    def watered_on(self, day):
        return sorted(n for n, w in self._w.items() if day in w)

    def total_waterings(self):
        return sum(len(w) for w in self._w.values())
