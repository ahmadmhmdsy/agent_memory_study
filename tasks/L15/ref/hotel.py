class Hotel:
    def __init__(self):
        self.rooms = {}
        self.bookings = {}
        self.n = 0

    def add_room(self, number, kind, price):
        if not isinstance(number, int) or number <= 0 or number in self.rooms:
            raise ValueError("bad room number")
        self.rooms[number] = (kind, price)

    def _free(self, room, start, end):
        return all(not (s < end and start < e) for g, r, s, e in self.bookings.values() if r == room)

    def book(self, guest, kind, start, end):
        if (end - start).days < 2:
            raise ValueError("at least 2 nights")
        for num in sorted(self.rooms):
            if self.rooms[num][0] == kind and self._free(num, start, end):
                self.n += 1
                self.bookings[self.n] = (guest.lower(), num, start, end)
                return self.n
        raise ValueError("no room free")

    def room_of(self, bid):
        return self.bookings[bid][1]

    def cancel(self, bid):
        del self.bookings[bid]

    def free_rooms(self, start, end, kind=None):
        return [n for n in sorted(self.rooms)
                if (kind is None or self.rooms[n][0] == kind) and self._free(n, start, end)]

    def guest_bookings(self, name):
        return sorted((b for b, v in self.bookings.items() if v[0] == name.lower()),
                      key=lambda b: (self.bookings[b][2], b))

    def occupancy(self, day):
        return sum(1 for g, r, s, e in self.bookings.values() if s <= day < e)
