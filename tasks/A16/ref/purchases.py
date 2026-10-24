"""Purchases and rewards."""

PER_100 = 3
REWARD = 120
MAX_PER_DAY = 3


class Purchases:
    def __init__(self, members):
        self.members = members
        self._p = {}
        self._r = []
        self._n = 0

    def buy(self, name, cents, day):
        from points import is_gold
        self.members.points(name)
        if cents < 1:
            raise ValueError("a purchase needs an amount")
        earned = cents // 100 * PER_100
        if is_gold(self, name):
            earned *= 2
        self._n += 1
        self._p[self._n] = (name, cents, day)
        self.members.add_points(name, earned)
        return self._n

    def get(self, pid):
        return self._p[pid]

    def ids(self):
        return list(self._p)

    def count(self):
        return len(self._p)

    def last(self):
        return self._n if self._p else None

    def of_member(self, name):
        return [k for k, v in self._p.items() if v[0] == name]

    def spent(self, name):
        return sum(self._p[k][1] for k in self.of_member(name))

    def total(self):
        return sum(v[1] for v in self._p.values())

    def redeem(self, name, day):
        if self.members.points(name) < REWARD:
            raise ValueError("not enough points")
        if sum(r == (name, day) for r in self._r) >= MAX_PER_DAY:
            raise ValueError("too many rewards today")
        self.members.add_points(name, -REWARD)
        self._r.append((name, day))

    def redeemed(self, name):
        return sum(r[0] == name for r in self._r)

    def redeemed_total(self):
        return len(self._r)

    def on_day(self, day):
        return [k for k, v in self._p.items() if v[2] == day]

    def gold_members(self):
        from points import is_gold
        return sorted(n for n in {v[0] for v in self._p.values()} if is_gold(self, n))

    def biggest(self):
        return max(self._p, key=lambda k: (self._p[k][1], -k)) if self._p else None

    def days(self):
        return sorted({v[2] for v in self._p.values()})

    def visits(self, name):
        return len({self._p[k][2] for k in self.of_member(name)})
