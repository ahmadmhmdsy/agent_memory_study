"""Hotel rooms."""


def code(number):
    return f"R{number:03d}"


class Hotel:
    def __init__(self):
        self._r = set()

    def add_room(self, number):
        self._r.add(code(number))

    def rooms(self):
        return sorted(self._r)

    def remove_room(self, c):
        self._r.discard(c)
