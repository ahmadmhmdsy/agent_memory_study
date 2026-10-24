"""Venue seats."""


class Venue:
    def __init__(self, rows, per_row):
        self._seats = {f"{chr(65 + r)}{n}" for r in range(rows) for n in range(1, per_row + 1)}
        self._h = {}

    def _check(self, seat):
        if seat not in self._seats:
            raise KeyError(seat)

    def reserve(self, seat, name):
        self._check(seat)
        if seat in self._h:
            raise ValueError("seat taken")
        self._h[seat] = name

    def holder(self, seat):
        self._check(seat)
        return self._h.get(seat)

    def free_count(self):
        return len(self._seats) - len(self._h)

    def seats_of(self, name):
        return sorted(s for s, n in self._h.items() if n == name)

    def release(self, seat):
        self._check(seat)
        self._h.pop(seat, None)

    def taken(self):
        return sorted(self._h)
