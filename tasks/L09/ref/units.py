ML = {"ml": 1, "tsp": 5, "tbsp": 15, "cup": 250}


def parse_qty(s):
    total = 0.0
    for p in s.split():
        if "/" in p:
            a, b = p.split("/")
            total += float(a) / float(b)
        else:
            total += float(p)
    if total <= 0:
        raise ValueError("quantity must be positive")
    return total


def to_ml(qty, unit):
    if qty <= 0:
        raise ValueError("quantity must be positive")
    u = unit.strip().lower()
    if u not in ML and u.endswith("s"):
        u = u[:-1]
    if u not in ML:
        raise ValueError("unknown unit")
    return qty * ML[u]
