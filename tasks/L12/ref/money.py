from decimal import Decimal


def parse_amount(s):
    v = int(Decimal(s.strip().replace("$", "").replace(",", "")) * 100)
    if v <= 0:
        raise ValueError("amount must be positive")
    return v
