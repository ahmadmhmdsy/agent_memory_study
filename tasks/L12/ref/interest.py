def monthly_interest(balance):
    return min(balance, 100000) // 100 + max(0, balance - 100000) * 2 // 100
