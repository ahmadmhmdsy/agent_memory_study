from decimal import Decimal, ROUND_HALF_UP


def grade(percent):
    p = int(Decimal(str(percent)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    return "A" if p >= 90 else "B" if p >= 75 else "C" if p >= 60 else "F"
