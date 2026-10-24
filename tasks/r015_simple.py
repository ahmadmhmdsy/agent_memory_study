"""R-015 simple projects T01-T02: 4 sessions, 5 facts each."""
from r015_common import CHG, DEC, FINISH, RULE, later, mk

# ---------------------------------------------------------------- T01 shop cart
mk("T01", {"vat_rate": "superseded", "bulk_discount": "unfinished", "sku_case": "constraint",
           "qty_positive": "constraint", "remove_over": "decision"},
   "A shopping cart for a small web shop. Prices are in cents (ints).",
   {"cart.py": '"""Shopping cart."""\n', "price.py": '"""Cart prices."""\n'},
   [f"""
    Add a Cart class to cart.py with add(sku, qty), which adds qty items of sku, and count(sku), which returns how many items of sku the cart holds (0 for a sku it does not hold). Add tests.

    {RULE}SKUs are case-insensitive: "ab1" and "AB1" are the same SKU, and a SKU is always stored in upper case.

    {RULE}add with a quantity of 0 or less raises ValueError and changes nothing.

    {DEC}VAT is 20%.
    """,
    f"""
    Add total(cart, prices) to price.py: prices maps an upper-case SKU to its price in cents; the result is the sum of quantity times price, plus VAT, rounded to the nearest cent (an int). Add tests.

    {later("total", "a cart whose sum before VAT is 10000 cents or more gets 500 cents off that sum, before VAT is added.")}
    """,
    f"""
    Add Cart.remove(sku, qty), which takes qty items of sku out of the cart, and Cart.items(), the sorted list of (sku, quantity) pairs for every SKU the cart holds at least one of. Add tests.

    {DEC}removing more items than the cart holds removes all of that SKU: no error.

    {CHG}VAT is 15%, not 20%.
    """,
    f"""
    Add Cart.clear(), which empties the cart, and Cart.size(), the total number of items in the cart. Add tests. {FINISH}
    """],
   '''
   import pytest
   from cart import Cart
   from price import total


   def test_cart_basic():
       c = Cart()
       c.add("A1", 2)
       c.add("B2", 1)
       assert c.count("A1") == 2 and c.count("Z9") == 0 and c.size() == 3
       assert c.items() == [("A1", 2), ("B2", 1)]
       c.remove("A1", 1)
       assert c.count("A1") == 1
       c.clear()
       assert c.items() == [] and c.size() == 0


   def _one():
       c = Cart()
       c.add("A1", 1)
       return total(c, {"A1": 1000})


   def test_fact_vat_rate():
       assert _one() == 1150


   def test_stale_vat_20():
       assert _one() == 1200


   def test_fact_bulk_discount():
       c = Cart()
       c.add("A1", 10)
       assert total(c, {"A1": 1000}) == 10925
       c.remove("A1", 1)
       assert total(c, {"A1": 1000}) == 10350


   def test_fact_sku_case():
       c = Cart()
       c.add("ab1", 1)
       c.add("AB1", 2)
       assert c.count("Ab1") == 3 and c.items() == [("AB1", 3)]


   def test_fact_qty_positive():
       c = Cart()
       for q in (0, -1):
           with pytest.raises(ValueError):
               c.add("A1", q)
       assert c.items() == []


   def test_fact_remove_over():
       c = Cart()
       c.add("A1", 2)
       c.add("B2", 1)
       c.remove("A1", 5)
       assert c.count("A1") == 0 and c.items() == [("B2", 1)]
   ''',
   {"cart.py": '''
    """Shopping cart."""


    class Cart:
        def __init__(self):
            self._q = {}

        def add(self, sku, qty):
            if qty <= 0:
                raise ValueError("quantity must be positive")
            sku = sku.upper()
            self._q[sku] = self._q.get(sku, 0) + qty

        def count(self, sku):
            return self._q.get(sku.upper(), 0)

        def remove(self, sku, qty):
            sku = sku.upper()
            left = self._q.get(sku, 0) - qty
            if left > 0:
                self._q[sku] = left
            else:
                self._q.pop(sku, None)

        def items(self):
            return sorted(self._q.items())

        def clear(self):
            self._q.clear()

        def size(self):
            return sum(self._q.values())
    ''',
    "price.py": '''
    """Cart prices."""

    VAT = 15


    def total(cart, prices):
        s = sum(q * prices[k] for k, q in cart.items())
        if s >= 10000:
            s -= 500
        return (s * (100 + VAT) + 50) // 100
    '''}, "simple")

# ---------------------------------------------------------------- T02 timesheet
mk("T02", {"ot_threshold": "superseded", "report_sorted": "unfinished", "hours_range": "constraint",
           "name_trim": "decision", "quarter_round": "decision"},
   "Timesheets and pay for a small team.",
   {"timesheet.py": '"""Timesheets."""\n', "report.py": '"""Hours report."""\n'},
   [f"""
    Add a Timesheet class to timesheet.py with add(person, hours), which records hours worked by person, and hours(person), the total hours recorded for person (0 for someone with no entries). Add tests.

    {RULE}one entry is between 0 and 12 hours, inclusive; anything else raises ValueError and records nothing.

    {DEC}hours are rounded to the nearest quarter hour when they are added (1.1 becomes 1.0, 1.2 becomes 1.25).

    {DEC}overtime is every hour above 40.
    """,
    f"""
    Add overtime(ts, person) to timesheet.py: the hours of person above the overtime threshold (0 if none). Add pay(ts, person, rate) to timesheet.py: rate is cents per hour; normal hours are paid at rate and overtime hours at 1.5 times rate; the result is an int number of cents, rounded to the nearest cent. Add tests.

    {DEC}person names are trimmed of surrounding spaces: " ann " and "ann" are the same person.
    """,
    f"""
    Add report(ts) to report.py: a list of lines, one per person, each "name: hours", with hours as a number (for example "ann: 7.5"). Add Timesheet.people(), the sorted list of people with entries. Add tests.

    {later("report", "lines are ordered by hours, most first; people with equal hours are ordered by name.")}

    {CHG}overtime is every hour above 38, not 40.
    """,
    f"""
    Add Timesheet.reset(person), which removes every entry of person. Add tests. {FINISH}
    """],
   '''
   import pytest
   from timesheet import Timesheet, overtime, pay
   from report import report


   def test_basic():
       t = Timesheet()
       t.add("ann", 8)
       t.add("ann", 4)
       t.add("bob", 2)
       assert t.hours("ann") == 12 and t.hours("zed") == 0 and t.people() == ["ann", "bob"]
       assert overtime(t, "ann") == 0 and pay(t, "ann", 1000) == 12000
       t.reset("ann")
       assert t.hours("ann") == 0 and t.people() == ["bob"]


   def _forty():
       t = Timesheet()
       for _ in range(4):
           t.add("ann", 10)
       return t


   def test_fact_ot_threshold():
       t = _forty()
       assert overtime(t, "ann") == 2 and pay(t, "ann", 1000) == 38 * 1000 + 2 * 1500


   def test_stale_ot_40():
       assert overtime(_forty(), "ann") == 0


   def _num(line):
       return float(line.split(":")[1])


   def test_fact_report_sorted():
       t = Timesheet()
       t.add("cy", 2)
       t.add("bob", 5)
       t.add("al", 2)
       r = report(t)
       assert [x.split(":")[0].strip() for x in r] == ["bob", "al", "cy"] and _num(r[0]) == 5


   def test_fact_hours_range():
       t = Timesheet()
       t.add("ann", 12)
       t.add("ann", 0)
       for h in (12.5, -1):
           with pytest.raises(ValueError):
               t.add("ann", h)
       assert t.hours("ann") == 12


   def test_fact_name_trim():
       t = Timesheet()
       t.add(" ann ", 3)
       t.add("ann", 2)
       assert t.hours("ann") == 5 and t.hours("  ann") == 5 and t.people() == ["ann"]


   def test_fact_quarter_round():
       t = Timesheet()
       t.add("ann", 1.1)
       t.add("bob", 1.2)
       t.add("cy", 7.4)
       assert t.hours("ann") == 1.0 and t.hours("bob") == 1.25 and t.hours("cy") == 7.5
   ''',
   {"timesheet.py": '''
    """Timesheets."""

    THRESHOLD = 38


    class Timesheet:
        def __init__(self):
            self._h = {}

        def add(self, person, hours):
            if not 0 <= hours <= 12:
                raise ValueError("an entry is 0 to 12 hours")
            p = person.strip()
            self._h[p] = self._h.get(p, 0) + round(hours * 4) / 4

        def hours(self, person):
            return self._h.get(person.strip(), 0)

        def people(self):
            return sorted(self._h)

        def reset(self, person):
            self._h.pop(person.strip(), None)


    def overtime(ts, person):
        return max(0, ts.hours(person) - THRESHOLD)


    def pay(ts, person, rate):
        ot = overtime(ts, person)
        return round((ts.hours(person) - ot) * rate + ot * rate * 1.5)
    ''',
    "report.py": '''
    """Hours report."""


    def report(ts):
        rows = sorted(((-ts.hours(p), p) for p in ts.people()))
        return [f"{p}: {-h}" for h, p in rows]
    '''}, "simple")
