from decimal import Decimal


def parse_weight(s):
    s = s.strip().lower()
    for suf, f in (("kg", 1000), ("lb", 454), ("g", 1)):
        if s.endswith(suf):
            return int(Decimal(s[:-len(suf)].strip()) * f)
    raise ValueError("unknown unit")


def split_parcels(grams):
    k = -(-grams // 30000)
    q, r = divmod(grams, k)
    return [q + 1] * r + [q] * (k - r)
