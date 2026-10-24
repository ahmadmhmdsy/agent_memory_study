class Office:
    def __init__(self):
        self.bookings = {}
        self.n = 0

    def book(self, event, adults, children, today):
        k = adults + children
        if k < 1 or k > 6:
            raise ValueError("bad ticket count")
        if event.date < today:
            raise ValueError("event is over")
        if k > event.seats_left():
            raise ValueError("not enough seats")
        event.sold += k
        self.n += 1
        ref = f"B{self.n:05d}"
        self.bookings[ref] = (event, adults, children)
        return ref

    def count(self):
        return len(self.bookings)

    def cancel(self, ref):
        b = self.bookings.pop(ref, None)
        if b is None:
            return False
        b[0].sold -= b[1] + b[2]
        return True
