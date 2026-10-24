"""Appointments."""
from collections import Counter

SLOT = 45
OPEN = 480
LAST = 1080
KINDS = ("checkup", "filling", "cleaning")


class Schedule:
    def __init__(self, patients):
        self.patients = patients
        self._a = {}
        self._st = {}
        self._n = 0

    def _check(self, pid, day, start, kind, skip=None):
        self.patients.name(pid)
        if kind not in KINDS:
            raise ValueError(f"bad kind {kind!r}")
        if not OPEN <= start < LAST:
            raise ValueError("clinic closed")
        for k, (_, d, s, _) in self._a.items():
            if k != skip and d == day and start < s + SLOT and s < start + SLOT:
                raise ValueError("chair taken")

    def book(self, pid, day, start, kind):
        self._check(pid, day, start, kind)
        self._n += 1
        self._a[self._n] = (pid, day, start, kind)
        self._st[self._n] = "open"
        return self._n

    def get(self, aid):
        return self._a[aid]

    def end(self, aid):
        return self._a[aid][2] + SLOT

    def day(self, day):
        return sorted((k for k, v in self._a.items() if v[1] == day), key=lambda k: self._a[k][2])

    def mark(self, aid, status):
        self._a[aid]
        if status not in ("done", "missed"):
            raise ValueError(f"bad status {status!r}")
        self._st[aid] = status

    def status(self, aid):
        self._a[aid]
        return self._st[aid]

    def cancel(self, aid):
        del self._a[aid]
        del self._st[aid]

    def ids(self):
        return list(self._a)

    def of_patient(self, pid):
        return [k for k, v in self._a.items() if v[0] == pid]

    def count(self, day):
        return len(self.day(day))

    def move(self, aid, day, start):
        pid, _, _, kind = self._a[aid]
        self._check(pid, day, start, kind, skip=aid)
        self._a[aid] = (pid, day, start, kind)

    def missed(self, pid):
        return sum(self._st[k] == "missed" for k in self.of_patient(pid))

    def kinds(self, day):
        return dict(Counter(self._a[k][3] for k in self.day(day)))

    def first(self, day):
        d = self.day(day)
        return d[0] if d else None

    def open_ids(self):
        return [k for k in self._a if self._st[k] == "open"]
