from datetime import timedelta


def stay_price(hotel, bid):
    g, r, s, e = hotel.bookings[bid]
    price = hotel.rooms[r][1]
    total = 0
    d = s
    while d < e:
        total += (price + price * 25 // 100) if d.weekday() in (4, 5) else price
        d += timedelta(days=1)
    if (e - s).days >= 7:
        total = total * 90 // 100
    return total
