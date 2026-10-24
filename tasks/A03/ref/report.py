"""Reports."""
from collections import Counter

from charges import days, total


def revenue(rentals):
    return sum(total(rentals, i) for i in rentals.ids())


def busiest_car(rentals):
    c = Counter()
    for i in rentals.ids():
        c[rentals.get(i)[0]] += days(rentals, i)
    return min(c, key=lambda p: (-c[p], p)) if c else None
