"""Loyalty rules."""

GOLD_AT = 120000


def is_gold(purchases, name):
    return purchases.spent(name) >= GOLD_AT
