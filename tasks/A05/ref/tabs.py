"""Table tabs."""

MAX_LINES = 40


class Tabs:
    def __init__(self, menu):
        self.menu = menu
        self._t = {}
        self._n = 0

    def open(self, table, guests, staff=False):
        self._n += 1
        self._t[self._n] = {"table": table, "guests": guests, "staff": staff, "lines": [], "open": True}
        return self._n

    def order(self, tid, dish, qty):
        t = self._t[tid]
        if not t["open"]:
            raise ValueError("tab is closed")
        if qty < 1:
            raise ValueError("quantity must be 1 or more")
        self.menu.price(dish)
        if len(t["lines"]) >= MAX_LINES:
            raise ValueError("tab is full")
        t["lines"].append((dish, qty))

    def lines(self, tid):
        return list(self._t[tid]["lines"])

    def table(self, tid):
        return self._t[tid]["table"]

    def guests(self, tid):
        return self._t[tid]["guests"]

    def is_staff(self, tid):
        return self._t[tid]["staff"]

    def close(self, tid):
        self._t[tid]["open"] = False

    def reopen(self, tid):
        self._t[tid]["open"] = True

    def is_open(self, tid):
        return self._t[tid]["open"]

    def ids(self):
        return list(self._t)

    def of_table(self, table):
        return [k for k, v in self._t.items() if v["table"] == table]

    def open_ids(self):
        return [k for k, v in self._t.items() if v["open"]]

    def guests_total(self):
        return sum(self._t[k]["guests"] for k in self.open_ids())

    def move(self, tid, table):
        self._t[tid]["table"] = table

    def void(self, tid, index):
        if not self._t[tid]["open"]:
            raise ValueError("tab is closed")
        del self._t[tid]["lines"][index]

    def item_count(self, tid):
        return sum(q for _, q in self._t[tid]["lines"])
