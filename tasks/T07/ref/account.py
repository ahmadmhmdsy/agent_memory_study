"""Bank account."""

LIMIT = -2000


def _check(amount):
    if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
        raise ValueError("amount must be a positive int")


class Account:
    def __init__(self):
        self._b = 0
        self._h = []

    def deposit(self, amount):
        _check(amount)
        if amount > 1000000:
            raise ValueError("deposit too large")
        self._b += amount
        self._h.append(("deposit", amount))

    def withdraw(self, amount):
        _check(amount)
        if self._b - amount < LIMIT:
            raise ValueError("over the overdraft limit")
        self._b -= amount
        self._h.append(("withdraw", amount))

    def balance(self):
        return self._b

    def history(self):
        return list(self._h)

    def add_interest(self, pct):
        if self._b <= 0:
            return
        n = self._b * pct // 100
        if n:
            self._b += n
            self._h.append(("interest", n))

    def count(self, kind):
        return sum(k == kind for k, _ in self._h)
