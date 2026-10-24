"""R-015 advanced projects A01-A02: 20+ sessions, facts superseded up to twice (3 values),
unfinished steps that wait up to 21 sessions, and a history long enough to stress replay."""
from r015_common import CHG, DEC, FINISH, RULE, later, mk

# ---------------------------------------------------------------- A01 warehouse (22 sessions)
mk("A01", {"reorder_level": "superseded", "bulk_discount": "superseded", "date_format": "superseded",
           "tax_rate": "superseded", "max_stock": "superseded",
           "sku_strip": "unfinished", "export_sorted": "unfinished", "order_ids": "unfinished", "top_ties": "unfinished",
           "sku_case": "constraint", "no_negative": "constraint", "order_qty_positive": "constraint",
           "export_header": "decision", "cancel_restock": "decision", "shipping_fee": "decision"},
   "Stock, orders and prices for a small warehouse. Prices are in cents (ints); days are datetime.date.",
   {"stock.py": '"""Stock levels."""\n', "orders.py": '"""Customer orders."""\n',
    "pricing.py": '"""Order prices."""\n', "export.py": '"""CSV exports."""\n', "report.py": '"""Reports."""\n'},
   [f"""
    Add normalize_sku(s) to stock.py: it returns s in upper case; a result that is not 1 to 12 letters and digits raises ValueError. Add tests.

    {later("normalize_sku", 'hyphens and spaces are dropped first ("ab-12 3" becomes "AB123").')}

    {RULE}every SKU this project stores or compares goes through normalize_sku, so SKUs are case-insensitive and always stored in upper case.

    {DEC}a SKU needs reordering when its count is below 5.
    """,
    f"""
    Add a Stock class to stock.py with add(sku, n), which adds n items of sku, and count(sku), the number of items of sku (0 for a SKU never added). Add tests.

    {RULE}a SKU holds at most 500 items; an add that would go above that raises ValueError and changes nothing.
    """,
    f"""
    Add Stock.remove(sku, n), which takes n items of sku out of stock. Add tests.

    {RULE}stock never goes negative: taking out more items than the count raises ValueError and changes nothing.

    {DEC}an order line of 100 or more items gets a 5% bulk discount.
    """,
    f"""
    Add Stock.skus(): the sorted list of SKUs whose count is above 0. Add tests.

    {DEC}dates in files this project writes are written as DD/MM/YYYY.
    """,
    f"""
    Add price_line(qty, unit_cents) to pricing.py: qty times unit_cents, less any bulk discount, rounded to the nearest cent (an int). Add tests.

    {DEC}sales tax is 8%.
    """,
    f"""
    Add an Orders class to orders.py. Orders(stock) works on a Stock. place(sku, qty, day) takes qty items of sku out of the stock, records the order and returns its id: "O-" followed by a counter that starts at 1 ("O-1", "O-2", ...). Add tests.

    {later("Orders.place", 'the counter in an order id is zero-padded to 4 digits ("O-0001", "O-0002").')}

    {RULE}an order quantity is 1 or more; anything else raises ValueError and changes nothing.
    """,
    f"""
    Add Orders.get(oid), which returns the order as a tuple (sku, qty, day); an unknown id raises KeyError. Add tests.

    {DEC}every order total includes a shipping fee of 300 cents, added after tax; shipping is not taxed.
    """,
    f"""
    Add needs_reorder(stock) to stock.py: the sorted list of SKUs with a count above 0 that need reordering. Add tests.

    {CHG}a SKU needs reordering when its count is below 10, not 5.
    """,
    f"""
    Add export_stock(stock, path) to export.py: it writes a CSV file with one row per SKU whose count is above 0 (SKU, count), in the order the SKUs were first added. Add tests.

    {later("export_stock", "the rows are sorted by SKU instead.")}

    {DEC}an exported stock file starts with the header line sku,count and uses "," as the delimiter.
    """,
    f"""
    Add order_total(qty, unit_cents) to pricing.py: the price_line of the order, plus sales tax rounded to the nearest cent, plus any fees. Add tests.

    {CHG}the bulk discount is 10%, not 5%.
    """,
    f"""
    Add Orders.cancel(oid), which removes the order; an unknown id raises KeyError. Add tests.

    {DEC}cancelling an order puts its items back in stock.

    {CHG}a SKU holds at most 1000 items, not 500.
    """,
    f"""
    Add export_orders(orders, path) to export.py: it writes a CSV file that starts with the header line id,sku,qty,day and has one row per order, in the order they were placed. Add tests.

    {CHG}dates in files this project writes are ISO dates, YYYY-MM-DD, not DD/MM/YYYY.
    """,
    f"""
    Add top_skus(orders, n) to report.py: the n SKUs with the most items ordered over all orders, most first. Add tests.

    {later("top_skus", "SKUs with equal totals are ordered by SKU.")}
    """,
    f"""
    Add Stock.value(prices): the sum of count times price over the SKUs in stock; prices maps a SKU to its price in cents. Add tests.

    {CHG}sales tax is 6%, not 8%.
    """,
    """
    Add Orders.of_day(day): the ids of the orders placed on day, in the order they were placed. Add tests.
    """,
    f"""
    Add daily_items(orders) to report.py: a dict that maps each day to the total number of items ordered on that day. Add tests.

    {CHG}a SKU needs reordering when its count is below 8, not 10.
    """,
    """
    Add Orders.open_count(): the number of orders that are not cancelled. Add tests.
    """,
    f"""
    Add Orders.history(sku): the ids of the orders for sku, in the order they were placed. Add tests.

    {CHG}the bulk discount is 7%, not 10%.
    """,
    """
    Add Stock.rename(old, new), which moves the whole count of old to new; if new already has a count above 0 it raises ValueError and changes nothing. Add tests.
    """,
    f"""
    Add export_reorder(stock, path) to export.py: a CSV file with the header line sku,count and one row per SKU in needs_reorder(stock). Add tests.

    {CHG}dates in files this project writes are written as YYYYMMDD (for example 20260105), not YYYY-MM-DD.
    """,
    """
    Add low_stock_summary(stock) to report.py: the string "N SKUs need reordering", where N is the number of SKUs in needs_reorder(stock). Add tests.
    """,
    f"""
    Add Orders.total_items(): the total number of items over all orders that are not cancelled. Add tests. {FINISH}
    """],
   '''
   import datetime as dt
   import pytest
   from stock import Stock, normalize_sku, needs_reorder
   from orders import Orders
   from pricing import price_line, order_total
   from export import export_stock, export_orders
   from report import top_skus

   D = dt.date
   A, B, C = "AA1", "BB2", "CC3"


   def test_basic():
       s = Stock()
       s.add(A, 20)
       s.remove(A, 5)
       assert s.count(A) == 15 and s.count("ZZ9") == 0 and s.skus() == [A]
       o = Orders(s)
       oid = o.place(A, 3, D(2026, 1, 5))
       assert o.get(oid) == (A, 3, D(2026, 1, 5)) and s.count(A) == 12
       with pytest.raises(KeyError):
           o.get("nope")
       assert price_line(2, 150) == 300


   def _reorder():
       s = Stock()
       s.add(A, 9)
       s.add(B, 7)
       s.add(C, 8)
       return needs_reorder(s)


   def test_fact_reorder_level():
       assert _reorder() == [B]


   def test_stale_reorder_10():
       assert _reorder() == [A, B, C]


   def test_stale_reorder_5():
       assert _reorder() == []


   def test_fact_bulk_discount():
       assert price_line(100, 100) == 9300 and price_line(99, 100) == 9900


   def test_stale_bulk_10():
       assert price_line(100, 100) == 9000


   def test_stale_bulk_5():
       assert price_line(100, 100) == 9500


   def _day(tmp_path):
       s = Stock()
       s.add(A, 10)
       o = Orders(s)
       o.place(A, 2, D(2026, 1, 5))
       p = tmp_path / "o.csv"
       export_orders(o, str(p))
       rows = [x.rstrip("\\r") for x in p.read_text().splitlines() if x.strip()]
       return rows[-1].split(",")[-1].strip()


   def test_fact_date_format(tmp_path):
       assert _day(tmp_path) == "20260105"


   def test_stale_date_iso(tmp_path):
       assert _day(tmp_path) == "2026-01-05"


   def test_stale_date_dmy(tmp_path):
       assert _day(tmp_path) == "05/01/2026"


   def _tax():
       return order_total(10, 100) - order_total(5, 100)


   def test_fact_tax_rate():
       assert _tax() == 530


   def test_stale_tax_8():
       assert _tax() == 540


   def test_fact_shipping_fee():
       assert 2 * order_total(1, 5000) - order_total(2, 5000) == 300 and order_total(1, 5000) == 5600


   def test_fact_max_stock():
       s = Stock()
       s.add(A, 1000)
       with pytest.raises(ValueError):
           s.add(A, 1)
       assert s.count(A) == 1000


   def test_stale_max_500():
       s = Stock()
       with pytest.raises(ValueError):
           s.add(A, 600)


   def test_fact_sku_strip():
       assert normalize_sku("ab-12 3") == "AB123"
       with pytest.raises(ValueError):
           normalize_sku("a!b")
       s = Stock()
       s.add("aa-1", 2)
       assert s.count("AA1") == 2


   def test_fact_sku_case():
       s = Stock()
       s.add("aa1", 1)
       s.add("AA1", 2)
       assert s.count("Aa1") == 3 and s.skus() == [A]


   def _stock_rows(tmp_path):
       s = Stock()
       s.add(B, 1)
       s.add(A, 2)
       p = tmp_path / "s.csv"
       export_stock(s, str(p))
       return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


   def test_fact_export_header(tmp_path):
       assert _stock_rows(tmp_path)[0] == "sku,count"


   def test_fact_export_sorted(tmp_path):
       assert _stock_rows(tmp_path)[1:] == ["AA1,2", "BB2,1"]


   def test_fact_order_ids():
       s = Stock()
       s.add(A, 10)
       o = Orders(s)
       assert o.place(A, 1, D(2026, 1, 5)) == "O-0001" and o.place(A, 1, D(2026, 1, 5)) == "O-0002"


   def test_fact_top_ties():
       s = Stock()
       for k in (A, B, C):
           s.add(k, 20)
       o = Orders(s)
       o.place(B, 5, D(2026, 1, 5))
       o.place(A, 5, D(2026, 1, 5))
       o.place(C, 7, D(2026, 1, 6))
       assert top_skus(o, 3) == [C, A, B] and top_skus(o, 1) == [C]


   def test_fact_no_negative():
       s = Stock()
       s.add(A, 3)
       with pytest.raises(ValueError):
           s.remove(A, 4)
       with pytest.raises(ValueError):
           Orders(s).place(A, 4, D(2026, 1, 5))
       assert s.count(A) == 3


   def test_fact_order_qty_positive():
       s = Stock()
       s.add(A, 3)
       o = Orders(s)
       for q in (0, -1):
           with pytest.raises(ValueError):
               o.place(A, q, D(2026, 1, 5))
       assert s.count(A) == 3


   def test_fact_cancel_restock():
       s = Stock()
       s.add(A, 10)
       o = Orders(s)
       oid = o.place(A, 4, D(2026, 1, 5))
       o.cancel(oid)
       assert s.count(A) == 10
       with pytest.raises(KeyError):
           o.get(oid)
   ''',
   {"stock.py": '''
    """Stock levels."""
    import re

    REORDER_BELOW = 8
    MAX_ITEMS = 1000


    def normalize_sku(s):
        s = s.replace("-", "").replace(" ", "").upper()
        if not re.fullmatch(r"[A-Z0-9]{1,12}", s):
            raise ValueError(f"bad SKU {s!r}")
        return s


    class Stock:
        def __init__(self):
            self._c = {}

        def add(self, sku, n):
            sku = normalize_sku(sku)
            if self._c.get(sku, 0) + n > MAX_ITEMS:
                raise ValueError("too many items")
            self._c[sku] = self._c.get(sku, 0) + n

        def count(self, sku):
            return self._c.get(normalize_sku(sku), 0)

        def remove(self, sku, n):
            sku = normalize_sku(sku)
            if n > self._c.get(sku, 0):
                raise ValueError("not enough stock")
            self._c[sku] -= n

        def skus(self):
            return sorted(k for k, v in self._c.items() if v > 0)

        def value(self, prices):
            return sum(v * prices[k] for k, v in self._c.items() if v > 0)

        def rename(self, old, new):
            old, new = normalize_sku(old), normalize_sku(new)
            if self._c.get(new, 0) > 0:
                raise ValueError("target in stock")
            self._c[new] = self._c.pop(old, 0)


    def needs_reorder(stock):
        return [k for k in stock.skus() if stock.count(k) < REORDER_BELOW]
    ''',
    "orders.py": '''
    """Customer orders."""
    from stock import normalize_sku


    class Orders:
        def __init__(self, stock):
            self.stock = stock
            self._o = {}
            self._n = 0

        def place(self, sku, qty, day):
            if qty < 1:
                raise ValueError("quantity must be 1 or more")
            sku = normalize_sku(sku)
            self.stock.remove(sku, qty)
            self._n += 1
            oid = f"O-{self._n:04d}"
            self._o[oid] = (sku, qty, day)
            return oid

        def get(self, oid):
            return self._o[oid]

        def cancel(self, oid):
            sku, qty, _ = self._o.pop(oid)
            self.stock.add(sku, qty)

        def ids(self):
            return list(self._o)

        def of_day(self, day):
            return [k for k, v in self._o.items() if v[2] == day]

        def open_count(self):
            return len(self._o)

        def history(self, sku):
            sku = normalize_sku(sku)
            return [k for k, v in self._o.items() if v[0] == sku]

        def total_items(self):
            return sum(v[1] for v in self._o.values())
    ''',
    "pricing.py": '''
    """Order prices."""

    BULK = 7
    TAX = 6
    SHIPPING = 300


    def price_line(qty, unit_cents):
        s = qty * unit_cents
        if qty >= 100:
            return round(s * (100 - BULK) / 100)
        return s


    def order_total(qty, unit_cents):
        p = price_line(qty, unit_cents)
        return p + round(p * TAX / 100) + SHIPPING
    ''',
    "export.py": '''
    """CSV exports."""
    import csv

    from stock import needs_reorder


    def _write(path, header, rows):
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(rows)


    def export_stock(stock, path):
        _write(path, ["sku", "count"], [(k, stock.count(k)) for k in stock.skus()])


    def export_orders(orders, path):
        rows = []
        for oid in orders.ids():
            sku, qty, day = orders.get(oid)
            rows.append((oid, sku, qty, day.strftime("%Y%m%d")))
        _write(path, ["id", "sku", "qty", "day"], rows)


    def export_reorder(stock, path):
        _write(path, ["sku", "count"], [(k, stock.count(k)) for k in needs_reorder(stock)])
    ''',
    "report.py": '''
    """Reports."""
    from collections import Counter

    from stock import needs_reorder


    def top_skus(orders, n):
        c = Counter()
        for oid in orders.ids():
            sku, qty, _ = orders.get(oid)
            c[sku] += qty
        return [k for k, _ in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))][:n]


    def daily_items(orders):
        c = Counter()
        for oid in orders.ids():
            _, qty, day = orders.get(oid)
            c[day] += qty
        return dict(c)


    def low_stock_summary(stock):
        return f"{len(needs_reorder(stock))} SKUs need reordering"
    '''}, "advanced")

# ---------------------------------------------------------------- A02 hotel (20 sessions)
mk("A02", {"night_rate": "superseded", "cancel_fee": "superseded", "max_nights": "superseded",
           "weekend": "superseded",
           "room_code": "unfinished", "guest_title": "unfinished", "invoice_nights": "unfinished",
           "no_overlap": "constraint", "guest_required": "constraint", "checkout_after": "constraint",
           "checkout_free": "decision", "tourist_tax": "decision", "export_header": "decision"},
   "Rooms, bookings and bills for a small hotel. Money is in cents (ints); days are datetime.date. A booking from checkin to checkout covers the nights of checkin up to the day before checkout.",
   {"rooms.py": '"""Hotel rooms."""\n', "bookings.py": '"""Room bookings."""\n',
    "billing.py": '"""Prices and bills."""\n', "export.py": '"""CSV export."""\n'},
   [f"""
    Add code(number) to rooms.py: the code of room number, "R" followed by the number ("R7"). Add a Hotel class to rooms.py with add_room(number) and rooms(), the sorted list of room codes. Add tests.

    {later("code", 'the number in a room code is zero-padded to 3 digits ("R007", "R012").')}

    {DEC}a night in a room costs 9000 cents.
    """,
    f"""
    Add a Bookings class to bookings.py. Bookings(hotel) works on a Hotel. book(room, guest, checkin, checkout) books room (a room code) for guest and returns a booking id: an int counter that starts at 1. Add tests.

    {RULE}checkout must be after checkin; otherwise book raises ValueError and books nothing.

    {RULE}a guest name that is empty or only spaces raises ValueError and books nothing; names are stored without surrounding spaces.
    """,
    f"""
    Add Bookings.get(bid), which returns the booking as a tuple (room, guest, checkin, checkout); an unknown id raises KeyError. Add tests.

    {RULE}a booking is at most 14 nights; a longer one raises ValueError and books nothing.
    """,
    f"""
    Add Bookings.is_free(room, day): False when a booking of room covers the night of day, else True. Add tests.

    {RULE}a room is never booked twice for the same night: a booking that overlaps another booking of the same room raises ValueError and books nothing.

    {DEC}the checkout day is not a booked night, so a room can be booked from the day another booking of it checks out.
    """,
    f"""
    Add price(bookings, bid) to billing.py: the price of the booking's nights, in cents. Add tests.

    {DEC}cancelling a booking costs a fee of 10% of its price, rounded to the nearest cent.
    """,
    f"""
    Add Bookings.of_guest(guest): the ids of the bookings of guest, in id order. Add tests.

    {DEC}Friday and Saturday nights cost 20% more than other nights, rounded to the nearest cent.
    """,
    f"""
    Add Bookings.cancel(bid), which removes the booking and returns the cancellation fee in cents. Add bill(bookings, bid) to billing.py: what the guest pays for the booking. Add tests.

    {DEC}a tourist tax of 200 cents per night is added to every bill; the weekend price rule does not apply to it.
    """,
    f"""
    Add Bookings.guests(): the sorted list of distinct guest names over all bookings. Add tests.

    {later("Bookings.book", 'each guest name is stored in title case, so "ann LEE" becomes "Ann Lee".')}
    """,
    f"""
    Add export_bookings(bookings, path) to export.py: a CSV file with one row per booking in id order (id, room, guest, checkin, checkout), with ISO dates. Add tests.

    {DEC}an exported bookings file starts with the header line id,room,guest,in,out and uses "," as the delimiter.

    {CHG}a night in a room costs 9500 cents, not 9000.
    """,
    """
    Add Bookings.occupancy(day): the number of rooms booked for the night of day. Add tests.
    """,
    f"""
    Add invoice(bookings, bid) to billing.py: a list of text lines for the booking; for now it has one line, "total: <cents>", where <cents> is the bill. Add tests.

    {later("invoice", 'before the total line it has one line per night, in date order, "YYYY-MM-DD: <cents>", where <cents> is the room price of that night.')}

    {CHG}a booking is at most 21 nights, not 14.
    """,
    f"""
    Add Bookings.extend(bid, checkout), which moves the checkout of a booking to a later day; the booking rules still apply, and a broken rule raises ValueError and changes nothing. Add tests.

    {CHG}the cancellation fee is 25% of the price, not 10%.
    """,
    """
    Add Hotel.remove_room(code), which removes a room from the hotel. Add tests.
    """,
    f"""
    Add Bookings.nights_booked(room): the total number of nights booked for room. Add tests.

    {CHG}only Saturday nights cost 20% more; Friday nights cost the same as other nights.
    """,
    """
    Add revenue(bookings) to billing.py: the sum of the bills of all bookings. Add tests.
    """,
    """
    Add Bookings.find(text): the ids of the bookings whose guest name contains text, ignoring case, in id order. Add tests.
    """,
    f"""
    Add Bookings.ids(): all booking ids in order. Add tests.

    {CHG}a night in a room costs 9900 cents, not 9500.
    """,
    f"""
    Add Bookings.move(bid, room), which moves a booking to another room; the booking rules still apply, and a broken rule raises ValueError and changes nothing. Add tests.

    {CHG}the cancellation fee is 20% of the price, not 25%.
    """,
    f"""
    Add Bookings.guest_nights(guest): the total number of nights booked by guest. Add tests.

    {CHG}a booking is at most 28 nights, not 21.
    """,
    f"""
    Add busiest_day(bookings) to billing.py: the day with the most rooms booked for its night, the earliest one on a tie, or None when there are no bookings. Add tests. {FINISH}
    """],
   '''
   import datetime as dt
   import pytest
   from rooms import Hotel, code
   from bookings import Bookings
   from billing import price, bill, invoice
   from export import export_bookings

   D = dt.date
   MON, WED, FRI, SAT, SUN = D(2026, 1, 5), D(2026, 1, 7), D(2026, 1, 9), D(2026, 1, 10), D(2026, 1, 11)


   def _b():
       h = Hotel()
       for n in (1, 2):
           h.add_room(n)
       return Bookings(h)


   def test_basic():
       b = _b()
       r = code(1)
       i = b.book(r, "Ann", MON, WED)
       assert b.get(i)[0] == r and b.get(i)[2:] == (MON, WED)
       assert not b.is_free(r, MON) and b.is_free(code(2), MON) and b.is_free(r, D(2026, 1, 4))
       with pytest.raises(KeyError):
           b.get(999)


   def _one_night():
       b = _b()
       i = b.book(code(1), "Ann", MON, MON + dt.timedelta(1))
       return b, i


   def test_fact_night_rate():
       b, i = _one_night()
       assert price(b, i) == 9900


   def test_stale_rate_9500():
       b, i = _one_night()
       assert price(b, i) == 9500


   def test_stale_rate_9000():
       b, i = _one_night()
       assert price(b, i) == 9000


   def _weekend():
       b = _b()
       i = b.book(code(1), "Ann", FRI, SUN)
       return b, i


   def test_fact_weekend():
       b, i = _weekend()
       assert price(b, i) == 9900 + 11880


   def test_stale_weekend_friday():
       b, i = _weekend()
       assert price(b, i) == 2 * 11880


   def test_fact_tourist_tax():
       b, i = _weekend()
       assert bill(b, i) == 9900 + 11880 + 400


   def _fee():
       b, i = _one_night()
       return b.cancel(i)


   def test_fact_cancel_fee():
       assert _fee() == 1980


   def test_stale_cancel_25():
       assert _fee() == 2475


   def test_stale_cancel_10():
       assert _fee() == 990


   def _nights_ok(n):
       b = _b()
       try:
           b.book(code(1), "Ann", MON, MON + dt.timedelta(n))
           return True
       except ValueError:
           return False


   def test_fact_max_nights():
       assert _nights_ok(28) and not _nights_ok(29)


   def test_stale_nights_21():
       assert not _nights_ok(22)


   def test_stale_nights_14():
       assert not _nights_ok(15)


   def test_fact_room_code():
       h = Hotel()
       h.add_room(12)
       h.add_room(7)
       assert code(7) == "R007" and h.rooms() == ["R007", "R012"]


   def test_fact_guest_title():
       b = _b()
       i = b.book(code(1), "  ann LEE ", MON, WED)
       assert b.get(i)[1] == "Ann Lee" and b.guests() == ["Ann Lee"]


   def test_fact_invoice_nights():
       b = _b()
       i = b.book(code(1), "Ann", MON, WED)
       inv = [x.strip() for x in invoice(b, i)]
       assert inv == ["2026-01-05: 9900", "2026-01-06: 9900", "total: 20200"]


   def test_fact_no_overlap():
       b = _b()
       b.book(code(1), "Ann", MON, D(2026, 1, 8))
       with pytest.raises(ValueError):
           b.book(code(1), "Bob", WED, FRI)
       assert b.guests() == ["Ann"] and b.book(code(2), "Bob", WED, FRI) == 2


   def test_fact_guest_required():
       b = _b()
       for g in ("", "   "):
           with pytest.raises(ValueError):
               b.book(code(1), g, MON, WED)
       assert b.is_free(code(1), MON)


   def test_fact_checkout_after():
       b = _b()
       for out in (MON, D(2026, 1, 4)):
           with pytest.raises(ValueError):
               b.book(code(1), "Ann", MON, out)
       assert b.is_free(code(1), MON)


   def test_fact_checkout_free():
       b = _b()
       b.book(code(1), "Ann", MON, WED)
       assert b.is_free(code(1), WED)
       b.book(code(1), "Bob", WED, FRI)
       assert not b.is_free(code(1), WED)


   def test_fact_export_header(tmp_path):
       b = _b()
       b.book(code(1), "Ann", MON, WED)
       p = tmp_path / "b.csv"
       export_bookings(b, str(p))
       rows = [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]
       assert rows[0] == "id,room,guest,in,out" and rows[1].split(",")[0] == "1"
   ''',
   {"rooms.py": '''
    """Hotel rooms."""


    def code(number):
        return f"R{number:03d}"


    class Hotel:
        def __init__(self):
            self._r = set()

        def add_room(self, number):
            self._r.add(code(number))

        def rooms(self):
            return sorted(self._r)

        def remove_room(self, c):
            self._r.discard(c)
    ''',
    "bookings.py": '''
    """Room bookings."""

    MAX_NIGHTS = 28
    CANCEL_FEE = 20


    class Bookings:
        def __init__(self, hotel):
            self.hotel = hotel
            self._b = {}
            self._n = 0

        def _check(self, room, guest, checkin, checkout, skip=None):
            if not guest:
                raise ValueError("guest name required")
            if checkout <= checkin:
                raise ValueError("checkout must be after checkin")
            if (checkout - checkin).days > MAX_NIGHTS:
                raise ValueError("too many nights")
            for k, (r, _, a, b) in self._b.items():
                if k != skip and r == room and checkin < b and a < checkout:
                    raise ValueError("room already booked")

        def book(self, room, guest, checkin, checkout):
            guest = guest.strip().title()
            self._check(room, guest, checkin, checkout)
            self._n += 1
            self._b[self._n] = (room, guest, checkin, checkout)
            return self._n

        def get(self, bid):
            return self._b[bid]

        def ids(self):
            return list(self._b)

        def is_free(self, room, day):
            return not any(r == room and a <= day < b for r, _, a, b in self._b.values())

        def of_guest(self, guest):
            return [k for k, v in self._b.items() if v[1] == guest.strip().title()]

        def cancel(self, bid):
            from billing import price
            fee = round(price(self, bid) * CANCEL_FEE / 100)
            del self._b[bid]
            return fee

        def guests(self):
            return sorted({v[1] for v in self._b.values()})

        def occupancy(self, day):
            return sum(a <= day < b for _, _, a, b in self._b.values())

        def extend(self, bid, checkout):
            r, g, a, _ = self._b[bid]
            self._check(r, g, a, checkout, skip=bid)
            self._b[bid] = (r, g, a, checkout)

        def move(self, bid, room):
            _, g, a, b = self._b[bid]
            self._check(room, g, a, b, skip=bid)
            self._b[bid] = (room, g, a, b)

        def nights_booked(self, room):
            return sum((b - a).days for r, _, a, b in self._b.values() if r == room)

        def guest_nights(self, guest):
            return sum((v[3] - v[2]).days for v in self._b.values() if v[1] == guest.strip().title())

        def find(self, text):
            return [k for k, v in self._b.items() if text.lower() in v[1].lower()]
    ''',
    "billing.py": '''
    """Prices and bills."""
    import datetime as dt
    from collections import Counter

    RATE = 9900
    TOURIST_TAX = 200


    def night_price(day):
        return round(RATE * 1.2) if day.weekday() == 5 else RATE


    def nights(booking):
        _, _, a, b = booking
        return [a + dt.timedelta(i) for i in range((b - a).days)]


    def price(bookings, bid):
        return sum(night_price(d) for d in nights(bookings.get(bid)))


    def bill(bookings, bid):
        return price(bookings, bid) + TOURIST_TAX * len(nights(bookings.get(bid)))


    def invoice(bookings, bid):
        lines = [f"{d.isoformat()}: {night_price(d)}" for d in nights(bookings.get(bid))]
        return lines + [f"total: {bill(bookings, bid)}"]


    def revenue(bookings):
        return sum(bill(bookings, i) for i in bookings.ids())


    def busiest_day(bookings):
        c = Counter(d for i in bookings.ids() for d in nights(bookings.get(i)))
        return min(c, key=lambda d: (-c[d], d)) if c else None
    ''',
    "export.py": '''
    """CSV export."""
    import csv


    def export_bookings(bookings, path):
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "room", "guest", "in", "out"])
            for i in bookings.ids():
                r, g, a, b = bookings.get(i)
                w.writerow([i, r, g, a.isoformat(), b.isoformat()])
    '''}, "advanced")
