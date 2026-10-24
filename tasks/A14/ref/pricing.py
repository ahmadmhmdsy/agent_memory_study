"""Job prices."""

BW = 12
COLOR = 45
BULK = 250
BULK_PCT = 10
BINDING = 400
RUSH = 25


def price(jobs, jid):
    _, pages, size, _, _ = jobs.get(jid)
    per = COLOR if jobs.is_color(jid) else BW
    if size == "A3":
        per *= 2
    p = pages * per
    if pages >= BULK:
        p = round(p * (100 - BULK_PCT) / 100)
    if jobs.is_bound(jid):
        p += BINDING
    if jobs.is_rush(jid):
        p = round(p * (100 + RUSH) / 100)
    return p


def revenue(jobs):
    return sum(price(jobs, k) for k in jobs.ids())
