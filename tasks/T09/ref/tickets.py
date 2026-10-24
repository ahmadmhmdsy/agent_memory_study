"""Ticket prices."""

ROW_A = 4500
OTHER = 2500


def price(seat):
    return ROW_A if seat[0] == "A" else OTHER


def total(venue, name):
    held = venue.seats_of(name)
    s = sum(price(x) for x in held)
    if len(held) >= 4:
        s = s * 9 // 10
    return s
