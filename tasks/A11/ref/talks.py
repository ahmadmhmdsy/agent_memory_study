"""Talks."""

OPEN, CLOSE = 480, 1080
MAX_MIN = 40
GAP = 5
PER_SPEAKER = 3


class Talks:
    def __init__(self, rooms):
        self.rooms = rooms
        self._t = {}
        self._n = 0

    def _check(self, speaker, room, start, minutes, skip=None):
        if room not in self.rooms.names():
            raise ValueError(f"no room {room!r}")
        if start < OPEN or start + minutes > CLOSE:
            raise ValueError("outside the day")
        if minutes > MAX_MIN:
            raise ValueError("talk too long")
        for k, (_, s, r, st, m) in self._t.items():
            if k == skip or r != room:
                continue
            if start < st + m + GAP and st < start + minutes + GAP:
                raise ValueError("too close to another talk")
        if sum(v[1] == speaker for k, v in self._t.items() if k != skip) >= PER_SPEAKER:
            raise ValueError("speaker has too many talks")

    def add(self, title, speaker, room, start, minutes):
        self._check(speaker, room, start, minutes)
        self._n += 1
        self._t[self._n] = (title, speaker, room, start, minutes)
        return self._n

    def get(self, tid):
        return self._t[tid]

    def end(self, tid):
        v = self._t[tid]
        return v[3] + v[4]

    def ids(self):
        return list(self._t)

    def count(self):
        return len(self._t)

    def agenda(self, room):
        return sorted((k for k, v in self._t.items() if v[2] == room), key=lambda k: self._t[k][3])

    def room_talks(self, room):
        return len(self.agenda(room))

    def of_speaker(self, speaker):
        return [k for k, v in self._t.items() if v[1] == speaker]

    def remove(self, tid):
        del self._t[tid]

    def move(self, tid, start):
        title, s, r, _, m = self._t[tid]
        self._check(s, r, start, m, skip=tid)
        self._t[tid] = (title, s, r, start, m)

    def speakers(self):
        return sorted({v[1] for v in self._t.values()})

    def minutes_in(self, room):
        return sum(v[4] for v in self._t.values() if v[2] == room)

    def at(self, minute):
        return [k for k, v in self._t.items() if v[3] <= minute < v[3] + v[4]]

    def free_after(self, room):
        a = self.agenda(room)
        return max(self.end(k) for k in a) if a else OPEN

    def rename(self, tid, title):
        _, s, r, st, m = self._t[tid]
        self._t[tid] = (title, s, r, st, m)
