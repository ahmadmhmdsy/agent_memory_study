"""Seat bookings and bags."""

MAX_BAGS = 3
MAX_KG = 32


def seat_key(seat):
    return (int(seat[:-1]), seat[-1])


class Bookings:
    def __init__(self, flights):
        self.flights = flights
        self._b = {}
        self._bags = {}
        self._ch = {}
        self._n = 0

    def _check(self, code, seat, skip=None):
        if seat not in self.flights.seats(code):
            raise ValueError(f"no seat {seat!r}")
        for k, v in self._b.items():
            if k != skip and v[0] == code and v[3] == seat:
                raise ValueError("seat taken")

    def book(self, code, name, age, seat):
        self._check(code, seat)
        self._n += 1
        self._b[self._n] = (code, name, age, seat)
        self._bags[self._n] = []
        self._ch[self._n] = 0
        return self._n

    def get(self, bid):
        return self._b[bid]

    def ids(self):
        return list(self._b)

    def free_seats(self, code):
        taken = {v[3] for v in self._b.values() if v[0] == code}
        return sorted((s for s in self.flights.seats(code) if s not in taken), key=seat_key)

    def add_bag(self, bid, kg):
        self._b[bid]
        if kg > MAX_KG:
            raise ValueError("bag too heavy")
        if len(self._bags[bid]) >= MAX_BAGS:
            raise ValueError("too many bags")
        self._bags[bid].append(kg)

    def bags(self, bid):
        self._b[bid]
        return list(self._bags[bid])

    def remove_bag(self, bid, index):
        del self._bags[bid][index]

    def change_seat(self, bid, seat):
        code, name, age, _ = self._b[bid]
        self._check(code, seat, skip=bid)
        self._b[bid] = (code, name, age, seat)
        self._ch[bid] += 1

    def changes(self, bid):
        self._b[bid]
        return self._ch[bid]

    def cancel(self, bid):
        del self._b[bid]
        del self._bags[bid]
        del self._ch[bid]

    def of_flight(self, code):
        return [k for k, v in self._b.items() if v[0] == code]

    def find(self, name):
        return [k for k, v in self._b.items() if name.lower() in v[1].lower()]

    def bag_weight(self, code):
        return sum(sum(self._bags[k]) for k in self.of_flight(code))

    def load(self, code):
        return len(self.of_flight(code))
