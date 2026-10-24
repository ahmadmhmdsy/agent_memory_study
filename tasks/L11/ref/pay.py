from fractions import Fraction
import math


def weekly_pay(sheet, worker, rate):
    m = sheet.minutes(worker)
    reg = min(m, 38 * 60)
    ot = m - reg
    x = Fraction(reg * rate, 60) + Fraction(ot * rate * 5, 240)
    return math.floor(x + Fraction(1, 2))
