"""Trips."""


class Trips:
    def __init__(self, stations):
        self.stations = stations
        self._t = {}
        self._n = 0

    def start(self, rider, station, t, ebike=False, member=False):
        if any(v["rider"] == rider and v["end"] is None for v in self._t.values()):
            raise ValueError("rider already on a trip")
        self.stations.take(station)
        self._n += 1
        self._t[self._n] = {"rider": rider, "from": station, "start": t, "end": None,
                            "ebike": ebike, "member": member}
        return self._n

    def end(self, tid, station, t):
        v = self._t[tid]
        self.stations.dock(station)
        v["end"] = t

    def get(self, tid):
        return dict(self._t[tid])

    def minutes(self, tid):
        v = self._t[tid]
        return v["end"] - v["start"]

    def is_open(self, tid):
        return self._t[tid]["end"] is None

    def ids(self):
        return list(self._t)

    def of_rider(self, rider):
        return [k for k, v in self._t.items() if v["rider"] == rider]

    def open_ids(self):
        return [k for k in self._t if self.is_open(k)]

    def finished(self):
        return [k for k in self._t if not self.is_open(k)]

    def longest(self):
        f = self.finished()
        return min(f, key=lambda k: (-self.minutes(k), k)) if f else None

    def cancel(self, tid):
        v = self._t[tid]
        if v["end"] is not None:
            raise ValueError("trip already ended")
        self.stations.dock(v["from"])
        del self._t[tid]

    def starts(self, station):
        return sum(v["from"] == station for v in self._t.values())

    def riders(self):
        return sorted({v["rider"] for v in self._t.values()})

    def total_minutes(self, rider):
        return sum(self.minutes(k) for k in self.of_rider(rider) if not self.is_open(k))
