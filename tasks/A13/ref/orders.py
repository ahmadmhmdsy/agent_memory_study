"""Orders."""

MAX_KM = 10
MIN_ORDER = 1200
FLOW = ["placed", "cooking", "out", "delivered"]


class Orders:
    def __init__(self, restaurants):
        self.restaurants = restaurants
        self._o = {}
        self._st = {}
        self._n = 0

    def place(self, rest, items, km, minute):
        menu = self.restaurants.dishes(rest)
        if any(d not in menu for d, _ in items):
            raise ValueError("dish not on the menu")
        if km > MAX_KM:
            raise ValueError("too far")
        if sum(self.restaurants.price(rest, d) * q for d, q in items) < MIN_ORDER:
            raise ValueError("order too small")
        self._n += 1
        self._o[self._n] = (rest, list(items), km, minute)
        self._st[self._n] = "placed"
        return self._n

    def get(self, oid):
        return self._o[oid]

    def ids(self):
        return list(self._o)

    def count(self):
        return len(self._o)

    def status(self, oid):
        return self._st[oid]

    def set_status(self, oid, status):
        cur = self._st[oid]
        if cur == FLOW[-1] or status != FLOW[FLOW.index(cur) + 1]:
            raise ValueError(f"cannot go from {cur} to {status}")
        self._st[oid] = status

    def of_restaurant(self, rest):
        return [k for k, v in self._o.items() if v[0] == rest]

    def items_count(self, oid):
        return sum(q for _, q in self._o[oid][1])

    def open_ids(self):
        return [k for k in self._o if self._st[k] != "delivered"]

    def at_status(self, status):
        return [k for k in self._o if self._st[k] == status]

    def cancel(self, oid):
        if self._st[oid] != "placed":
            raise ValueError("order already under way")
        del self._o[oid]
        del self._st[oid]

    def busiest(self):
        rs = sorted({v[0] for v in self._o.values()})
        return max(rs, key=lambda r: (len(self.of_restaurant(r)), [-ord(c) for c in r])) if rs else None

    def km_total(self):
        return sum(v[2] for v in self._o.values())
