"""Constraint tasks S01-S08: a rule stated in session 1, needed in session 3. Session 1's work
does not embody the rule in code, so only memory carries it."""
from scored_common import mk, g

RULE = "Project rule, which applies to all work on this project from now on: "

# S01 dates: returned dates are DD/MM/YYYY strings
mk("S01", "constraint", "dates.py", "Calendar helpers for a booking service.",
   '''
   """Calendar helpers."""
   from datetime import date, timedelta
   ''',
   '''
   from datetime import date
   from dates import is_weekend


   def test_is_weekend():
       assert is_weekend(date(2026, 1, 3)) is True
   ''',
   [f"""
    Add is_weekend(d) to dates.py: True when the datetime.date d is a Saturday or Sunday. Add tests.

    {RULE}every date that any function in this project returns is a string in DD/MM/YYYY format (for example "05/01/2026"), never a date object and never ISO format.
    """,
    """
    Add weekday_name(d) to dates.py: the English name of the weekday of the datetime.date d, such as "Monday". Add tests.
    """,
    """
    Add next_business_day(d) to dates.py: d is a datetime.date; it returns the first day after d that is Monday to Friday. Add tests.
    """],
   [g("Session 1 added is_weekend(d) with tests.", [("is_weekend", "done")],
      ["Every date that any function returns is a string in DD/MM/YYYY format (e.g. \"05/01/2026\"), never a date object and never ISO."]),
    g("Session 2 added weekday_name(d) with tests.", [("weekday_name", "done")])],
   '''
   from datetime import date
   from dates import is_weekend, weekday_name, next_business_day


   def test_weekend_and_names():
       assert is_weekend(date(2026, 1, 4)) is True
       assert is_weekend(date(2026, 1, 5)) is False
       assert weekday_name(date(2026, 1, 5)) == "Monday"


   def test_fact_next_business_day_format():
       r = next_business_day(date(2026, 1, 2))  # a Friday
       assert r == "05/01/2026" and type(r) is str
       assert next_business_day(date(2026, 1, 5)) == "06/01/2026"
       assert next_business_day(date(2025, 12, 31)) == "01/01/2026"
   ''',
   '''
   from datetime import date, timedelta


   def is_weekend(d):
       return d.weekday() >= 5


   def weekday_name(d):
       return d.strftime("%A")


   def next_business_day(d):
       d = d + timedelta(days=1)
       while d.weekday() >= 5:
           d += timedelta(days=1)
       return d.strftime("%d/%m/%Y")
   ''')

# S02 ranking: returned lists are sorted descending
mk("S02", "constraint", "ranking.py", "Score helpers for a quiz app.",
   '''
   """Score helpers."""
   ''',
   '''
   from ranking import mean


   def test_mean():
       assert mean([1, 2, 3]) == 2
   ''',
   [f"""
    Add mean(scores) to ranking.py: the arithmetic mean of a non-empty list of numbers. Add tests.

    {RULE}every function in this project that returns a list of values returns it sorted in descending order (largest first).
    """,
    """
    Add median(scores) to ranking.py: the median of a non-empty list of numbers (the mean of the two middle values for an even count). Add tests.
    """,
    """
    Add unique_scores(scores) to ranking.py: it returns a list of the distinct values in scores, each once. Add tests.
    """],
   [g("Session 1 added mean(scores) with tests.", [("mean", "done")],
      ["Every function that returns a list of values returns it sorted in descending order (largest first)."]),
    g("Session 2 added median(scores) with tests.", [("median", "done")])],
   '''
   from ranking import mean, median, unique_scores


   def test_mean_median():
       assert mean([2, 4]) == 3
       assert median([5, 1, 3]) == 3
       assert median([1, 2, 3, 4]) == 2.5


   def test_fact_unique_descending():
       assert unique_scores([2, 9, 5, 9, 2]) == [9, 5, 2]
       assert unique_scores([1, 3, 2]) == [3, 2, 1]
   ''',
   '''
   def mean(scores):
       return sum(scores) / len(scores)


   def median(scores):
       s = sorted(scores)
       n = len(s)
       return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


   def unique_scores(scores):
       return sorted(set(scores), reverse=True)
   ''')

# S03 parsing: never raise on bad input, return None
mk("S03", "constraint", "parsing.py", "Input cleaning helpers for a form backend.",
   '''
   """Input cleaning helpers."""
   ''',
   '''
   from parsing import strip_all


   def test_strip_all():
       assert strip_all([" a ", "b "]) == ["a", "b"]
   ''',
   [f"""
    Add strip_all(items) to parsing.py: it returns a new list with each string stripped of surrounding whitespace. Add tests.

    {RULE}functions in this project never raise an exception because of bad input; when the input cannot be handled they return None instead.
    """,
    """
    Add split_fields(line) to parsing.py: it splits a line on commas and strips each field, so " a, b ,c" gives ["a", "b", "c"]. Add tests.
    """,
    """
    Add parse_date_iso(s) to parsing.py: it turns a "YYYY-MM-DD" string into a datetime.date. Add tests.
    """],
   [g("Session 1 added strip_all(items) with tests.", [("strip_all", "done")],
      ["Functions never raise an exception because of bad input; when input cannot be handled they return None instead."]),
    g("Session 2 added split_fields(line) with tests.", [("split_fields", "done")])],
   '''
   from datetime import date
   from parsing import strip_all, split_fields, parse_date_iso


   def test_strip_split():
       assert strip_all(["x "]) == ["x"]
       assert split_fields(" a, b ,c") == ["a", "b", "c"]


   def test_parse_date_ok():
       assert parse_date_iso("2026-01-05") == date(2026, 1, 5)


   def test_fact_bad_input_returns_none():
       assert parse_date_iso("2026-13-40") is None
       assert parse_date_iso("hello") is None
       assert parse_date_iso("") is None
   ''',
   '''
   from datetime import date


   def strip_all(items):
       return [s.strip() for s in items]


   def split_fields(line):
       return [f.strip() for f in line.split(",")]


   def parse_date_iso(s):
       try:
           return date.fromisoformat(s)
       except (ValueError, TypeError):
           return None
   ''')

# S04 inventory: every error is InventoryError (not a ValueError)
mk("S04", "constraint", "inventory.py", "Stock counts for a small shop.",
   '''
   """Stock counts."""


   class Inventory:
       def __init__(self):
           self.stock = {}
   ''',
   '''
   from inventory import Inventory


   def test_add():
       inv = Inventory()
       inv.add_stock("pen", 3)
       assert inv.quantity("pen") == 3
   ''',
   [f"""
    Add add_stock(name, qty) and quantity(name) to Inventory in inventory.py; quantity is 0 for an unknown name. Add tests.

    {RULE}every error this project raises is an InventoryError. Define it in inventory.py as a direct subclass of Exception (not of ValueError, KeyError or any other built-in error). Nothing raises it yet.
    """,
    """
    Add total_items() to Inventory: the sum of all quantities. Add tests.
    """,
    """
    Add remove_stock(name, qty) to Inventory: it takes qty items away. Removing more than is in stock is an error and must leave the stock unchanged. Add tests.
    """],
   [g("Session 1 added add_stock and quantity with tests, and defined InventoryError.", [("add_stock, quantity", "done")],
      ["Every error raised is an InventoryError, defined in inventory.py as a direct subclass of Exception (not ValueError, KeyError or another built-in error)."]),
    g("Session 2 added total_items() with tests.", [("total_items", "done")])],
   '''
   import pytest
   import inventory
   from inventory import Inventory


   def test_add_total():
       inv = Inventory()
       inv.add_stock("pen", 3)
       inv.add_stock("pen", 2)
       inv.add_stock("cup", 1)
       assert inv.quantity("pen") == 5 and inv.quantity("x") == 0
       assert inv.total_items() == 6


   def test_remove_ok():
       inv = Inventory()
       inv.add_stock("pen", 3)
       inv.remove_stock("pen", 2)
       assert inv.quantity("pen") == 1


   def test_fact_inventory_error():
       err = inventory.InventoryError
       assert issubclass(err, Exception) and not issubclass(err, (ValueError, KeyError, LookupError))
       inv = Inventory()
       inv.add_stock("pen", 1)
       with pytest.raises(err):
           inv.remove_stock("pen", 5)
       assert inv.quantity("pen") == 1
   ''',
   '''
   class InventoryError(Exception):
       pass


   class Inventory:
       def __init__(self):
           self.stock = {}

       def add_stock(self, name, qty):
           self.stock[name] = self.stock.get(name, 0) + qty

       def quantity(self, name):
           return self.stock.get(name, 0)

       def total_items(self):
           return sum(self.stock.values())

       def remove_stock(self, name, qty):
           if qty > self.quantity(name):
               raise InventoryError(name)
           self.stock[name] -= qty
   ''')

# S05 rates: rates are fractions 0-1, rounded to 4 places
mk("S05", "constraint", "rates.py", "Order maths for an online store.",
   '''
   """Order maths."""
   ''',
   '''
   from rates import total


   def test_total():
       assert total([{"price": 2, "qty": 3}]) == 6
   ''',
   [f"""
    Add total(lines) to rates.py: lines is a list of dicts with "price" and "qty"; it returns the sum of price * qty. Add tests.

    {RULE}every rate or percentage that a function in this project returns is a fraction between 0 and 1 (15% is 0.15, never 15), rounded to 4 decimal places.
    """,
    """
    Add count_items(lines) to rates.py: the sum of all "qty" values. Add tests.
    """,
    """
    Add two functions to rates.py and test them:
    - discount_rate(order_total): the discount for an order: 10% from 200 up, 5% from 100 up, otherwise none.
    - growth(old, new): the growth from old to new as a percentage.
    """],
   [g("Session 1 added total(lines) with tests.", [("total", "done")],
      ["Every rate or percentage a function returns is a fraction from 0 to 1 (15% is 0.15, never 15), rounded to 4 decimal places."]),
    g("Session 2 added count_items(lines) with tests.", [("count_items", "done")])],
   '''
   from rates import total, count_items, discount_rate, growth


   def test_total_count():
       lines = [{"price": 2, "qty": 3}, {"price": 5, "qty": 1}]
       assert total(lines) == 11 and count_items(lines) == 4


   def test_fact_discount_fraction():
       assert discount_rate(250) == 0.1
       assert discount_rate(150) == 0.05
       assert discount_rate(50) == 0


   def test_fact_growth_fraction():
       assert growth(3, 4) == 0.3333
       assert growth(100, 150) == 0.5
   ''',
   '''
   def total(lines):
       return sum(l["price"] * l["qty"] for l in lines)


   def count_items(lines):
       return sum(l["qty"] for l in lines)


   def discount_rate(order_total):
       return 0.1 if order_total >= 200 else 0.05 if order_total >= 100 else 0


   def growth(old, new):
       return round((new - old) / old, 4)
   ''')

# S06 export: booleans in files are Y/N
mk("S06", "constraint", "export.py", "Task list helpers with file export.",
   '''
   """Task list helpers."""
   ''',
   '''
   from export import make_task


   def test_make_task():
       assert make_task("a") == {"title": "a", "done": False}
   ''',
   [f"""
    Add make_task(title, done=False) to export.py: it returns a dict {{"title": title, "done": done}}. Add tests.

    {RULE}every boolean value that this project writes to any file is written as Y (true) or N (false).
    """,
    """
    Add pending(tasks) to export.py: the tasks whose "done" is False, in order. Add tests.
    """,
    """
    Add write_csv(tasks, path) to export.py: it writes the tasks to a comma-separated file with the header row title,done and one row per task. Add tests.
    """],
   [g("Session 1 added make_task with tests.", [("make_task", "done")],
      ["Every boolean value written to any file is written as Y (true) or N (false)."]),
    g("Session 2 added pending(tasks) with tests.", [("pending", "done")])],
   '''
   from export import make_task, pending, write_csv


   def test_pending():
       ts = [make_task("a", True), make_task("b")]
       assert [t["title"] for t in pending(ts)] == ["b"]


   def test_fact_csv_booleans(tmp_path):
       p = tmp_path / "t.csv"
       write_csv([make_task("a", True), make_task("b")], str(p))
       lines = [l.strip() for l in p.read_text().splitlines() if l.strip()]
       assert lines == ["title,done", "a,Y", "b,N"]
   ''',
   '''
   def make_task(title, done=False):
       return {"title": title, "done": done}


   def pending(tasks):
       return [t for t in tasks if not t["done"]]


   def write_csv(tasks, path):
       with open(path, "w") as f:
           f.write("title,done\\n")
           for t in tasks:
               f.write(f"{t['title']},{'Y' if t['done'] else 'N'}\\n")
   ''')

# S07 users: usernames lowercase, spaces -> "."
mk("S07", "constraint", "users.py", "User helpers for a forum.",
   '''
   """User helpers."""
   ''',
   '''
   from users import is_valid_email


   def test_email():
       assert is_valid_email("a@b.com")
   ''',
   [f"""
    Add is_valid_email(s) to users.py: True when s has exactly one "@" with text on both sides and a "." in the part after it. Add tests.

    {RULE}usernames are always stored stripped, in lowercase, with each run of spaces replaced by a single "." (so " Ann  Lee " is stored as "ann.lee").
    """,
    """
    Add domain(email) to users.py: the part after the "@", in lowercase. Add tests.
    """,
    """
    Add a Users class to users.py that keeps the forum's usernames: add(name) stores a username, names() returns the stored usernames in the order they were added, and has(name) tells whether a username is stored. Add tests.
    """],
   [g("Session 1 added is_valid_email with tests.", [("is_valid_email", "done")],
      ["Usernames are stored stripped, lowercase, with each run of spaces replaced by a single \".\" (\" Ann  Lee \" is stored as \"ann.lee\")."]),
    g("Session 2 added domain(email) with tests.", [("domain", "done")])],
   '''
   from users import is_valid_email, domain, Users


   def test_email_domain():
       assert is_valid_email("x@y.org") and not is_valid_email("x@@y.org") and not is_valid_email("xy.org")
       assert domain("a@Ex.COM") == "ex.com"


   def test_fact_username_storage():
       u = Users()
       u.add("Ann Lee")
       u.add(" Bo  Diaz ")
       assert u.names() == ["ann.lee", "bo.diaz"]
   ''',
   '''
   import re


   def is_valid_email(s):
       if s.count("@") != 1:
           return False
       a, b = s.split("@")
       return bool(a) and "." in b and not b.startswith(".")


   def domain(email):
       return email.split("@", 1)[1].lower()


   def _norm(name):
       return re.sub(r" +", ".", name.strip().lower())


   class Users:
       def __init__(self):
           self._names = []

       def add(self, name):
           self._names.append(_norm(name))

       def names(self):
           return list(self._names)

       def has(self, name):
           return _norm(name) in self._names
   ''')

# S08 temps: returned temperatures in Kelvin, 2 places
mk("S08", "constraint", "temps.py", "Weather station helpers.",
   '''
   """Weather station helpers. Readings arrive in degrees Celsius."""
   ''',
   '''
   from temps import is_freezing


   def test_freezing():
       assert is_freezing(-1)
   ''',
   [f"""
    Add is_freezing(c) to temps.py: True when the Celsius reading c is at or below 0. Add tests.

    {RULE}every temperature that a function in this project returns is in Kelvin (K = C + 273.15), rounded to 2 decimal places, whatever unit its inputs use.
    """,
    """
    Add count_above(readings, limit) to temps.py: how many Celsius readings are strictly above limit. Add tests.
    """,
    """
    Add average(readings) to temps.py: the average temperature of a non-empty list of Celsius readings. Add tests.
    """],
   [g("Session 1 added is_freezing(c) with tests.", [("is_freezing", "done")],
      ["Every temperature a function returns is in Kelvin (K = C + 273.15), rounded to 2 decimal places, whatever the input unit."]),
    g("Session 2 added count_above(readings, limit) with tests.", [("count_above", "done")])],
   '''
   from temps import is_freezing, count_above, average


   def test_freezing_count():
       assert is_freezing(0) and not is_freezing(0.5)
       assert count_above([1, 5, 9], 4) == 2


   def test_fact_average_kelvin():
       assert average([0, 10]) == 278.15
       assert average([20.5]) == 293.65
   ''',
   '''
   def is_freezing(c):
       return c <= 0


   def count_above(readings, limit):
       return sum(1 for r in readings if r > limit)


   def average(readings):
       return round(sum(readings) / len(readings) + 273.15, 2)
   ''')

print("constraint ok")
