"""Trip expenses."""


def _shares(amount, people):
    base, left = divmod(amount, len(people))
    return {p: base + (1 if i < left else 0) for i, p in enumerate(sorted(people, reverse=True))}


class Trip:
    def __init__(self):
        self._e = []

    def add_expense(self, payer, amount, people):
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            raise ValueError("amount is a positive int")
        if not people or len(set(people)) != len(people):
            raise ValueError("people must be non-empty and unique")
        self._e.append((payer, amount, list(people)))

    def balance(self, name):
        b = 0
        for payer, amount, people in self._e:
            if payer == name:
                b += amount
            b -= _shares(amount, people).get(name, 0)
        return b

    def people(self):
        return sorted({p for payer, _, ps in self._e for p in [payer, *ps]})

    def undo(self):
        if not self._e:
            raise IndexError("no expenses")
        self._e.pop()

    def total(self):
        return sum(a for _, a, _ in self._e)
