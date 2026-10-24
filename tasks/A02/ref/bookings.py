"""Room bookings."""

MAX_NIGHTS = 28
CANCEL_FEE = 20


class Bookings:
    def __init__(self, hotel):
        self.hotel = hotel
        self._b = {}
        self._n = 0

    def _check(self, room, guest, checkin, checkout, skip=None):
        if not guest:
            raise ValueError("guest name required")
        if checkout <= checkin:
            raise ValueError("checkout must be after checkin")
        if (checkout - checkin).days > MAX_NIGHTS:
            raise ValueError("too many nights")
        for k, (r, _, a, b) in self._b.items():
            if k != skip and r == room and checkin < b and a < checkout:
                raise ValueError("room already booked")

    def book(self, room, guest, checkin, checkout):
        guest = guest.strip().title()
        self._check(room, guest, checkin, checkout)
        self._n += 1
        self._b[self._n] = (room, guest, checkin, checkout)
        return self._n

    def get(self, bid):
        return self._b[bid]

    def ids(self):
        return list(self._b)

    def is_free(self, room, day):
        return not any(r == room and a <= day < b for r, _, a, b in self._b.values())

    def of_guest(self, guest):
        return [k for k, v in self._b.items() if v[1] == guest.strip().title()]

    def cancel(self, bid):
        from billing import price
        fee = round(price(self, bid) * CANCEL_FEE / 100)
        del self._b[bid]
        return fee

    def guests(self):
        return sorted({v[1] for v in self._b.values()})

    def occupancy(self, day):
        return sum(a <= day < b for _, _, a, b in self._b.values())

    def extend(self, bid, checkout):
        r, g, a, _ = self._b[bid]
        self._check(r, g, a, checkout, skip=bid)
        self._b[bid] = (r, g, a, checkout)

    def move(self, bid, room):
        _, g, a, b = self._b[bid]
        self._check(room, g, a, b, skip=bid)
        self._b[bid] = (room, g, a, b)

    def nights_booked(self, room):
        return sum((b - a).days for r, _, a, b in self._b.values() if r == room)

    def guest_nights(self, guest):
        return sum((v[3] - v[2]).days for v in self._b.values() if v[1] == guest.strip().title())

    def find(self, text):
        return [k for k, v in self._b.items() if text.lower() in v[1].lower()]
