"""R-014 scored projects L09-L11 (v3 form: 8 sessions, 12 facts)."""
from long_common import CHG, DEC, FINISH, RULE, g, later, mk

# ---------------------------------------------------------------- L09 recipe scaler
mk("L09", {"cup_250": "superseded", "round_quarter": "superseded", "line_format": "superseded",
           "parse_mixed": "unfinished", "unit_names": "unfinished", "title_small": "unfinished",
           "positive_qty": "constraint", "name_lower": "constraint", "dup_merge": "decision",
           "remove_bool": "decision", "max_factor": "decision", "card_serves": "decision"},
   "Recipe helpers: quantities, scaling and recipe cards.",
   {"units.py": '"""Quantities and units."""\n', "recipe.py": '"""Recipes."""\n',
    "scale.py": '"""Recipe scaling."""\n', "card.py": '"""Recipe cards."""\n'},
   [f"""
    Add parse_qty(s) to units.py: a quantity string becomes a float ("2" becomes 2.0, "1/2" becomes 0.5). Add tests.

    {later("parse_qty", 'it also accepts a mixed number such as "1 1/2", which becomes 1.5.')}

    {RULE}a quantity must be positive: any function given a quantity of zero or less raises ValueError.

    {DEC}a cup is 240 ml in every conversion.
    """,
    f"""
    Add a Recipe class to recipe.py: Recipe(name, servings) keeps name and servings as attributes; add(name, qty, unit) adds an ingredient, and items() returns the ingredients as a list of (name, qty, unit) tuples in the order they were added. Add tests.

    {RULE}ingredient names are stored in lower case with leading and trailing spaces removed, and every function that takes an ingredient name treats it the same way.

    {DEC}scaled quantities are rounded to 1 decimal place.

    {DEC}each ingredient line of a recipe card has the form 200 g flour.
    """,
    f"""
    Add Recipe.remove(name) to recipe.py: it removes that ingredient. Add tests.

    {CHG}scaled quantities are rounded to the nearest 0.25, not to 1 decimal place.

    {DEC}adding an ingredient that is already in the recipe with the same unit adds to its quantity; with a different unit it raises ValueError and changes nothing.

    {DEC}Recipe.remove returns True when it removed the ingredient and False when the ingredient was not in the recipe.
    """,
    f"""
    Add to_ml(qty, unit) to units.py: it converts a quantity in "ml", "tsp" (5 ml), "tbsp" (15 ml) or "cup" to millilitres. Add tests.

    {later("to_ml", 'unit names ignore case and a trailing "s" ("Tbsps" is the same as "tbsp").')}

    {CHG}a cup is 250 ml in every conversion, not 240.
    """,
    f"""
    Add title(name) to card.py: each word of a recipe name starts with a capital letter ("chocolate cake" becomes "Chocolate Cake"). Add tests.

    {later("title", 'the small words "and", "of" and "with" stay in lower case unless they are the first word ("fish and chips" becomes "Fish and Chips").')}
    """,
    f"""
    Add Recipe.count() to recipe.py: the number of ingredients. Add tests.

    {CHG}each ingredient line of a recipe card has the form flour: 200 g, not 200 g flour.

    {DEC}scaling to fewer than 1 serving or to more than 10 times the recipe's servings raises ValueError.

    {DEC}the first line of a recipe card is the title (from title()) followed by the servings, in the form Pancakes (serves 4).
    """,
    """
    Add scale(recipe, servings) to scale.py: it returns a new Recipe with the same name, the new servings, and each quantity multiplied by servings / recipe.servings. Add tests.
    """,
    f"""
    Add write_card(recipe, path) to card.py: it writes a text recipe card with a title line and one line per ingredient. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_qty(s) with tests. Its last step is left for later: accept a mixed number such as \"1 1/2\".",
      [("parse_qty", "done"), ("parse_qty: accept mixed numbers", "todo")],
      ["A quantity must be positive: a quantity of zero or less raises ValueError in any function.",
       "A cup is 240 ml in every conversion."]),
    g("Session 2 added Recipe(name, servings) with add and items, with tests.", [("Recipe.add / Recipe.items", "done")],
      ["Ingredient names are stored lower case without outer spaces; every function treats names the same way.",
       "Scaled quantities are rounded to 1 decimal place.",
       "A recipe card ingredient line has the form 200 g flour."]),
    g("Session 3 added Recipe.remove(name) with tests.", [("Recipe.remove", "done")],
      ["Supersedes 1 decimal place: scaled quantities are rounded to the nearest 0.25.",
       "Adding an existing ingredient with the same unit adds to its quantity; a different unit raises ValueError and changes nothing.",
       "Recipe.remove returns True when it removed the ingredient, False when it was not there."]),
    g("Session 4 added to_ml(qty, unit) with tests. Its last step is left for later: unit names ignore case and a trailing \"s\".",
      [("to_ml", "done"), ("to_ml: ignore case and a trailing s", "todo")],
      ["Supersedes 240 ml: a cup is 250 ml in every conversion."]),
    g("Session 5 added title(name) with tests. Its last step is left for later: \"and\", \"of\", \"with\" stay lower case unless first.",
      [("title", "done"), ("title: small words stay lower case", "todo")]),
    g("Session 6 added Recipe.count() with tests.", [("Recipe.count", "done")],
      ["Supersedes 200 g flour: a recipe card ingredient line has the form flour: 200 g.",
       "Scaling to fewer than 1 serving or more than 10 times the servings raises ValueError.",
       "The first line of a recipe card is the title then the servings: Pancakes (serves 4)."]),
    g("Session 7 added scale(recipe, servings) with tests.", [("scale", "done")])],
   '''
   import re
   import pytest
   from units import parse_qty, to_ml
   from recipe import Recipe
   from scale import scale
   from card import title, write_card


   def test_recipe_basic():
       r = Recipe("pancakes", 2)
       r.add("flour", 100, "g")
       r.add("milk", 200, "ml")
       assert r.items() == [("flour", 100, "g"), ("milk", 200, "ml")] and r.count() == 2
       s = scale(r, 4)
       assert s.servings == 4 and s.name == "pancakes" and s.items()[0] == ("flour", 200, "g")
       assert parse_qty("1/2") == 0.5 and to_ml(2, "tbsp") == 30 and title("chocolate cake") == "Chocolate Cake"


   def test_fact_cup_250():
       assert to_ml(2, "cup") == 500


   def test_stale_cup_240():
       assert to_ml(2, "cup") == 480


   def test_fact_round_quarter():
       r = Recipe("x", 3)
       r.add("flour", 1, "cup")
       assert scale(r, 2).items() == [("flour", 0.75, "cup")]


   def test_stale_round_decimal():
       r = Recipe("x", 3)
       r.add("flour", 1, "cup")
       assert scale(r, 2).items() == [("flour", 0.7, "cup")]


   def _card(tmp_path):
       r = Recipe("pancakes", 4)
       r.add("flour", 200, "g")
       r.add("milk", 300, "ml")
       p = tmp_path / "card.txt"
       write_card(r, str(p))
       return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def test_fact_line_format(tmp_path):
       assert any(re.fullmatch(r"flour: 200(\\.0+)? g", x) for x in _card(tmp_path))


   def test_stale_line_qty_first(tmp_path):
       assert any(re.fullmatch(r"200(\\.0+)? g flour", x) for x in _card(tmp_path))


   def test_fact_card_serves(tmp_path):
       assert _card(tmp_path)[0] == "Pancakes (serves 4)"


   def test_fact_parse_mixed():
       assert parse_qty("1 1/2") == 1.5 and parse_qty("2") == 2.0


   def test_fact_unit_names():
       assert to_ml(2, "Tbsps") == 30 and to_ml(1, "TSP") == 5


   def test_fact_title_small():
       assert title("fish and chips") == "Fish and Chips" and title("of mice") == "Of Mice"


   def test_fact_positive_qty():
       for bad in ("0", "-1"):
           with pytest.raises(ValueError):
               parse_qty(bad)
       r = Recipe("x", 2)
       with pytest.raises(ValueError):
           r.add("salt", 0, "g")
       assert r.items() == []


   def test_fact_name_lower():
       r = Recipe("x", 2)
       r.add(" Flour ", 100, "g")
       assert r.items() == [("flour", 100, "g")]
       r.remove("FLOUR")
       assert r.items() == []


   def test_fact_dup_merge():
       r = Recipe("x", 2)
       r.add("flour", 100, "g")
       r.add("flour", 50, "g")
       assert r.items() == [("flour", 150, "g")]
       with pytest.raises(ValueError):
           r.add("flour", 1, "cup")
       assert r.items() == [("flour", 150, "g")]


   def test_fact_remove_bool():
       r = Recipe("x", 2)
       r.add("salt", 5, "g")
       assert r.remove("sugar") is False and r.remove("salt") is True and r.items() == []


   def test_fact_max_factor():
       r = Recipe("x", 2)
       r.add("flour", 100, "g")
       for bad in (21, 0):
           with pytest.raises(ValueError):
               scale(r, bad)
       assert scale(r, 20).items() == [("flour", 1000, "g")]
   ''',
   {"units.py": '''
    ML = {"ml": 1, "tsp": 5, "tbsp": 15, "cup": 250}


    def parse_qty(s):
        total = 0.0
        for p in s.split():
            if "/" in p:
                a, b = p.split("/")
                total += float(a) / float(b)
            else:
                total += float(p)
        if total <= 0:
            raise ValueError("quantity must be positive")
        return total


    def to_ml(qty, unit):
        if qty <= 0:
            raise ValueError("quantity must be positive")
        u = unit.strip().lower()
        if u not in ML and u.endswith("s"):
            u = u[:-1]
        if u not in ML:
            raise ValueError("unknown unit")
        return qty * ML[u]
    ''',
    "recipe.py": '''
    class Recipe:
        def __init__(self, name, servings):
            self.name = name
            self.servings = servings
            self._items = []

        def add(self, name, qty, unit):
            if qty <= 0:
                raise ValueError("quantity must be positive")
            name = name.strip().lower()
            for i, (n, q, u) in enumerate(self._items):
                if n == name:
                    if u != unit:
                        raise ValueError("unit mismatch")
                    self._items[i] = (n, q + qty, u)
                    return
            self._items.append((name, qty, unit))

        def items(self):
            return list(self._items)

        def remove(self, name):
            name = name.strip().lower()
            for i, (n, _, _) in enumerate(self._items):
                if n == name:
                    del self._items[i]
                    return True
            return False

        def count(self):
            return len(self._items)
    ''',
    "scale.py": '''
    from recipe import Recipe


    def scale(recipe, servings):
        if servings < 1 or servings > 10 * recipe.servings:
            raise ValueError("bad servings")
        out = Recipe(recipe.name, servings)
        f = servings / recipe.servings
        for n, q, u in recipe.items():
            out.add(n, round(q * f * 4) / 4, u)
        return out
    ''',
    "card.py": '''
    SMALL = {"and", "of", "with"}


    def title(name):
        words = name.split()
        return " ".join(w.lower() if i and w.lower() in SMALL else w.capitalize() for i, w in enumerate(words))


    def _num(q):
        return str(int(q)) if float(q).is_integer() else str(q)


    def write_card(recipe, path):
        with open(path, "w", encoding="utf8") as f:
            f.write(f"{title(recipe.name)} (serves {recipe.servings})\\n")
            for n, q, u in recipe.items():
                f.write(f"{n}: {_num(q)} {u}\\n")
    '''})

# ---------------------------------------------------------------- L10 event tickets
mk("L10", {"child_40": "superseded", "fee_ticket": "superseded", "ref_format": "superseded",
           "parse_dmy": "unfinished", "upcoming_sorted": "unfinished", "slug_clean": "unfinished",
           "past_event": "constraint", "capacity": "constraint", "max_6": "decision",
           "no_empty": "decision", "cancel_unknown": "decision", "invoice_event": "decision"},
   "Ticket helpers for a small event venue. Prices are int cents.",
   {"events.py": '"""Events."""\n', "booking.py": '"""Bookings."""\n',
    "pricing.py": '"""Ticket prices."""\n', "invoice.py": '"""Invoices."""\n'},
   [f"""
    Add parse_date(s) to events.py: a date string such as "2026-03-05" becomes datetime.date(2026, 3, 5). Add tests.

    {later("parse_date", 'it also accepts day.month.year dates such as "05.03.2026".')}

    {RULE}nothing can be booked for an event whose date is before the booking day: such a booking raises ValueError and books nothing.

    {DEC}a child ticket costs half the adult price, rounded down to a whole cent.
    """,
    f"""
    Add an Event class to events.py: Event(name, date, capacity, price), where price is the adult ticket price in cents, with seats_left(). Add an Office class to booking.py with book(event, adults, children, today), which records a booking, takes its seats and returns the booking reference. Add tests.

    {RULE}an event never sells more seats than its capacity: a booking with more tickets than the seats left raises ValueError and books nothing.

    {DEC}each order pays a booking fee of 100 cents.

    {DEC}booking references are "B-1", "B-2" and so on, in the order the bookings were made.
    """,
    f"""
    Add Office.count() to booking.py: the number of bookings. Add tests.

    {CHG}the booking fee is 50 cents for each ticket, not 100 cents per order.

    {DEC}one booking has at most 6 tickets (adults plus children); a larger booking raises ValueError and books nothing.

    {DEC}a booking with no tickets raises ValueError.
    """,
    f"""
    Add upcoming(events, today) to events.py: the names of the events dated today or later. Add tests.

    {later("upcoming", "the names must be sorted by event date, earliest first, with ties sorted by name.")}

    {CHG}a child ticket costs 40% of the adult price, rounded down to a whole cent, not half.
    """,
    f"""
    Add slug(name) to events.py: an event name in lower case with spaces replaced by hyphens ("Summer Fest" becomes "summer-fest"). Add tests.

    {later("slug", 'punctuation is removed and runs of hyphens become one ("Rock & Roll!" becomes "rock-roll").')}
    """,
    f"""
    Add Office.cancel(ref) to booking.py: it removes that booking and frees its seats. Add tests.

    {CHG}booking references are "B00001", "B00002" and so on (B and 5 digits), not "B-1".

    {DEC}Office.cancel returns True when it cancelled a booking; for an unknown reference it returns False and changes nothing.

    {DEC}the first line of an invoice is the event name in the form Event: Summer Fest.
    """,
    """
    Add price(adult_cents, adults, children) to pricing.py: the total in cents (an int) of an order, booking fees included. Add tests.
    """,
    f"""
    Add write_invoice(office, ref, path) to invoice.py: it writes a text invoice for that booking with the event name, the booking reference, the number of tickets and the total. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_date(s) with tests. Its last step is left for later: accept day.month.year dates such as \"05.03.2026\".",
      [("parse_date", "done"), ("parse_date: accept day.month.year", "todo")],
      ["A booking for an event dated before the booking day raises ValueError and books nothing.",
       "A child ticket costs half the adult price, rounded down to a whole cent."]),
    g("Session 2 added Event(name, date, capacity, price) with seats_left, and Office.book, with tests.",
      [("Event / seats_left", "done"), ("Office.book", "done")],
      ["A booking with more tickets than the seats left raises ValueError and books nothing.",
       "Each order pays a booking fee of 100 cents.",
       "Booking references are \"B-1\", \"B-2\" and so on, in booking order."]),
    g("Session 3 added Office.count() with tests.", [("Office.count", "done")],
      ["Supersedes 100 cents per order: the booking fee is 50 cents per ticket.",
       "One booking has at most 6 tickets; a larger one raises ValueError and books nothing.",
       "A booking with no tickets raises ValueError."]),
    g("Session 4 added upcoming(events, today) with tests. Its last step is left for later: sort by date, ties by name.",
      [("upcoming", "done"), ("upcoming: sort by date, ties by name", "todo")],
      ["Supersedes half price: a child ticket costs 40% of the adult price, rounded down to a whole cent."]),
    g("Session 5 added slug(name) with tests. Its last step is left for later: remove punctuation and collapse hyphens.",
      [("slug", "done"), ("slug: remove punctuation, collapse hyphens", "todo")]),
    g("Session 6 added Office.cancel(ref) with tests.", [("Office.cancel", "done")],
      ["Supersedes \"B-1\": booking references are \"B00001\", \"B00002\" and so on.",
       "Office.cancel returns True when it cancelled; an unknown reference returns False and changes nothing.",
       "The first invoice line is the event name: Event: Summer Fest."]),
    g("Session 7 added price(adult_cents, adults, children) with tests.", [("price", "done")])],
   '''
   from datetime import date
   import pytest
   from events import Event, parse_date, slug, upcoming
   from booking import Office
   from pricing import price
   from invoice import write_invoice

   D = date(2026, 6, 1)


   def _event(cap=20):
       return Event("Summer Fest", date(2026, 7, 1), cap, 1000)


   def test_event_basic():
       e = _event(10)
       o = Office()
       o.book(e, 2, 1, D)
       assert e.seats_left() == 7 and o.count() == 1
       assert parse_date("2026-03-05") == date(2026, 3, 5) and slug("Summer Fest") == "summer-fest"
       assert upcoming([e], D) == ["Summer Fest"]


   def test_fact_child_40():
       assert price(1000, 0, 2) - price(1000, 2, 0) == -1200


   def test_stale_child_half():
       assert price(1000, 0, 2) - price(1000, 2, 0) == -1000


   def test_fact_fee_ticket():
       assert price(1000, 3, 0) == 3150


   def test_stale_fee_order():
       assert price(1000, 3, 0) == 3100


   def _refs():
       e = _event()
       o = Office()
       return [o.book(e, 1, 0, D), o.book(e, 2, 0, D)]


   def test_fact_ref_format():
       assert _refs() == ["B00001", "B00002"]


   def test_stale_ref_dash():
       assert _refs()[0] == "B-1"


   def test_fact_parse_dmy():
       assert parse_date("05.03.2026") == date(2026, 3, 5) and parse_date("2026-03-05") == date(2026, 3, 5)


   def test_fact_upcoming_sorted():
       evs = [Event("Zed", date(2026, 7, 1), 5, 100), Event("Mid", date(2026, 6, 15), 5, 100),
              Event("Old", date(2026, 5, 1), 5, 100), Event("Alp", date(2026, 7, 1), 5, 100)]
       assert upcoming(evs, D) == ["Mid", "Alp", "Zed"]


   def test_fact_slug_clean():
       assert slug("Rock & Roll!") == "rock-roll" and slug("  Jazz   Night ") == "jazz-night"


   def test_fact_past_event():
       e = Event("A", date(2026, 1, 1), 10, 1000)
       o = Office()
       with pytest.raises(ValueError):
           o.book(e, 1, 0, date(2026, 1, 2))
       o.book(e, 1, 0, date(2026, 1, 1))
       assert e.seats_left() == 9 and o.count() == 1


   def test_fact_capacity():
       e = _event(3)
       o = Office()
       o.book(e, 2, 0, D)
       with pytest.raises(ValueError):
           o.book(e, 2, 0, D)
       assert e.seats_left() == 1 and o.count() == 1


   def test_fact_max_6():
       e = _event()
       o = Office()
       with pytest.raises(ValueError):
           o.book(e, 4, 3, D)
       o.book(e, 4, 2, D)
       assert e.seats_left() == 14


   def test_fact_no_empty():
       e = _event()
       o = Office()
       with pytest.raises(ValueError):
           o.book(e, 0, 0, D)
       assert o.count() == 0


   def test_fact_cancel_unknown():
       e = _event()
       o = Office()
       r = o.book(e, 2, 0, D)
       assert o.cancel("nope") is False and e.seats_left() == 18
       assert o.cancel(r) is True and e.seats_left() == 20 and o.count() == 0


   def test_fact_invoice_event(tmp_path):
       e = _event()
       o = Office()
       r = o.book(e, 1, 1, D)
       p = tmp_path / "inv.txt"
       write_invoice(o, r, str(p))
       lines = [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]
       assert lines[0] == "Event: Summer Fest"
   ''',
   {"events.py": '''
    import re
    from datetime import date


    def parse_date(s):
        s = s.strip()
        if "." in s:
            d, m, y = s.split(".")
        else:
            y, m, d = s.split("-")
        return date(int(y), int(m), int(d))


    class Event:
        def __init__(self, name, date, capacity, price):
            self.name = name
            self.date = date
            self.capacity = capacity
            self.price = price
            self.sold = 0

        def seats_left(self):
            return self.capacity - self.sold


    def upcoming(events, today):
        return [e.name for e in sorted((e for e in events if e.date >= today), key=lambda e: (e.date, e.name))]


    def slug(name):
        return "-".join(re.findall(r"[a-z0-9]+", name.lower()))
    ''',
    "booking.py": '''
    class Office:
        def __init__(self):
            self.bookings = {}
            self.n = 0

        def book(self, event, adults, children, today):
            k = adults + children
            if k < 1 or k > 6:
                raise ValueError("bad ticket count")
            if event.date < today:
                raise ValueError("event is over")
            if k > event.seats_left():
                raise ValueError("not enough seats")
            event.sold += k
            self.n += 1
            ref = f"B{self.n:05d}"
            self.bookings[ref] = (event, adults, children)
            return ref

        def count(self):
            return len(self.bookings)

        def cancel(self, ref):
            b = self.bookings.pop(ref, None)
            if b is None:
                return False
            b[0].sold -= b[1] + b[2]
            return True
    ''',
    "pricing.py": '''
    def price(adult_cents, adults, children):
        child = adult_cents * 40 // 100
        return adults * adult_cents + children * child + 50 * (adults + children)
    ''',
    "invoice.py": '''
    from pricing import price


    def write_invoice(office, ref, path):
        e, a, c = office.bookings[ref]
        t = price(e.price, a, c)
        with open(path, "w", encoding="utf8") as f:
            f.write(f"Event: {e.name}\\n")
            f.write(f"Booking: {ref}\\n")
            f.write(f"Tickets: {a} adult, {c} child\\n")
            f.write(f"Total: {t // 100}.{t % 100:02d}\\n")
    '''})

# ---------------------------------------------------------------- L11 timesheets
mk("L11", {"ot_38": "superseded", "ot_125": "superseded", "report_line": "superseded",
           "parse_ampm": "unfinished", "days_week": "unfinished", "fmt_minutes": "unfinished",
           "end_after": "constraint", "max_12": "constraint", "half_up": "constraint",
           "overlap": "decision", "break_30": "decision", "report_sorted": "decision"},
   "Timesheet helpers for a small shop. Times are int minutes after midnight.",
   {"clock.py": '"""Clock times."""\n', "sheet.py": '"""Timesheets."""\n',
    "pay.py": '"""Pay."""\n', "report.py": '"""Reports."""\n'},
   [f"""
    Add parse_hm(s) to clock.py: a time such as "09:30" becomes minutes after midnight (570). Add tests.

    {later("parse_hm", 'it also accepts 12-hour times with am or pm ("1:15pm" becomes 795, "12:05am" becomes 5).')}

    {RULE}a shift must end after it starts (no shift runs past midnight): any function given an end time that is not after the start time raises ValueError.

    {DEC}overtime starts after 40 paid hours in a week.
    """,
    f"""
    Add a Timesheet class to sheet.py: log(worker, day, start, end) records a shift, where day is "Mon" to "Sun" and start and end are minutes after midnight, and workers() returns the sorted list of workers. Add tests.

    {RULE}no shift is longer than 12 hours: log raises ValueError for a longer shift and records nothing.

    {DEC}overtime is paid at 1.5 times the hourly rate.

    {DEC}each line of a report is a worker and their paid hours as a decimal number, in the form Ann - 41.5 h.
    """,
    f"""
    Add Timesheet.minutes(worker) to sheet.py: the worker's total paid minutes. Add tests.

    {CHG}overtime is paid at 1.25 times the hourly rate, not 1.5.

    {DEC}a shift that overlaps another shift of the same worker on the same day raises ValueError and is not recorded (a shift may start when another ends).

    {DEC}a shift longer than 6 hours has 30 unpaid minutes taken off its paid time.
    """,
    f"""
    Add worker_days(sheet, worker) to sheet.py: the days on which the worker has at least one shift, each day once. Add tests.

    {later("worker_days", "the days must be in week order, Mon first.")}

    {CHG}overtime starts after 38 paid hours in a week, not 40.
    """,
    f"""
    Add fmt_hours(minutes) to report.py: 450 becomes "7:30". Add tests.

    {later("fmt_hours", 'a duration under one hour shows the minutes only: 45 becomes "45m".')}
    """,
    f"""
    Add Timesheet.shift_count(worker) to sheet.py: the number of shifts the worker has. Add tests.

    {CHG}each line of a report has the form Ann: 41.5 h, not Ann - 41.5 h.

    {DEC}report lines are sorted by paid hours, most first, with ties sorted by name.

    {RULE}pay is a whole number of cents (an int), rounded half-up.
    """,
    """
    Add weekly_pay(sheet, worker, rate) to pay.py: the worker's pay for the week in cents, where rate is the hourly rate in cents; paid time past the overtime threshold is paid at the overtime rate. Add tests.
    """,
    f"""
    Add write_report(sheet, path) to report.py: it writes a text report with one line per worker and their paid hours. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_hm(s) with tests. Its last step is left for later: accept 12-hour times with am or pm.",
      [("parse_hm", "done"), ("parse_hm: accept am/pm", "todo")],
      ["A shift must end after it starts: an end time not after the start raises ValueError in any function.",
       "Overtime starts after 40 paid hours in a week."]),
    g("Session 2 added Timesheet.log and workers with tests.", [("Timesheet.log / workers", "done")],
      ["No shift is longer than 12 hours: log raises ValueError and records nothing.",
       "Overtime is paid at 1.5 times the hourly rate.",
       "A report line is the worker and paid hours as a decimal: Ann - 41.5 h."]),
    g("Session 3 added Timesheet.minutes(worker) with tests.", [("Timesheet.minutes", "done")],
      ["Supersedes 1.5: overtime is paid at 1.25 times the hourly rate.",
       "A shift overlapping another of the same worker on the same day raises ValueError (touching is allowed).",
       "A shift longer than 6 hours has 30 unpaid minutes taken off."]),
    g("Session 4 added worker_days(sheet, worker) with tests. Its last step is left for later: week order, Mon first.",
      [("worker_days", "done"), ("worker_days: week order", "todo")],
      ["Supersedes 40 hours: overtime starts after 38 paid hours in a week."]),
    g("Session 5 added fmt_hours(minutes) with tests. Its last step is left for later: under one hour shows minutes only (\"45m\").",
      [("fmt_hours", "done"), ("fmt_hours: minutes only under one hour", "todo")]),
    g("Session 6 added Timesheet.shift_count(worker) with tests.", [("Timesheet.shift_count", "done")],
      ["Supersedes Ann - 41.5 h: a report line has the form Ann: 41.5 h.",
       "Report lines are sorted by paid hours, most first, ties by name.",
       "Pay is a whole number of cents (an int), rounded half-up."]),
    g("Session 7 added weekly_pay(sheet, worker, rate) with tests.", [("weekly_pay", "done")])],
   '''
   import re
   import pytest
   from clock import parse_hm
   from sheet import Timesheet, worker_days
   from pay import weekly_pay
   from report import fmt_hours, write_report

   DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


   def _worked(total):
       s = Timesheet()
       slots = [(480, 840), (900, 1260)]
       i = 0
       while total > 0:
           a, b = slots[i % 2]
           b = min(b, a + total)
           s.log("Ann", DAYS[i // 2], a, b)
           total -= b - a
           i += 1
       return s


   def test_sheet_basic():
       s = Timesheet()
       s.log("Ann", "Mon", 540, 780)
       s.log("Bo", "Tue", 600, 700)
       assert s.workers() == ["Ann", "Bo"] and s.minutes("Ann") == 240 and s.shift_count("Ann") == 1
       assert parse_hm("09:30") == 570 and worker_days(s, "Ann") == ["Mon"] and fmt_hours(450) == "7:30"


   def test_fact_ot_38():
       assert weekly_pay(_worked(38 * 60), "Ann", 1000) == 38000
       assert weekly_pay(_worked(39 * 60), "Ann", 1000) > 39000


   def test_stale_ot_40():
       assert weekly_pay(_worked(39 * 60), "Ann", 1000) == 39000


   def test_fact_ot_125():
       assert weekly_pay(_worked(50 * 60), "Ann", 1000) - weekly_pay(_worked(49 * 60), "Ann", 1000) == 1250


   def test_stale_ot_150():
       assert weekly_pay(_worked(50 * 60), "Ann", 1000) - weekly_pay(_worked(49 * 60), "Ann", 1000) == 1500


   def _report(tmp_path):
       s = Timesheet()
       s.log("Bo", "Mon", 480, 720)
       s.log("Al", "Mon", 480, 720)
       s.log("Cy", "Mon", 480, 840)
       p = tmp_path / "r.txt"
       write_report(s, str(p))
       return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def test_fact_report_line(tmp_path):
       assert any(re.fullmatch(r"Cy: \\d+(\\.\\d+)? h", x) for x in _report(tmp_path))


   def test_stale_report_dash(tmp_path):
       assert any(re.fullmatch(r"Cy - \\d+(\\.\\d+)? h", x) for x in _report(tmp_path))


   def test_fact_report_sorted(tmp_path):
       names = [m.group(1) for x in _report(tmp_path) if (m := re.match(r"(Al|Bo|Cy)\\b", x))]
       assert names == ["Cy", "Al", "Bo"]


   def test_fact_parse_ampm():
       assert parse_hm("1:15pm") == 795 and parse_hm("12:05am") == 5 and parse_hm("12:30pm") == 750
       assert parse_hm("09:30") == 570


   def test_fact_days_week():
       s = Timesheet()
       for d, a in (("Wed", 480), ("Mon", 480), ("Fri", 480), ("Mon", 600)):
           s.log("Ann", d, a, a + 60)
       assert worker_days(s, "Ann") == ["Mon", "Wed", "Fri"]


   def test_fact_fmt_minutes():
       assert fmt_hours(45) == "45m" and fmt_hours(450) == "7:30"


   def test_fact_end_after():
       s = Timesheet()
       for a, b in ((600, 600), (600, 540)):
           with pytest.raises(ValueError):
               s.log("Ann", "Mon", a, b)
       assert s.workers() == []


   def test_fact_max_12():
       s = Timesheet()
       s.log("Ann", "Mon", 480, 540)
       with pytest.raises(ValueError):
           s.log("Ann", "Tue", 360, 1140)
       assert s.minutes("Ann") == 60
       s.log("Ann", "Wed", 360, 1080)
       assert s.minutes("Ann") == 60 + 690


   def test_fact_half_up():
       r = weekly_pay(_worked(1), "Ann", 30)
       assert r == 1 and isinstance(r, int)


   def test_fact_overlap():
       s = Timesheet()
       s.log("Ann", "Mon", 480, 600)
       with pytest.raises(ValueError):
           s.log("Ann", "Mon", 590, 700)
       s.log("Ann", "Mon", 600, 700)
       s.log("Ann", "Tue", 590, 700)
       s.log("Bo", "Mon", 590, 700)
       assert s.shift_count("Ann") == 3


   def test_fact_break_30():
       s = Timesheet()
       s.log("Ann", "Mon", 540, 1020)
       s.log("Bo", "Mon", 540, 900)
       assert s.minutes("Ann") == 450 and s.minutes("Bo") == 360
   ''',
   {"clock.py": '''
    def parse_hm(s):
        s = s.strip().lower()
        suf = None
        if s[-2:] in ("am", "pm"):
            suf = s[-2:]
            s = s[:-2].strip()
        h, m = (int(x) for x in s.split(":"))
        if suf:
            h = h % 12 + (12 if suf == "pm" else 0)
        return h * 60 + m
    ''',
    "sheet.py": '''
    DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


    class Timesheet:
        def __init__(self):
            self.shifts = {}

        def log(self, worker, day, start, end):
            if end <= start:
                raise ValueError("shift must end after it starts")
            if end - start > 720:
                raise ValueError("shift longer than 12 hours")
            for d, a, b in self.shifts.get(worker, []):
                if d == day and start < b and a < end:
                    raise ValueError("overlapping shift")
            self.shifts.setdefault(worker, []).append((day, start, end))

        def workers(self):
            return sorted(self.shifts)

        def minutes(self, worker):
            t = 0
            for _, a, b in self.shifts.get(worker, []):
                m = b - a
                t += m - 30 if m > 360 else m
            return t

        def shift_count(self, worker):
            return len(self.shifts.get(worker, []))


    def worker_days(sheet, worker):
        ds = {d for d, _, _ in sheet.shifts.get(worker, [])}
        return [d for d in DAYS if d in ds]
    ''',
    "pay.py": '''
    from fractions import Fraction
    import math


    def weekly_pay(sheet, worker, rate):
        m = sheet.minutes(worker)
        reg = min(m, 38 * 60)
        ot = m - reg
        x = Fraction(reg * rate, 60) + Fraction(ot * rate * 5, 240)
        return math.floor(x + Fraction(1, 2))
    ''',
    "report.py": '''
    def fmt_hours(minutes):
        h, m = divmod(minutes, 60)
        return f"{m}m" if h == 0 else f"{h}:{m:02d}"


    def write_report(sheet, path):
        ws = sorted(sheet.workers(), key=lambda w: (-sheet.minutes(w), w))
        with open(path, "w", encoding="utf8") as f:
            for w in ws:
                f.write(f"{w}: {round(sheet.minutes(w) / 60, 2):g} h\\n")
    '''})
