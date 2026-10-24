"""Hotel bookings."""


class Hotel:
    def __init__(self, rooms):
        self._rooms = set(rooms)
        self._b = []

    def book(self, room, guest, first_night, nights):
        if room not in self._rooms:
            raise KeyError(room)
        if not isinstance(nights, int) or not 1 <= nights <= 14:
            raise ValueError("a booking is 1 to 14 nights")
        for r, g, f, n in self._b:
            if r == room and first_night < f + n and f < first_night + nights:
                raise ValueError("room already booked")
        self._b.append((room, guest, first_night, nights))

    def guest_in(self, room, night):
        for r, g, f, n in self._b:
            if r == room and f <= night < f + n:
                return g
        return None

    def bookings(self, guest):
        return [(r, f, n) for r, g, f, n in self._b if g == guest]

    def cancel(self, room, first_night):
        self._b = [b for b in self._b if not (b[0] == room and b[2] == first_night)]

    def free_rooms(self, night):
        return sorted(r for r in self._rooms if self.guest_in(r, night) is None)
