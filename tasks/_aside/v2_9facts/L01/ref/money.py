from decimal import Decimal, ROUND_HALF_UP


def _round(x):
    return int(Decimal(x).quantize(Decimal(1), ROUND_HALF_UP))


def parse_cents(s):
    return _round(Decimal(s.strip().lstrip("$").replace(",", "")) * 100)


def invoice_total(lines, rate):
    if not 0 <= rate <= 1:
        raise ValueError("rate out of range")
    sub = 0
    for c, q in lines:
        line = Decimal(c * q)
        if q >= 10:
            line *= Decimal("0.9")
        sub += _round(line)
    return sub + _round(Decimal(sub) * Decimal(str(rate)))
