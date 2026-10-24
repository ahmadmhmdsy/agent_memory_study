from price import stay_price


def write_confirmation(hotel, bid, path):
    g, r, s, e = hotel.bookings[bid]
    with open(path, "w", encoding="utf8") as f:
        f.write(f"Booking #{bid}\n")
        f.write(f"Guest: {g.title()}\n")
        f.write(f"{(e - s).days} nights in room {r}\n")
        f.write(f"Total: {stay_price(hotel, bid) / 100:.2f}\n")
