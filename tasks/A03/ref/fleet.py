"""The cars."""

CLASSES = ("economy", "compact", "van")


class Fleet:
    def __init__(self):
        self._c = {}

    def add(self, plate, car_class):
        if car_class not in CLASSES:
            raise ValueError(f"bad class {car_class!r}")
        self._c[plate] = car_class

    def car_class(self, plate):
        return self._c[plate]

    def plates(self):
        return sorted(self._c, key=lambda p: (CLASSES.index(self._c[p]), p))

    def remove(self, plate):
        del self._c[plate]
