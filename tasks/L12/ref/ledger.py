class Ledger:
    def __init__(self):
        self.bal = {}
        self.hist = {}

    def open(self, account):
        a = account.lower()
        if a in self.bal:
            raise ValueError("account exists")
        self.bal[a] = 0
        self.hist[a] = []

    def _chg(self, a, c):
        self.bal[a] += c
        self.hist[a].append(c)

    def deposit(self, account, cents):
        if cents <= 0:
            raise ValueError("amount must be positive")
        self._chg(account.lower(), cents)

    def withdraw(self, account, cents):
        if cents <= 0:
            raise ValueError("amount must be positive")
        a = account.lower()
        if self.bal[a] - cents - 25 < 0:
            raise ValueError("no overdraft")
        self._chg(a, -cents)
        self._chg(a, -25)

    def balance(self, account):
        return self.bal[account.lower()]

    def transfer(self, src, dst, cents):
        if cents <= 0:
            raise ValueError("amount must be positive")
        a, b = src.lower(), dst.lower()
        if a == b:
            raise ValueError("same account")
        if self.bal[a] - cents < 0:
            raise ValueError("no overdraft")
        self._chg(a, -cents)
        self._chg(b, cents)

    def history(self, account, n=None):
        h = list(self.hist[account.lower()])
        return h[-n:] if n else h

    def accounts(self):
        return sorted(self.bal)
