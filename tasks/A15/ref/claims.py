"""Claims."""

WINDOW = 45
MAX_CLAIMS = 4


class Claims:
    def __init__(self, policies):
        self.policies = policies
        self._c = {}
        self._denied = set()
        self._n = 0

    def file(self, number, amount, incident, filed):
        self.policies.holder(number)
        if amount < 1:
            raise ValueError("amount must be positive")
        if incident > filed:
            raise ValueError("incident after filing")
        if (filed - incident).days > WINDOW:
            raise ValueError("filed too late")
        if len(self.of_policy(number)) >= MAX_CLAIMS:
            raise ValueError("too many claims")
        self._n += 1
        self._c[self._n] = (number, amount, incident, filed)
        return self._n

    def get(self, cid):
        return self._c[cid]

    def ids(self):
        return list(self._c)

    def count(self):
        return len(self._c)

    def last(self):
        return self._n if self._c else None

    def of_policy(self, number):
        return [k for k, v in self._c.items() if v[0] == number]

    def deny(self, cid):
        self._c[cid]
        self._denied.add(cid)

    def is_denied(self, cid):
        self._c[cid]
        return cid in self._denied

    def denied_ids(self):
        return [k for k in self._c if k in self._denied]

    def open_ids(self):
        return [k for k in self._c if k not in self._denied]

    def filed_on(self, day):
        return [k for k, v in self._c.items() if v[3] == day]

    def since(self, day):
        return [k for k, v in self._c.items() if v[3] >= day]

    def amount_total(self, number):
        return sum(self._c[k][1] for k in self.of_policy(number))

    def largest(self):
        return max(self._c, key=lambda k: (self._c[k][1], -k)) if self._c else None
