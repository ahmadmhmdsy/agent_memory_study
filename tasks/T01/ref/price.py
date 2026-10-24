"""Cart prices."""

VAT = 15


def total(cart, prices):
    s = sum(q * prices[k] for k, q in cart.items())
    if s >= 10000:
        s -= 500
    return (s * (100 + VAT) + 50) // 100
