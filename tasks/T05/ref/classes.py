"""Gym classes."""


class Schedule:
    def __init__(self):
        self._cap = {}
        self._booked = {}
        self._wait = {}

    def add_class(self, name, capacity):
        if not 1 <= capacity <= 30:
            raise ValueError("capacity is 1 to 30")
        self._cap[name] = capacity
        self._booked[name] = []
        self._wait[name] = []

    def book(self, name, member):
        if member in self._booked[name] or member in self._wait[name]:
            raise ValueError("already booked")
        if len(self._booked[name]) < self._cap[name]:
            self._booked[name].append(member)
            return True
        self._wait[name].append(member)
        return False

    def booked(self, name):
        return list(self._booked[name])

    def waitlist(self, name):
        return list(self._wait[name])

    def cancel(self, name, member):
        if member in self._wait[name]:
            self._wait[name].remove(member)
            return
        self._booked[name].remove(member)
        if self._wait[name]:
            self._booked[name].append(self._wait[name].pop(0))

    def classes(self):
        return sorted(self._cap)

    def busy(self, member):
        return sorted(n for n, b in self._booked.items() if member in b)
