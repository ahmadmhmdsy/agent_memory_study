class Account:
    def __init__(self):
        self.balance = 0
        self.moves = []

    def deposit(self, amount):
        self.balance += amount
        self.moves.append(amount)

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
        self.moves.append(-amount)

    def transaction_count(self):
        return len(self.moves)

    def statement(self):
        return [f"{m:+d}" for m in self.moves]

    def largest_deposit(self):
        return max([m for m in self.moves if m > 0], default=0)
