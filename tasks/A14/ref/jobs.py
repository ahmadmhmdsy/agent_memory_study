"""Print jobs."""


class Jobs:
    def __init__(self, customers):
        self.customers = customers
        self._j = {}
        self._opt = {}
        self._n = 0

    def add(self, customer, pages, size, ordered, due):
        if not self.customers.has(customer):
            raise KeyError(customer)
        if size not in ("A4", "A3"):
            raise ValueError(f"bad size {size!r}")
        if pages < 1:
            raise ValueError("a job needs pages")
        if due < ordered:
            raise ValueError("due before ordered")
        self._n += 1
        self._j[self._n] = (customer, pages, size, ordered, due)
        self._opt[self._n] = set()
        return self._n

    def get(self, jid):
        return self._j[jid]

    def ids(self):
        return list(self._j)

    def count(self):
        return len(self._j)

    def _set(self, jid, flag):
        self._j[jid]
        self._opt[jid].add(flag)

    def set_color(self, jid):
        self._set(jid, "color")

    def bind(self, jid):
        self._set(jid, "bound")

    def set_rush(self, jid):
        self._set(jid, "rush")

    def is_color(self, jid):
        return "color" in self._opt[jid]

    def is_bound(self, jid):
        return "bound" in self._opt[jid]

    def is_rush(self, jid):
        return "rush" in self._opt[jid]

    def of_customer(self, customer):
        return [k for k, v in self._j.items() if v[0] == customer]

    def pages_total(self, customer):
        return sum(self._j[k][1] for k in self.of_customer(customer))

    def cancel(self, jid):
        del self._j[jid]
        del self._opt[jid]

    def due_on(self, day):
        return [k for k, v in self._j.items() if v[4] == day]

    def late(self, day):
        return [k for k, v in self._j.items() if v[4] < day]

    def color_ids(self):
        return [k for k in self._j if self.is_color(k)]

    def of_size(self, size):
        return [k for k, v in self._j.items() if v[2] == size]

    def customers_with_jobs(self):
        return sorted({v[0] for v in self._j.values()})

    def next_due(self):
        return min((v[4] for v in self._j.values()), default=None)
