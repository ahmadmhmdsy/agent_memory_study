"""Claim payouts."""

DEDUCTIBLE = 30000
PCT = 75
CAP = 800000


def payout(claims, cid):
    if claims.is_denied(cid):
        return 0
    amount = claims.get(cid)[1]
    return min(CAP, round(max(0, amount - DEDUCTIBLE) * PCT / 100))


def total_paid(claims):
    return sum(payout(claims, k) for k in claims.ids())
