"""Guest bills."""

RATE = 9900


def bill(hotel, guest):
    return sum((n - n // 7) * RATE for _, _, n in hotel.bookings(guest))
