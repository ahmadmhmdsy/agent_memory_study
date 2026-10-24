from decimal import Decimal, ROUND_HALF_UP


def parse_cents(s):
    return int((Decimal(s) * 100).quantize(Decimal(1), ROUND_HALF_UP))


def invoice_total(lines, rate):
    sub = sum(c * q for c, q in lines)
    tax = (Decimal(sub) * Decimal(str(rate))).quantize(Decimal(1), ROUND_HALF_UP)
    return sub + int(tax)
