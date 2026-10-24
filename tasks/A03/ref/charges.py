"""Rental charges."""

RATE = 4200
FREE_KM = 100
KM_FEE = 30
YOUNG = 12


def days(rentals, rid):
    _, _, _, a, b = rentals.get(rid)
    return (b - a).days


def price(rentals, rid):
    n = days(rentals, rid)
    p = (n - n // 7) * RATE
    if rentals.get(rid)[2] < 25:
        p = round(p * (100 + YOUNG) / 100)
    return p


def extra_km(rentals, rid):
    return max(0, rentals.km(rid) - FREE_KM * days(rentals, rid))


def km_charge(rentals, rid):
    return extra_km(rentals, rid) * KM_FEE


def total(rentals, rid):
    return price(rentals, rid) + km_charge(rentals, rid)


def receipt(rentals, rid):
    return [f"days: {days(rentals, rid)}", f"extra km: {extra_km(rentals, rid)}", f"total: {total(rentals, rid)}"]
