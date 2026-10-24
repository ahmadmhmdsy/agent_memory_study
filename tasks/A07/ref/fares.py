"""Fares and fees."""

WINDOW = 1500
CHILD = 60
FREE_KG = 25
EXCESS = 1200
CHANGE = 6000


def fare(bookings, bid):
    code, _, age, seat = bookings.get(bid)
    f = bookings.flights.fare(code)
    if age < 12:
        f = round(f * CHILD / 100)
    if seat[-1] in "AF":
        f += WINDOW
    return f


def bag_fee(bookings, bid):
    return sum(max(0, kg - FREE_KG) * EXCESS for kg in bookings.bags(bid))


def total(bookings, bid):
    return fare(bookings, bid) + bag_fee(bookings, bid) + bookings.changes(bid) * CHANGE


def revenue(bookings, code):
    return sum(total(bookings, b) for b in bookings.of_flight(code))
