from pricing import price


def write_invoice(office, ref, path):
    e, a, c = office.bookings[ref]
    t = price(e.price, a, c)
    with open(path, "w", encoding="utf8") as f:
        f.write(f"Event: {e.name}\n")
        f.write(f"Booking: {ref}\n")
        f.write(f"Tickets: {a} adult, {c} child\n")
        f.write(f"Total: {t // 100}.{t % 100:02d}\n")
