"""Plants."""

RAIN_MIN = 2


class Garden:
    def __init__(self):
        self.every = {}
        self._last = {}

    def add(self, plant, every_days, day):
        if not isinstance(every_days, int) or isinstance(every_days, bool) or not 1 <= every_days <= 30:
            raise ValueError("every_days is 1 to 30")
        if plant in self.every:
            raise ValueError("plant exists")
        self.every[plant] = every_days
        self._last[plant] = day

    def water(self, plant, day):
        if plant not in self.every:
            raise KeyError(plant)
        self._last[plant] = day

    def last(self, plant):
        return self._last[plant]

    def rain(self, day):
        for p, e in self.every.items():
            if e >= RAIN_MIN:
                self._last[p] = day

    def plants(self):
        return sorted(self.every)

    def remove(self, plant):
        self.every.pop(plant, None)
        self._last.pop(plant, None)
