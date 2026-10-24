"""R-015 simple projects T03-T16: 4 sessions, 5 facts each, the same style as r015_simple.py
(T01, T02). Each project has one superseded fact (with a test_stale_* for the old value), one
unfinished step, and constraints and decisions; every fact is stated in a session prompt."""
from r015_common import CHG, DEC, FINISH, RULE, later, mk

# ---------------------------------------------------------------- T03 library loans
mk("T03", {"loan_days": "superseded", "fee_cap": "unfinished", "no_double_lend": "constraint",
           "member_limit": "constraint", "return_unknown": "decision"},
   "Book loans for a small lending library. Days are int day numbers; fees are in cents.",
   {"library.py": '"""Library loans."""\n', "fees.py": '"""Late fees."""\n'},
   [f"""
    Add a Library class to library.py with add_book(isbn, title), which adds a book, lend(isbn, member, day), which lends the book isbn to member on day (days are int day numbers), and is_out(isbn), which tells whether the book is lent out. Add tests.

    {RULE}a book that is already out cannot be lent again: lend raises ValueError and changes nothing.

    {RULE}a member holds at most 3 books at once: lending a 4th book to them raises ValueError and changes nothing.

    {DEC}the loan period is 14 days.
    """,
    f"""
    Add Library.due(isbn), the day a lent book is due back: the day it was lent plus the loan period. Add late_fee(lib, isbn, day) to fees.py: the fee in cents if the lent book isbn comes back on day, 25 cents for each day after its due day (0 if day is not after the due day). Add tests.

    {later("late_fee", "the fee is never more than 500 cents.")}
    """,
    f"""
    Add Library.give_back(isbn), which ends the loan of isbn, and Library.held(member), the sorted list of the ISBNs member holds. Add tests.

    {DEC}give_back of a book that is not out raises KeyError.

    {CHG}the loan period is 21 days, not 14.
    """,
    f"""
    Add Library.titles(), the sorted list of the titles of the books that are not out. Add tests. {FINISH}
    """],
   '''
   import pytest
   from library import Library
   from fees import late_fee


   def _lib():
       lib = Library()
       for i in "1234":
           lib.add_book("isbn" + i, "Book " + i)
       return lib


   def test_basic():
       lib = _lib()
       lib.lend("isbn1", "ann", 0)
       lib.lend("isbn2", "bob", 3)
       assert lib.is_out("isbn1") and not lib.is_out("isbn3")
       assert lib.held("ann") == ["isbn1"] and lib.held("zed") == []
       lib.give_back("isbn1")
       assert not lib.is_out("isbn1") and lib.titles() == ["Book 1", "Book 3", "Book 4"]


   def test_fact_loan_days():
       lib = _lib()
       lib.lend("isbn1", "ann", 5)
       assert lib.due("isbn1") == 26 and late_fee(lib, "isbn1", 26) == 0 and late_fee(lib, "isbn1", 30) == 100


   def test_stale_loan_14():
       lib = _lib()
       lib.lend("isbn1", "ann", 5)
       assert lib.due("isbn1") == 19


   def test_fact_fee_cap():
       lib = _lib()
       lib.lend("isbn1", "ann", 0)
       assert late_fee(lib, "isbn1", 30) == 225 and late_fee(lib, "isbn1", 100) == 500


   def test_fact_no_double_lend():
       lib = _lib()
       lib.lend("isbn1", "ann", 0)
       with pytest.raises(ValueError):
           lib.lend("isbn1", "bob", 1)
       assert lib.held("ann") == ["isbn1"] and lib.held("bob") == []


   def test_fact_member_limit():
       lib = _lib()
       for i in "123":
           lib.lend("isbn" + i, "ann", 0)
       with pytest.raises(ValueError):
           lib.lend("isbn4", "ann", 0)
       assert not lib.is_out("isbn4") and len(lib.held("ann")) == 3


   def test_fact_return_unknown():
       lib = _lib()
       for isbn in ("isbn9", "isbn2"):
           with pytest.raises(KeyError):
               lib.give_back(isbn)
   ''',
   {"library.py": '''
    """Library loans."""

    LOAN_DAYS = 21


    class Library:
        def __init__(self):
            self._title = {}
            self._out = {}

        def add_book(self, isbn, title):
            self._title[isbn] = title

        def lend(self, isbn, member, day):
            if isbn in self._out:
                raise ValueError("book is out")
            if len(self.held(member)) >= 3:
                raise ValueError("member holds 3 books")
            self._out[isbn] = (member, day)

        def is_out(self, isbn):
            return isbn in self._out

        def due(self, isbn):
            return self._out[isbn][1] + LOAN_DAYS

        def give_back(self, isbn):
            if isbn not in self._out:
                raise KeyError(isbn)
            del self._out[isbn]

        def held(self, member):
            return sorted(i for i, (m, _) in self._out.items() if m == member)

        def titles(self):
            return sorted(t for i, t in self._title.items() if i not in self._out)
    ''',
    "fees.py": '''
    """Late fees."""


    def late_fee(lib, isbn, day):
        return min(500, max(0, day - lib.due(isbn)) * 25)
    '''}, "simple")

# ---------------------------------------------------------------- T04 parking garage
mk("T04", {"free_minutes": "superseded", "day_cap": "unfinished", "plate_norm": "constraint",
           "no_double_enter": "constraint", "leave_before": "decision"},
   "A parking garage: cars enter and leave, stays are paid. Times are int minutes; prices are in cents.",
   {"garage.py": '"""Parking garage."""\n', "tariff.py": '"""Parking prices."""\n'},
   [f"""
    Add a Garage class to garage.py with enter(plate, minute), which records that the car with that plate entered at minute (an int), leave(plate, minute), which records that it left and returns the minutes it stayed (leave for a plate that is not inside raises KeyError), and inside(), the sorted list of plates inside. Add tests.

    {RULE}plates are stored without spaces and in upper case: "ab 123" and "AB123" are the same car.

    {RULE}enter for a car that is already inside raises ValueError and changes nothing.

    {DEC}the first 30 minutes are free: a stay of 30 minutes or less costs nothing.
    """,
    f"""
    Add fee(minutes) to tariff.py: the price in cents of a stay of that many minutes: 0 for a stay within the free minutes, otherwise 200 cents for every started hour of the whole stay (a stay of 61 minutes is 2 started hours). Add tests.

    {later("fee", "a stay never costs more than 1500 cents.")}
    """,
    f"""
    Add Garage.count(), the number of cars inside, and Garage.history(plate), the list of the minutes of each finished stay of plate, in order. Add tests.

    {DEC}leave with a minute earlier than the car's entry minute raises ValueError, and the car stays inside.

    {CHG}the first 15 minutes are free, not 30: a stay of 15 minutes or less costs nothing.
    """,
    f"""
    Add Garage.revenue(), the sum of the fees of all finished stays. Add tests. {FINISH}
    """],
   '''
   import pytest
   from garage import Garage
   from tariff import fee


   def test_basic():
       g = Garage()
       g.enter("A1", 0)
       g.enter("B2", 10)
       assert g.count() == 2 and g.inside() == ["A1", "B2"]
       assert g.leave("A1", 60) == 60
       assert g.inside() == ["B2"] and g.history("A1") == [60] and g.revenue() == 200
       with pytest.raises(KeyError):
           g.leave("Q9", 5)


   def test_fact_free_minutes():
       assert fee(15) == 0 and fee(20) == 200 and fee(30) == 200 and fee(61) == 400


   def test_stale_free_30():
       assert fee(20) == 0


   def test_fact_day_cap():
       assert fee(300) == 1000 and fee(480) == 1500 and fee(600) == 1500


   def test_fact_plate_norm():
       g = Garage()
       g.enter("ab 123", 0)
       assert g.inside() == ["AB123"]
       assert g.leave("Ab1 23", 60) == 60 and g.history("AB123") == [60]


   def test_fact_no_double_enter():
       g = Garage()
       g.enter("X1", 0)
       with pytest.raises(ValueError):
           g.enter("X1", 5)
       assert g.count() == 1 and g.leave("X1", 10) == 10


   def test_fact_leave_before():
       g = Garage()
       g.enter("X1", 50)
       with pytest.raises(ValueError):
           g.leave("X1", 40)
       assert g.inside() == ["X1"] and g.leave("X1", 70) == 20
   ''',
   {"garage.py": '''
    """Parking garage."""
    from tariff import fee


    def _p(plate):
        return plate.replace(" ", "").upper()


    class Garage:
        def __init__(self):
            self._in = {}
            self._stays = {}

        def enter(self, plate, minute):
            p = _p(plate)
            if p in self._in:
                raise ValueError("already inside")
            self._in[p] = minute

        def leave(self, plate, minute):
            p = _p(plate)
            if p not in self._in:
                raise KeyError(p)
            if minute < self._in[p]:
                raise ValueError("leave before entry")
            m = minute - self._in.pop(p)
            self._stays.setdefault(p, []).append(m)
            return m

        def inside(self):
            return sorted(self._in)

        def count(self):
            return len(self._in)

        def history(self, plate):
            return list(self._stays.get(_p(plate), []))

        def revenue(self):
            return sum(fee(m) for s in self._stays.values() for m in s)
    ''',
    "tariff.py": '''
    """Parking prices."""

    FREE = 15


    def fee(minutes):
        if minutes <= FREE:
            return 0
        return min(1500, -(-minutes // 60) * 200)
    '''}, "simple")

# ---------------------------------------------------------------- T05 gym classes
mk("T05", {"class_price": "superseded", "waitlist_promote": "unfinished", "no_double_book": "constraint",
           "capacity_range": "constraint", "full_waitlist": "decision"},
   "Class bookings for a small gym. Prices are in cents.",
   {"classes.py": '"""Gym classes."""\n', "billing.py": '"""Class billing."""\n'},
   [f"""
    Add a Schedule class to classes.py with add_class(name, capacity), which adds a class with that many places, book(name, member), which books member into class name, booked(name), the list of members booked in class name in booking order, and waitlist(name), the list of members waiting for a place in class name, in order. Add tests.

    {RULE}a member who is already booked or waiting in a class cannot book it again: book raises ValueError and changes nothing.

    {DEC}when a class is full, book puts the member at the end of its waitlist and returns False; a booking that gets a place returns True.

    {DEC}a class costs 800 cents.
    """,
    f"""
    Add Schedule.cancel(name, member), which removes member's booking or waitlist place in class name. Add bill(schedule, member) to billing.py: the price of one class times the number of classes member is booked in (waitlist places are not billed). Add tests.

    {later("cancel", "when a booked member cancels, the first member on the waitlist leaves the waitlist and is booked (at the end of booked).")}
    """,
    f"""
    Add Schedule.classes(), the sorted list of class names. Add tests.

    {RULE}a class capacity is between 1 and 30, inclusive: add_class with any other capacity raises ValueError and adds nothing.

    {CHG}a class costs 950 cents, not 800.
    """,
    f"""
    Add Schedule.busy(member), the sorted list of the classes member is booked in. Add tests. {FINISH}
    """],
   '''
   import pytest
   from classes import Schedule
   from billing import bill


   def test_basic():
       s = Schedule()
       s.add_class("yoga", 2)
       s.add_class("spin", 5)
       assert s.book("yoga", "ann") is True and s.book("spin", "ann") is True
       assert s.booked("yoga") == ["ann"] and s.waitlist("yoga") == []
       assert s.classes() == ["spin", "yoga"] and s.busy("ann") == ["spin", "yoga"]
       s.cancel("spin", "ann")
       assert s.busy("ann") == ["yoga"] and s.booked("spin") == []


   def _two():
       s = Schedule()
       s.add_class("yoga", 5)
       s.add_class("spin", 5)
       s.book("yoga", "ann")
       s.book("spin", "ann")
       return s


   def test_fact_class_price():
       assert bill(_two(), "ann") == 1900


   def test_stale_price_800():
       assert bill(_two(), "ann") == 1600


   def test_fact_waitlist_promote():
       s = Schedule()
       s.add_class("yoga", 1)
       s.book("yoga", "ann")
       s.book("yoga", "bob")
       s.book("yoga", "cy")
       s.cancel("yoga", "ann")
       assert s.booked("yoga") == ["bob"] and s.waitlist("yoga") == ["cy"]


   def test_fact_no_double_book():
       s = Schedule()
       s.add_class("yoga", 1)
       s.book("yoga", "ann")
       s.book("yoga", "bob")
       for m in ("ann", "bob"):
           with pytest.raises(ValueError):
               s.book("yoga", m)
       assert s.booked("yoga") == ["ann"] and s.waitlist("yoga") == ["bob"]


   def test_fact_capacity_range():
       s = Schedule()
       for name, cap in (("a", 0), ("b", 31), ("c", -1)):
           with pytest.raises(ValueError):
               s.add_class(name, cap)
       s.add_class("d", 30)
       s.add_class("e", 1)
       assert s.classes() == ["d", "e"]


   def test_fact_full_waitlist():
       s = Schedule()
       s.add_class("yoga", 2)
       assert [s.book("yoga", m) for m in ("ann", "bob", "cy", "dee")] == [True, True, False, False]
       assert s.booked("yoga") == ["ann", "bob"] and s.waitlist("yoga") == ["cy", "dee"]
   ''',
   {"classes.py": '''
    """Gym classes."""


    class Schedule:
        def __init__(self):
            self._cap = {}
            self._booked = {}
            self._wait = {}

        def add_class(self, name, capacity):
            if not 1 <= capacity <= 30:
                raise ValueError("capacity is 1 to 30")
            self._cap[name] = capacity
            self._booked[name] = []
            self._wait[name] = []

        def book(self, name, member):
            if member in self._booked[name] or member in self._wait[name]:
                raise ValueError("already booked")
            if len(self._booked[name]) < self._cap[name]:
                self._booked[name].append(member)
                return True
            self._wait[name].append(member)
            return False

        def booked(self, name):
            return list(self._booked[name])

        def waitlist(self, name):
            return list(self._wait[name])

        def cancel(self, name, member):
            if member in self._wait[name]:
                self._wait[name].remove(member)
                return
            self._booked[name].remove(member)
            if self._wait[name]:
                self._booked[name].append(self._wait[name].pop(0))

        def classes(self):
            return sorted(self._cap)

        def busy(self, member):
            return sorted(n for n, b in self._booked.items() if member in b)
    ''',
    "billing.py": '''
    """Class billing."""

    PRICE = 950


    def bill(schedule, member):
        return len(schedule.busy(member)) * PRICE
    '''}, "simple")

# ---------------------------------------------------------------- T06 recipe scaling
mk("T06", {"default_servings": "superseded", "min_one_gram": "unfinished", "grams_positive": "constraint",
           "scale_positive": "constraint", "name_lower": "decision"},
   "Recipes that scale to a number of servings. Amounts are whole grams.",
   {"recipe.py": '"""Recipes."""\n', "shopping.py": '"""Shopping lists."""\n'},
   [f"""
    Add a Recipe class to recipe.py: Recipe(servings) has a servings attribute, add(ingredient, grams), which adds grams of ingredient (adding an ingredient again adds to its amount), and grams(ingredient), the amount of ingredient (0 for one the recipe does not have). Add tests.

    {RULE}grams must be more than 0: add with 0 or less raises ValueError and changes nothing.

    {DEC}a Recipe made without a servings number serves 4: Recipe() has servings 4.
    """,
    f"""
    Add scale(recipe, servings) to recipe.py: a new Recipe for that many servings, each amount being grams times new servings divided by old servings, rounded to the nearest whole gram. Add Recipe.ingredients(), the sorted list of ingredient names. Add tests.

    {DEC}ingredient names are stored in lower case: "Flour" and "flour" are the same ingredient.

    {later("scale", "an amount that would round to 0 grams becomes 1 gram.")}
    """,
    f"""
    Add shopping_list(recipes) to shopping.py: a dict from ingredient name to its total grams over all the recipes in the list. Add tests.

    {RULE}scale to 0 or fewer servings raises ValueError.

    {CHG}a Recipe made without a servings number serves 2, not 4: Recipe() has servings 2.
    """,
    f"""
    Add Recipe.remove(ingredient), which takes ingredient out of the recipe. Add tests. {FINISH}
    """],
   '''
   import pytest
   from recipe import Recipe, scale
   from shopping import shopping_list


   def test_basic():
       r = Recipe(4)
       r.add("flour", 200)
       r.add("flour", 50)
       r.add("egg", 100)
       assert r.servings == 4 and r.grams("flour") == 250 and r.grams("milk") == 0
       assert r.ingredients() == ["egg", "flour"]
       s = scale(r, 8)
       assert s.servings == 8 and s.grams("egg") == 200 and s.grams("flour") == 500
       assert shopping_list([r, s]) == {"egg": 300, "flour": 750}
       r.remove("egg")
       assert r.ingredients() == ["flour"]


   def test_fact_default_servings():
       r = Recipe()
       r.add("salt", 10)
       assert r.servings == 2 and scale(r, 4).grams("salt") == 20


   def test_stale_servings_4():
       assert Recipe().servings == 4


   def test_fact_min_one_gram():
       r = Recipe(4)
       r.add("salt", 1)
       r.add("sugar", 12)
       s = scale(r, 1)
       assert s.grams("salt") == 1 and s.grams("sugar") == 3


   def test_fact_grams_positive():
       r = Recipe(4)
       for g in (0, -5):
           with pytest.raises(ValueError):
               r.add("salt", g)
       assert r.ingredients() == [] and r.grams("salt") == 0


   def test_fact_scale_positive():
       r = Recipe(4)
       r.add("salt", 10)
       for n in (0, -2):
           with pytest.raises(ValueError):
               scale(r, n)


   def test_fact_name_lower():
       r = Recipe(4)
       r.add("Flour", 100)
       assert r.grams("FLOUR") == 100 and r.ingredients() == ["flour"]
   ''',
   {"recipe.py": '''
    """Recipes."""


    class Recipe:
        def __init__(self, servings=2):
            self.servings = servings
            self._g = {}

        def add(self, ingredient, grams):
            if grams <= 0:
                raise ValueError("grams must be positive")
            k = ingredient.lower()
            self._g[k] = self._g.get(k, 0) + grams

        def grams(self, ingredient):
            return self._g.get(ingredient.lower(), 0)

        def ingredients(self):
            return sorted(self._g)

        def remove(self, ingredient):
            self._g.pop(ingredient.lower(), None)


    def scale(recipe, servings):
        if servings <= 0:
            raise ValueError("servings must be positive")
        r = Recipe(servings)
        for k, g in recipe._g.items():
            r._g[k] = max(1, round(g * servings / recipe.servings))
        return r
    ''',
    "shopping.py": '''
    """Shopping lists."""


    def shopping_list(recipes):
        out = {}
        for r in recipes:
            for k in r.ingredients():
                out[k] = out.get(k, 0) + r.grams(k)
        return out
    '''}, "simple")

# ---------------------------------------------------------------- T07 bank account
mk("T07", {"overdraft": "superseded", "balance_line": "unfinished", "amount_positive": "constraint",
           "deposit_max": "constraint", "interest_round": "decision"},
   "A bank account with a statement. Amounts are in cents (ints).",
   {"account.py": '"""Bank account."""\n', "statement.py": '"""Account statement."""\n'},
   [f"""
    Add an Account class to account.py with deposit(amount), withdraw(amount) and balance(), all in cents (ints); a new account has balance 0. Add tests.

    {RULE}an amount must be a positive int: deposit or withdraw with anything else (0, a negative number, a float) raises ValueError and changes nothing.

    {DEC}the overdraft limit is 5000 cents: a withdrawal that would take the balance below -5000 raises ValueError and changes nothing.
    """,
    f"""
    Add Account.history(), the list of (kind, amount) pairs of every deposit and withdrawal in order, with kind "deposit" or "withdraw". Add statement(acct) to statement.py: a list of lines, one per history entry, each "kind amount" (for example "deposit 500" or "withdraw 200"). Add tests.

    {later("statement", 'add a last line "balance N", with N the balance in cents (for example "balance 300").')}
    """,
    f"""
    Add Account.add_interest(pct), which adds pct percent of the balance to the balance and records it in history as ("interest", amount). Add tests.

    {RULE}one deposit is at most 1000000 cents: a larger deposit raises ValueError and changes nothing.

    {DEC}interest is rounded down to a whole cent, and an account whose balance is 0 or less gets no interest.

    {CHG}the overdraft limit is 2000 cents, not 5000: a withdrawal that would take the balance below -2000 raises ValueError and changes nothing.
    """,
    f"""
    Add Account.count(kind), the number of history entries of that kind. Add tests. {FINISH}
    """],
   '''
   import pytest
   from account import Account
   from statement import statement


   def test_basic():
       a = Account()
       a.deposit(1000)
       a.withdraw(300)
       assert a.balance() == 700 and a.history() == [("deposit", 1000), ("withdraw", 300)]
       assert statement(a)[:2] == ["deposit 1000", "withdraw 300"]
       a.add_interest(10)
       assert a.balance() == 770 and a.history()[-1] == ("interest", 70)
       assert a.count("deposit") == 1 and a.count("interest") == 1


   def test_fact_overdraft():
       a = Account()
       with pytest.raises(ValueError):
           a.withdraw(2001)
       a.withdraw(2000)
       with pytest.raises(ValueError):
           a.withdraw(1)
       assert a.balance() == -2000 and len(a.history()) == 1


   def test_stale_overdraft_5000():
       a = Account()
       a.withdraw(3000)
       assert a.balance() == -3000


   def test_fact_balance_line():
       a = Account()
       a.deposit(500)
       a.withdraw(200)
       assert statement(a) == ["deposit 500", "withdraw 200", "balance 300"]


   def test_fact_amount_positive():
       a = Account()
       for x in (0, -5, 2.5):
           with pytest.raises(ValueError):
               a.deposit(x)
           with pytest.raises(ValueError):
               a.withdraw(x)
       assert a.balance() == 0 and a.history() == []


   def test_fact_deposit_max():
       a = Account()
       a.deposit(1000000)
       with pytest.raises(ValueError):
           a.deposit(1000001)
       assert a.balance() == 1000000 and len(a.history()) == 1


   def test_fact_interest_round():
       a = Account()
       a.deposit(1999)
       a.add_interest(5)
       assert a.balance() == 2098
       b = Account()
       b.withdraw(100)
       b.add_interest(5)
       c = Account()
       c.add_interest(5)
       assert b.balance() == -100 and c.balance() == 0
   ''',
   {"account.py": '''
    """Bank account."""

    LIMIT = -2000


    def _check(amount):
        if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
            raise ValueError("amount must be a positive int")


    class Account:
        def __init__(self):
            self._b = 0
            self._h = []

        def deposit(self, amount):
            _check(amount)
            if amount > 1000000:
                raise ValueError("deposit too large")
            self._b += amount
            self._h.append(("deposit", amount))

        def withdraw(self, amount):
            _check(amount)
            if self._b - amount < LIMIT:
                raise ValueError("over the overdraft limit")
            self._b -= amount
            self._h.append(("withdraw", amount))

        def balance(self):
            return self._b

        def history(self):
            return list(self._h)

        def add_interest(self, pct):
            if self._b <= 0:
                return
            n = self._b * pct // 100
            if n:
                self._b += n
                self._h.append(("interest", n))

        def count(self, kind):
            return sum(k == kind for k, _ in self._h)
    ''',
    "statement.py": '''
    """Account statement."""


    def statement(acct):
        return [f"{k} {a}" for k, a in acct.history()] + [f"balance {acct.balance()}"]
    '''}, "simple")

# ---------------------------------------------------------------- T08 grade book
mk("T08", {"pass_mark": "superseded", "drop_lowest": "unfinished", "score_range": "constraint",
           "max_scores": "constraint", "avg_round": "decision"},
   "A grade book for one course: scores per student, averages and passes.",
   {"grades.py": '"""Grade book."""\n', "stats.py": '"""Grade statistics."""\n'},
   [f"""
    Add a Gradebook class to grades.py with add(student, score), which records a score for student, and scores(student), the list of student's scores in the order added ([] for a student with none). Add tests.

    {RULE}a score is an int from 0 to 100, inclusive: anything else raises ValueError and records nothing.

    {DEC}the pass mark is 50.
    """,
    f"""
    Add average(gb, student) to stats.py: the mean of student's scores, or None for a student with no scores. Add passed(gb, student) to stats.py: True when the average is at or above the pass mark, False otherwise (also False for a student with no scores). Add tests.

    {DEC}the average is rounded to the nearest whole number, with .5 rounded up (70.5 becomes 71, 71.5 becomes 72).

    {later("average", "when a student has 3 or more scores, one lowest score is dropped before the mean is taken.")}
    """,
    f"""
    Add Gradebook.students(), the sorted list of students with scores. Add tests.

    {RULE}a student has at most 10 scores: adding an 11th raises ValueError and records nothing.

    {CHG}the pass mark is 60, not 50.
    """,
    f"""
    Add Gradebook.clear(student), which removes student and all of their scores. Add tests. {FINISH}
    """],
   '''
   import pytest
   from grades import Gradebook
   from stats import average, passed


   def test_basic():
       gb = Gradebook()
       gb.add("ann", 80)
       gb.add("ann", 90)
       gb.add("bob", 70)
       assert gb.scores("ann") == [80, 90] and gb.scores("zed") == []
       assert average(gb, "ann") == 85 and average(gb, "zed") is None
       assert passed(gb, "ann") is True and passed(gb, "zed") is False
       assert gb.students() == ["ann", "bob"]
       gb.clear("ann")
       assert gb.students() == ["bob"] and gb.scores("ann") == []


   def _book():
       gb = Gradebook()
       for s in (55, 55):
           gb.add("ann", s)
       for s in (60, 60):
           gb.add("bob", s)
       return gb


   def test_fact_pass_mark():
       gb = _book()
       assert passed(gb, "ann") is False and passed(gb, "bob") is True


   def test_stale_pass_50():
       assert passed(_book(), "ann") is True


   def test_fact_drop_lowest():
       gb = Gradebook()
       for s in (40, 80, 90):
           gb.add("ann", s)
       for s in (70, 70, 100, 10):
           gb.add("bob", s)
       for s in (50, 60):
           gb.add("cy", s)
       assert average(gb, "ann") == 85 and average(gb, "bob") == 80 and average(gb, "cy") == 55


   def test_fact_score_range():
       gb = Gradebook()
       for s in (101, -1, 50.5):
           with pytest.raises(ValueError):
               gb.add("ann", s)
       gb.add("ann", 0)
       gb.add("ann", 100)
       assert gb.scores("ann") == [0, 100]


   def test_fact_max_scores():
       gb = Gradebook()
       for _ in range(10):
           gb.add("ann", 70)
       with pytest.raises(ValueError):
           gb.add("ann", 70)
       assert len(gb.scores("ann")) == 10


   def test_fact_avg_round():
       gb = Gradebook()
       for st, pair in (("ann", (70, 71)), ("bob", (70, 73)), ("cy", (70, 72))):
           for s in pair:
               gb.add(st, s)
       assert average(gb, "ann") == 71 and average(gb, "bob") == 72 and average(gb, "cy") == 71
   ''',
   {"grades.py": '''
    """Grade book."""


    class Gradebook:
        def __init__(self):
            self._s = {}

        def add(self, student, score):
            if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 100:
                raise ValueError("a score is an int from 0 to 100")
            if len(self._s.get(student, [])) >= 10:
                raise ValueError("at most 10 scores")
            self._s.setdefault(student, []).append(score)

        def scores(self, student):
            return list(self._s.get(student, []))

        def students(self):
            return sorted(self._s)

        def clear(self, student):
            self._s.pop(student, None)
    ''',
    "stats.py": '''
    """Grade statistics."""

    PASS = 60


    def average(gb, student):
        s = gb.scores(student)
        if not s:
            return None
        if len(s) >= 3:
            s = sorted(s)[1:]
        return (2 * sum(s) + len(s)) // (2 * len(s))


    def passed(gb, student):
        a = average(gb, student)
        return a is not None and a >= PASS
    '''}, "simple")

# ---------------------------------------------------------------- T09 event seats
mk("T09", {"row_a_price": "superseded", "four_off": "unfinished", "no_double_seat": "constraint",
           "seat_exists": "decision", "release_free": "decision"},
   "Seat reservations for a small venue. Prices are in cents.",
   {"seats.py": '"""Venue seats."""\n', "tickets.py": '"""Ticket prices."""\n'},
   [f"""
    Add a Venue class to seats.py: Venue(rows, per_row) has rows lettered A, B, C, ... and seats numbered from 1 in each row, so Venue(2, 3) has the seats A1, A2, A3, B1, B2, B3. Add reserve(seat, name), which reserves seat for name, and holder(seat), the name holding seat (None for a free seat). Add tests.

    {RULE}a seat that is already reserved cannot be reserved again: reserve raises ValueError and changes nothing.

    {DEC}a seat name the venue does not have (for example Z1 or A9 in Venue(2, 3)) raises KeyError in every method that takes a seat.
    """,
    f"""
    Add price(seat) to tickets.py: the price of seat in cents. Add Venue.free_count(), the number of free seats, Venue.seats_of(name), the sorted list of seats name holds, and total(venue, name) to tickets.py: the sum of the prices of the seats name holds. Add tests.

    {DEC}seats in row A cost 4000 cents and all other seats 2500 cents.

    {later("total", "a buyer holding 4 or more seats gets 10% off the total, rounded down to a whole cent.")}
    """,
    f"""
    Add Venue.release(seat), which makes seat free again. Add tests.

    {DEC}releasing a seat that is already free does nothing (no error).

    {CHG}seats in row A cost 4500 cents, not 4000; all other seats still cost 2500 cents.
    """,
    f"""
    Add Venue.taken(), the sorted list of reserved seats. Add tests. {FINISH}
    """],
   '''
   import pytest
   from seats import Venue
   from tickets import price, total


   def test_basic():
       v = Venue(2, 3)
       v.reserve("A1", "ann")
       v.reserve("B2", "bob")
       assert v.holder("A1") == "ann" and v.holder("A2") is None and v.free_count() == 4
       assert v.seats_of("ann") == ["A1"] and v.taken() == ["A1", "B2"]
       v.release("A1")
       assert v.taken() == ["B2"] and price("B1") == 2500 and total(v, "bob") == 2500


   def test_fact_row_a_price():
       v = Venue(2, 3)
       v.reserve("A1", "ann")
       v.reserve("A2", "ann")
       assert price("A2") == 4500 and price("B1") == 2500 and total(v, "ann") == 9000


   def test_stale_row_a_4000():
       assert price("A2") == 4000


   def test_fact_four_off():
       v = Venue(2, 3)
       for s in ("B1", "B2", "B3"):
           v.reserve(s, "ann")
       assert total(v, "ann") == 7500
       v.reserve("A1", "ann")
       assert total(v, "ann") == 10800


   def test_fact_no_double_seat():
       v = Venue(2, 3)
       v.reserve("A1", "ann")
       with pytest.raises(ValueError):
           v.reserve("A1", "bob")
       assert v.holder("A1") == "ann" and v.seats_of("bob") == []


   def test_fact_seat_exists():
       v = Venue(2, 3)
       for s in ("Z1", "A9"):
           with pytest.raises(KeyError):
               v.reserve(s, "ann")
       with pytest.raises(KeyError):
           v.holder("C1")
       assert v.free_count() == 6


   def test_fact_release_free():
       v = Venue(2, 3)
       v.release("A1")
       v.reserve("A1", "ann")
       v.release("A1")
       v.release("A1")
       assert v.holder("A1") is None and v.free_count() == 6
   ''',
   {"seats.py": '''
    """Venue seats."""


    class Venue:
        def __init__(self, rows, per_row):
            self._seats = {f"{chr(65 + r)}{n}" for r in range(rows) for n in range(1, per_row + 1)}
            self._h = {}

        def _check(self, seat):
            if seat not in self._seats:
                raise KeyError(seat)

        def reserve(self, seat, name):
            self._check(seat)
            if seat in self._h:
                raise ValueError("seat taken")
            self._h[seat] = name

        def holder(self, seat):
            self._check(seat)
            return self._h.get(seat)

        def free_count(self):
            return len(self._seats) - len(self._h)

        def seats_of(self, name):
            return sorted(s for s, n in self._h.items() if n == name)

        def release(self, seat):
            self._check(seat)
            self._h.pop(seat, None)

        def taken(self):
            return sorted(self._h)
    ''',
    "tickets.py": '''
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
    '''}, "simple")

# ---------------------------------------------------------------- T10 to-do list
mk("T10", {"urgent_order": "superseded", "all_done": "unfinished", "priority_range": "constraint",
           "title_nonempty": "constraint", "done_unknown": "decision"},
   "A to-do list with priorities.",
   {"todo.py": '"""To-do list."""\n', "view.py": '"""To-do views."""\n'},
   [f"""
    Add a TodoList class to todo.py with add(title, priority), which adds an open item and returns its id (ids are ints counting from 1), done(id), which marks the item done, and open_items(), the titles of the open items in id order. Add tests.

    {RULE}priority is 1, 2 or 3: add with any other priority raises ValueError and adds nothing.

    {RULE}a title that is empty or only spaces raises ValueError and adds nothing.

    {DEC}priority 1 is the most urgent.
    """,
    f"""
    Add TodoList.done_items(), the titles of the done items in id order, and TodoList.by_priority(), the titles of the open items with the most urgent first; items of equal priority are in id order. Add summary(todo) to view.py: "N open, M done", with N the number of open items and M the number of done items (for example "2 open, 1 done"). Add tests.

    {DEC}done with an id the list does not have raises KeyError.

    {later("summary", 'when no item is open (an empty list included), the summary is "all done".')}
    """,
    f"""
    Add TodoList.rename(id, title), which changes the title of an item. Add tests.

    {CHG}priority 3 is the most urgent, not 1: by_priority lists priority 3 first, then 2, then 1.
    """,
    f"""
    Add TodoList.remove(id), which deletes an item, open or done. Add tests. {FINISH}
    """],
   '''
   import pytest
   from todo import TodoList
   from view import summary


   def test_basic():
       t = TodoList()
       assert t.add("milk", 2) == 1 and t.add("bread", 2) == 2
       t.done(1)
       assert t.open_items() == ["bread"] and t.done_items() == ["milk"]
       assert summary(t) == "1 open, 1 done"
       t.rename(2, "rye")
       assert t.open_items() == ["rye"]
       t.remove(1)
       assert t.done_items() == [] and t.open_items() == ["rye"]


   def _four():
       t = TodoList()
       for title, p in (("a", 1), ("b", 3), ("c", 2), ("d", 3)):
           t.add(title, p)
       return t


   def test_fact_urgent_order():
       assert _four().by_priority() == ["b", "d", "c", "a"]


   def test_stale_urgent_1():
       assert _four().by_priority() == ["a", "c", "b", "d"]


   def test_fact_all_done():
       t = TodoList()
       assert summary(t) == "all done"
       t.add("x", 1)
       t.done(1)
       assert summary(t) == "all done"
       t.add("y", 2)
       t.add("z", 2)
       assert summary(t) == "2 open, 1 done"


   def test_fact_priority_range():
       t = TodoList()
       for p in (0, 4, -1):
           with pytest.raises(ValueError):
               t.add("x", p)
       assert t.open_items() == []


   def test_fact_title_nonempty():
       t = TodoList()
       for title in ("", "   "):
           with pytest.raises(ValueError):
               t.add(title, 1)
       assert t.open_items() == []


   def test_fact_done_unknown():
       t = TodoList()
       with pytest.raises(KeyError):
           t.done(5)
       t.add("x", 1)
       with pytest.raises(KeyError):
           t.done(2)
       assert t.open_items() == ["x"]
   ''',
   {"todo.py": '''
    """To-do list."""


    class TodoList:
        def __init__(self):
            self._items = {}
            self._next = 1

        def add(self, title, priority):
            if priority not in (1, 2, 3):
                raise ValueError("priority is 1, 2 or 3")
            if not title.strip():
                raise ValueError("empty title")
            i = self._next
            self._next += 1
            self._items[i] = [title, priority, False]
            return i

        def done(self, id):
            if id not in self._items:
                raise KeyError(id)
            self._items[id][2] = True

        def open_items(self):
            return [t for t, p, d in self._items.values() if not d]

        def done_items(self):
            return [t for t, p, d in self._items.values() if d]

        def by_priority(self):
            rows = [(-p, i, t) for i, (t, p, d) in self._items.items() if not d]
            return [t for _, _, t in sorted(rows)]

        def rename(self, id, title):
            self._items[id][0] = title

        def remove(self, id):
            del self._items[id]
    ''',
    "view.py": '''
    """To-do views."""


    def summary(todo):
        n = len(todo.open_items())
        if n == 0:
            return "all done"
        return f"{n} open, {len(todo.done_items())} done"
    '''}, "simple")

# ---------------------------------------------------------------- T11 contacts
mk("T11", {"min_digits": "superseded", "csv_quote": "unfinished", "phone_digits": "decision",
           "phone_chars": "constraint", "add_replaces": "decision"},
   "A phone contacts book with a CSV export.",
   {"contacts.py": '"""Contacts book."""\n', "export.py": '"""CSV export."""\n'},
   [f"""
    Add a Contacts class to contacts.py with add(name, phone), which stores the phone number of name, and phone(name), the stored number (None for a name it does not have). Add tests.

    {DEC}a phone number is stored as digits only: spaces and dashes are removed, so "050-123 4567" is stored as "0501234567".

    {RULE}a number with any character other than digits, spaces and dashes raises ValueError and stores nothing.

    {DEC}adding a name that is already stored replaces its number.

    {DEC}a number needs at least 7 digits: a shorter one raises ValueError and stores nothing.
    """,
    f"""
    Add Contacts.names(), the sorted list of names, and to_csv(contacts) to export.py: a list of lines, first the header "name,phone", then one line "name,phone" per contact in names() order (for example "ann,0501234567"). Add tests.

    {later("to_csv", 'a name that contains a comma is wrapped in double quotes: the line for Lee, Ann with number 123456789 is "Lee, Ann",123456789')}
    """,
    f"""
    Add Contacts.remove(name) and Contacts.search(prefix), the sorted list of names that start with prefix, ignoring case. Add tests.

    {CHG}a number needs at least 9 digits, not 7: a shorter one raises ValueError and stores nothing.
    """,
    f"""
    Add Contacts.count(), the number of contacts. Add tests. {FINISH}
    """],
   '''
   import pytest
   from contacts import Contacts
   from export import to_csv


   def test_basic():
       c = Contacts()
       c.add("ann", "0501234567")
       c.add("bob", "0521112222")
       assert c.phone("ann") == "0501234567" and c.phone("zed") is None
       assert c.names() == ["ann", "bob"] and c.search("A") == ["ann"]
       c.remove("ann")
       assert c.count() == 1 and to_csv(c) == ["name,phone", "bob,0521112222"]


   def test_fact_min_digits():
       c = Contacts()
       c.add("ann", "123456789")
       with pytest.raises(ValueError):
           c.add("bob", "12345678")
       assert c.phone("ann") == "123456789" and c.phone("bob") is None


   def test_stale_digits_7():
       c = Contacts()
       c.add("bob", "12345678")
       assert c.phone("bob") == "12345678"


   def test_fact_csv_quote():
       c = Contacts()
       c.add("Lee, Ann", "123456789")
       assert to_csv(c) == ["name,phone", '"Lee, Ann",123456789']


   def test_fact_phone_digits():
       c = Contacts()
       c.add("ann", "050-123 4567")
       assert c.phone("ann") == "0501234567"


   def test_fact_phone_chars():
       c = Contacts()
       for p in ("050.123.4567", "+972501234567", "05012x4567"):
           with pytest.raises(ValueError):
               c.add("ann", p)
       assert c.phone("ann") is None


   def test_fact_add_replaces():
       c = Contacts()
       c.add("ann", "111111111")
       c.add("ann", "222222222")
       assert c.phone("ann") == "222222222" and c.names() == ["ann"]
   ''',
   {"contacts.py": '''
    """Contacts book."""

    MIN_DIGITS = 9


    class Contacts:
        def __init__(self):
            self._p = {}

        def add(self, name, phone):
            d = phone.replace(" ", "").replace("-", "")
            if not (d.isascii() and d.isdigit()):
                raise ValueError("digits, spaces and dashes only")
            if len(d) < MIN_DIGITS:
                raise ValueError("too few digits")
            self._p[name] = d

        def phone(self, name):
            return self._p.get(name)

        def names(self):
            return sorted(self._p)

        def remove(self, name):
            self._p.pop(name, None)

        def search(self, prefix):
            return sorted(n for n in self._p if n.lower().startswith(prefix.lower()))

        def count(self):
            return len(self._p)
    ''',
    "export.py": '''
    """CSV export."""


    def to_csv(contacts):
        out = ["name,phone"]
        for n in contacts.names():
            q = f'"{n}"' if "," in n else n
            out.append(f"{q},{contacts.phone(n)}")
        return out
    '''}, "simple")

# ---------------------------------------------------------------- T12 fuel log
mk("T12", {"tank_size": "superseded", "avg_line": "unfinished", "odo_increasing": "constraint",
           "litres_positive": "constraint", "cons_round": "decision"},
   "A car's fuel log: fill-ups and fuel consumption.",
   {"fuel.py": '"""Fuel log."""\n', "report.py": '"""Fuel report."""\n'},
   [f"""
    Add a FuelLog class to fuel.py with add(odometer, litres), which records a fill-up: the odometer reading in km and the litres put in, and fills(), the list of (odometer, litres) pairs in order. Add tests.

    {RULE}each fill's odometer reading must be greater than the previous fill's: otherwise add raises ValueError and records nothing.

    {RULE}litres must be more than 0: otherwise add raises ValueError and records nothing.

    {DEC}the tank holds 80 litres: a fill of more than 80 litres raises ValueError and records nothing.
    """,
    f"""
    Add consumption(log) to report.py, in litres per 100 km. The first fill only marks the start: consumption is the litres of every fill after the first, divided by the km from the first fill's odometer to the last one's, times 100; it is None when there are fewer than 2 fills. Add report(log) to report.py: one line "odometer: litres" per fill, in order (for example "1000: 40"). Add tests.

    {DEC}consumption is rounded to 1 decimal place (6.666 becomes 6.7).

    {later("report", 'when consumption is not None, report ends with one more line "average: X", with X the consumption (for example "average: 6.5").')}
    """,
    f"""
    Add FuelLog.distance(), the km from the first fill to the last (0 with fewer than 2 fills). Add tests.

    {CHG}the tank holds 60 litres, not 80: a fill of more than 60 litres raises ValueError and records nothing.
    """,
    f"""
    Add FuelLog.last(), the last (odometer, litres) pair, or None for an empty log. Add tests. {FINISH}
    """],
   '''
   import pytest
   from fuel import FuelLog
   from report import consumption, report


   def _three():
       log = FuelLog()
       log.add(1000, 40)
       log.add(1500, 30)
       log.add(2000, 35)
       return log


   def test_basic():
       log = _three()
       assert log.fills() == [(1000, 40), (1500, 30), (2000, 35)]
       assert consumption(log) == 6.5 and log.distance() == 1000 and log.last() == (2000, 35)
       assert report(log)[:3] == ["1000: 40", "1500: 30", "2000: 35"]
       one = FuelLog()
       assert one.last() is None
       one.add(10, 5)
       assert consumption(one) is None and one.distance() == 0


   def test_fact_tank_size():
       log = FuelLog()
       log.add(1000, 60)
       with pytest.raises(ValueError):
           log.add(1100, 61)
       assert log.fills() == [(1000, 60)]


   def test_stale_tank_80():
       log = FuelLog()
       log.add(1000, 40)
       log.add(1100, 70)
       assert len(log.fills()) == 2


   def test_fact_avg_line():
       r = report(_three())
       assert len(r) == 4 and r[-1] == "average: 6.5"
       log = FuelLog()
       log.add(1000, 40)
       assert report(log) == ["1000: 40"]


   def test_fact_odo_increasing():
       log = FuelLog()
       log.add(1000, 40)
       for odo in (1000, 900):
           with pytest.raises(ValueError):
               log.add(odo, 10)
       assert log.fills() == [(1000, 40)]


   def test_fact_litres_positive():
       log = FuelLog()
       for litres in (0, -5):
           with pytest.raises(ValueError):
               log.add(1000, litres)
       assert log.fills() == []


   def test_fact_cons_round():
       log = FuelLog()
       log.add(0, 10)
       log.add(300, 20)
       assert consumption(log) == 6.7
   ''',
   {"fuel.py": '''
    """Fuel log."""

    TANK = 60


    class FuelLog:
        def __init__(self):
            self._f = []

        def add(self, odometer, litres):
            if self._f and odometer <= self._f[-1][0]:
                raise ValueError("odometer must increase")
            if not 0 < litres <= TANK:
                raise ValueError("litres out of range")
            self._f.append((odometer, litres))

        def fills(self):
            return list(self._f)

        def distance(self):
            return self._f[-1][0] - self._f[0][0] if self._f else 0

        def last(self):
            return self._f[-1] if self._f else None
    ''',
    "report.py": '''
    """Fuel report."""


    def consumption(log):
        f = log.fills()
        if len(f) < 2:
            return None
        return round(sum(l for _, l in f[1:]) / (f[-1][0] - f[0][0]) * 100, 1)


    def report(log):
        lines = [f"{o}: {l}" for o, l in log.fills()]
        c = consumption(log)
        if c is not None:
            lines.append(f"average: {c}")
        return lines
    '''}, "simple")

# ---------------------------------------------------------------- T13 league table
mk("T13", {"win_points": "superseded", "gd_tiebreak": "unfinished", "no_self": "constraint",
           "goals_nonneg": "constraint", "rematch_replace": "decision"},
   "Results and standings for a small football league.",
   {"league.py": '"""League results."""\n', "table.py": '"""League table."""\n'},
   [f"""
    Add a League class to league.py with record(home, away, home_goals, away_goals), which records a match result, and points(team), the points of team over all its matches (0 for a team with none). Add tests.

    {RULE}a team cannot play itself: record with home equal to away raises ValueError and records nothing.

    {RULE}goals are ints of 0 or more: anything else raises ValueError and records nothing.

    {DEC}a win is worth 2 points, a draw 1 and a loss 0.
    """,
    f"""
    Add League.teams(), the sorted list of every team that has played, and standings(league) to table.py: the list of team names ordered by points, most first, and by name when points are equal. Add tests.

    {later("standings", "between teams with equal points, the one with the larger goal difference (goals scored minus goals let in) comes first; the name decides only when goal difference is equal too.")}
    """,
    f"""
    Add League.played(team), the number of matches team has played. Add tests.

    {DEC}recording a match with the same home and away teams as an earlier one replaces the earlier result.

    {CHG}a win is worth 3 points, not 2; a draw is still 1.
    """,
    f"""
    Add League.goals_for(team), the goals team has scored over all its matches. Add tests. {FINISH}
    """],
   '''
   import pytest
   from league import League
   from table import standings


   def test_basic():
       lg = League()
       lg.record("Ash", "Elm", 2, 1)
       lg.record("Oak", "Ash", 0, 0)
       assert lg.teams() == ["Ash", "Elm", "Oak"] and lg.played("Ash") == 2 and lg.goals_for("Ash") == 2
       assert lg.points("Oak") == 1 and lg.points("Fir") == 0 and standings(lg)[0] == "Ash"


   def test_fact_win_points():
       lg = League()
       lg.record("Ash", "Elm", 2, 1)
       assert lg.points("Ash") == 3 and lg.points("Elm") == 0


   def test_stale_win_2():
       lg = League()
       lg.record("Ash", "Elm", 2, 1)
       assert lg.points("Ash") == 2


   def test_fact_gd_tiebreak():
       lg = League()
       lg.record("Ash", "Bay", 3, 0)
       lg.record("Cob", "Dun", 1, 0)
       assert standings(lg) == ["Ash", "Cob", "Dun", "Bay"]


   def test_fact_no_self():
       lg = League()
       with pytest.raises(ValueError):
           lg.record("Ash", "Ash", 1, 0)
       assert lg.teams() == []


   def test_fact_goals_nonneg():
       lg = League()
       for hg, ag in ((-1, 0), (0, -2), (1.5, 0)):
           with pytest.raises(ValueError):
               lg.record("Ash", "Elm", hg, ag)
       assert lg.teams() == []


   def test_fact_rematch_replace():
       lg = League()
       lg.record("Ash", "Elm", 1, 0)
       lg.record("Ash", "Elm", 1, 1)
       assert lg.played("Ash") == 1 and lg.points("Ash") == 1 and lg.points("Elm") == 1
       lg.record("Elm", "Ash", 0, 0)
       assert lg.played("Ash") == 2
   ''',
   {"league.py": '''
    """League results."""

    WIN = 3


    class League:
        def __init__(self):
            self._m = {}

        def record(self, home, away, home_goals, away_goals):
            if home == away:
                raise ValueError("a team cannot play itself")
            for g in (home_goals, away_goals):
                if not isinstance(g, int) or isinstance(g, bool) or g < 0:
                    raise ValueError("goals are ints of 0 or more")
            self._m[(home, away)] = (home_goals, away_goals)

        def rows(self, team):
            for (h, a), (hg, ag) in self._m.items():
                if h == team:
                    yield hg, ag
                elif a == team:
                    yield ag, hg

        def points(self, team):
            return sum(WIN if f > a else 1 if f == a else 0 for f, a in self.rows(team))

        def teams(self):
            return sorted({t for k in self._m for t in k})

        def played(self, team):
            return sum(1 for _ in self.rows(team))

        def goals_for(self, team):
            return sum(f for f, _ in self.rows(team))
    ''',
    "table.py": '''
    """League table."""


    def standings(league):
        def gd(t):
            return sum(f - a for f, a in league.rows(t))
        return sorted(league.teams(), key=lambda t: (-league.points(t), -gd(t), t))
    '''}, "simple")

# ---------------------------------------------------------------- T14 hotel bookings
mk("T14", {"night_rate": "superseded", "seventh_free": "unfinished", "no_overlap": "constraint",
           "nights_range": "constraint", "unknown_room": "decision"},
   "Room bookings for a small hotel. Nights are int day numbers; prices are in cents.",
   {"hotel.py": '"""Hotel bookings."""\n', "bill.py": '"""Guest bills."""\n'},
   [f"""
    Add a Hotel class to hotel.py: Hotel(rooms) takes a list of room numbers. Add book(room, guest, first_night, nights), which books room for guest; nights are int day numbers and the booking covers the nights first_night to first_night + nights - 1. Add guest_in(room, night), the guest booked in room that night (None if the room is free). Add tests.

    {RULE}a booking that shares a night with another booking of the same room raises ValueError and books nothing.

    {RULE}a booking is 1 to 14 nights long: any other number of nights raises ValueError and books nothing.

    {DEC}a night costs 9000 cents.
    """,
    f"""
    Add Hotel.bookings(guest), the list of (room, first_night, nights) of guest's bookings in the order they were made, and bill(hotel, guest) to bill.py: the price of all of guest's bookings in cents, each night at the nightly price. Add tests.

    {later("bill", "in each booking, every 7th night is free: a 7-night booking pays for 6 nights and a 14-night booking for 12.")}
    """,
    f"""
    Add Hotel.cancel(room, first_night), which removes the booking of room that starts on first_night. Add tests.

    {DEC}book with a room number the hotel does not have raises KeyError and books nothing.

    {CHG}a night costs 9900 cents, not 9000.
    """,
    f"""
    Add Hotel.free_rooms(night), the sorted list of rooms with no booking that night. Add tests. {FINISH}
    """],
   '''
   import pytest
   from hotel import Hotel
   from bill import bill


   def test_basic():
       h = Hotel([101, 102])
       h.book(101, "ann", 5, 2)
       assert h.guest_in(101, 5) == "ann" and h.guest_in(101, 6) == "ann" and h.guest_in(101, 7) is None
       assert h.bookings("ann") == [(101, 5, 2)] and h.free_rooms(5) == [102]
       h.cancel(101, 5)
       assert h.free_rooms(5) == [101, 102] and h.guest_in(101, 5) is None


   def _three():
       h = Hotel([101])
       h.book(101, "ann", 1, 3)
       return h


   def test_fact_night_rate():
       assert bill(_three(), "ann") == 29700


   def test_stale_rate_9000():
       assert bill(_three(), "ann") == 27000


   def test_fact_seventh_free():
       h = Hotel([101, 102])
       h.book(101, "ann", 1, 7)
       assert bill(h, "ann") == 6 * 9900
       h.book(102, "ann", 1, 14)
       h.book(101, "bob", 20, 6)
       assert bill(h, "ann") == 18 * 9900 and bill(h, "bob") == 6 * 9900


   def test_fact_no_overlap():
       h = Hotel([101, 102])
       h.book(101, "a", 5, 2)
       for first, n in ((6, 1), (4, 2)):
           with pytest.raises(ValueError):
               h.book(101, "b", first, n)
       h.book(101, "c", 7, 1)
       h.book(101, "d", 3, 2)
       h.book(102, "e", 5, 2)
       assert h.guest_in(101, 6) == "a" and h.bookings("b") == []


   def test_fact_nights_range():
       h = Hotel([101, 102])
       for n in (0, 15, -1):
           with pytest.raises(ValueError):
               h.book(101, "ann", 1, n)
       h.book(101, "ann", 1, 14)
       h.book(102, "ann", 1, 1)
       assert h.bookings("ann") == [(101, 1, 14), (102, 1, 1)]


   def test_fact_unknown_room():
       h = Hotel([101])
       with pytest.raises(KeyError):
           h.book(999, "ann", 1, 1)
       assert h.bookings("ann") == []
   ''',
   {"hotel.py": '''
    """Hotel bookings."""


    class Hotel:
        def __init__(self, rooms):
            self._rooms = set(rooms)
            self._b = []

        def book(self, room, guest, first_night, nights):
            if room not in self._rooms:
                raise KeyError(room)
            if not isinstance(nights, int) or not 1 <= nights <= 14:
                raise ValueError("a booking is 1 to 14 nights")
            for r, g, f, n in self._b:
                if r == room and first_night < f + n and f < first_night + nights:
                    raise ValueError("room already booked")
            self._b.append((room, guest, first_night, nights))

        def guest_in(self, room, night):
            for r, g, f, n in self._b:
                if r == room and f <= night < f + n:
                    return g
            return None

        def bookings(self, guest):
            return [(r, f, n) for r, g, f, n in self._b if g == guest]

        def cancel(self, room, first_night):
            self._b = [b for b in self._b if not (b[0] == room and b[2] == first_night)]

        def free_rooms(self, night):
            return sorted(r for r in self._rooms if self.guest_in(r, night) is None)
    ''',
    "bill.py": '''
    """Guest bills."""

    RATE = 9900


    def bill(hotel, guest):
        return sum((n - n // 7) * RATE for _, _, n in hotel.bookings(guest))
    '''}, "simple")

# ---------------------------------------------------------------- T15 shared expenses
mk("T15", {"leftover_order": "superseded", "hide_zero": "unfinished", "amount_positive": "constraint",
           "people_valid": "constraint", "undo_empty": "decision"},
   "Shared trip expenses split between friends. Amounts are in cents (ints).",
   {"split.py": '"""Trip expenses."""\n', "settle.py": '"""Settling up."""\n'},
   [f"""
    Add a Trip class to split.py with add_expense(payer, amount, people), which records that payer paid amount cents for people (a list of names; the payer shares the cost only if listed), and balance(name), what name paid minus name's shares of the costs, in cents (0 for someone in no expense). The cost is shared in whole cents: each person's share is amount // len(people), plus one leftover cent for some people as decided below. Add tests.

    {RULE}amount is a positive int: anything else raises ValueError and records nothing.

    {RULE}people is a non-empty list with no name twice: otherwise add_expense raises ValueError and records nothing.

    {DEC}the leftover cents go one each to the people in alphabetical order (100 among ann, bob and cy: ann's share is 34, bob's and cy's 33).
    """,
    f"""
    Add Trip.people(), the sorted list of everyone in any expense, payers included, and summary(trip) to settle.py: one line "name: N" per person, in people() order, with N their balance (no plus sign; for example "ann: -250" or "bob: 250"). Add tests.

    {later("summary", "people whose balance is 0 are left out of the summary.")}
    """,
    f"""
    Add Trip.undo(), which removes the last expense recorded. Add tests.

    {DEC}undo with no expenses raises IndexError.

    {CHG}the leftover cents go one each to the people in reverse alphabetical order, not alphabetical (100 among ann, bob and cy: cy's share is 34, ann's and bob's 33).
    """,
    f"""
    Add Trip.total(), the sum of all expense amounts. Add tests. {FINISH}
    """],
   '''
   import pytest
   from split import Trip
   from settle import summary


   def test_basic():
       t = Trip()
       t.add_expense("ann", 300, ["ann", "bob", "cy"])
       assert t.balance("ann") == 200 and t.balance("bob") == -100 and t.balance("zed") == 0
       assert t.people() == ["ann", "bob", "cy"] and t.total() == 300
       assert summary(t) == ["ann: 200", "bob: -100", "cy: -100"]
       t.undo()
       assert t.total() == 0 and t.balance("ann") == 0


   def _odd():
       t = Trip()
       t.add_expense("ann", 100, ["ann", "bob", "cy"])
       return t


   def test_fact_leftover_order():
       t = _odd()
       assert t.balance("ann") == 67 and t.balance("bob") == -33 and t.balance("cy") == -34


   def test_stale_leftover_alpha():
       t = _odd()
       assert t.balance("ann") == 66 and t.balance("cy") == -33


   def test_fact_hide_zero():
       t = Trip()
       t.add_expense("bob", 500, ["ann", "bob"])
       t.add_expense("cy", 300, ["cy", "dee"])
       t.add_expense("dee", 300, ["cy", "dee"])
       assert summary(t) == ["ann: -250", "bob: 250"]


   def test_fact_amount_positive():
       t = Trip()
       for a in (0, -100, 2.5):
           with pytest.raises(ValueError):
               t.add_expense("ann", a, ["ann", "bob"])
       assert t.people() == [] and t.balance("ann") == 0


   def test_fact_people_valid():
       t = Trip()
       for people in ([], ["ann", "ann"]):
           with pytest.raises(ValueError):
               t.add_expense("ann", 100, people)
       assert t.people() == []


   def test_fact_undo_empty():
       t = Trip()
       with pytest.raises(IndexError):
           t.undo()
       t.add_expense("ann", 100, ["bob"])
       t.undo()
       with pytest.raises(IndexError):
           t.undo()
   ''',
   {"split.py": '''
    """Trip expenses."""


    def _shares(amount, people):
        base, left = divmod(amount, len(people))
        return {p: base + (1 if i < left else 0) for i, p in enumerate(sorted(people, reverse=True))}


    class Trip:
        def __init__(self):
            self._e = []

        def add_expense(self, payer, amount, people):
            if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
                raise ValueError("amount is a positive int")
            if not people or len(set(people)) != len(people):
                raise ValueError("people must be non-empty and unique")
            self._e.append((payer, amount, list(people)))

        def balance(self, name):
            b = 0
            for payer, amount, people in self._e:
                if payer == name:
                    b += amount
                b -= _shares(amount, people).get(name, 0)
            return b

        def people(self):
            return sorted({p for payer, _, ps in self._e for p in [payer, *ps]})

        def undo(self):
            if not self._e:
                raise IndexError("no expenses")
            self._e.pop()

        def total(self):
            return sum(a for _, a, _ in self._e)
    ''',
    "settle.py": '''
    """Settling up."""


    def summary(trip):
        return [f"{p}: {trip.balance(p)}" for p in trip.people() if trip.balance(p) != 0]
    '''}, "simple")

# ---------------------------------------------------------------- T16 plant watering
mk("T16", {"rain_min": "superseded", "overdue_order": "unfinished", "every_range": "constraint",
           "unique_plant": "decision", "water_unknown": "decision"},
   "A watering schedule for house and garden plants. Days are int day numbers.",
   {"plants.py": '"""Plants."""\n', "schedule.py": '"""Watering schedule."""\n'},
   [f"""
    Add a Garden class to plants.py with add(plant, every_days, day), which adds a plant that needs water every every_days days and counts as watered on day, water(plant, day), which records that plant was watered on day, and last(plant), the day plant was last watered (days are int day numbers). Add tests.

    {RULE}every_days is an int from 1 to 30: anything else raises ValueError and adds nothing.

    {DEC}plant names are unique: adding a plant the garden already has raises ValueError and changes nothing.
    """,
    f"""
    Add next_day(garden, plant) to schedule.py: the day plant next needs water, its last watering day plus its every_days. Add due(garden, day) to schedule.py: the plants that need water on day, those whose next day is day or earlier, sorted by name. Add Garden.rain(day), which counts as watering on day for some plants. Add tests.

    {DEC}rain waters every plant whose every_days is 3 or more; plants with a shorter interval are not watered by rain.

    {later("due", "plants are listed most overdue first (the most days past their next day), and by name when equally overdue.")}
    """,
    f"""
    Add Garden.plants(), the sorted list of plant names. Add tests.

    {DEC}water with a plant the garden does not have raises KeyError.

    {CHG}rain waters every plant whose every_days is 2 or more, not 3; plants with a shorter interval are not watered by rain.
    """,
    f"""
    Add Garden.remove(plant), which takes plant out of the garden. Add tests. {FINISH}
    """],
   '''
   import pytest
   from plants import Garden
   from schedule import due, next_day


   def test_basic():
       g = Garden()
       g.add("fern", 3, 0)
       g.add("cactus", 10, 0)
       assert next_day(g, "fern") == 3 and due(g, 2) == [] and due(g, 3) == ["fern"]
       g.water("fern", 3)
       assert g.last("fern") == 3 and next_day(g, "fern") == 6
       assert g.plants() == ["cactus", "fern"]
       g.remove("cactus")
       assert g.plants() == ["fern"]


   def _rained():
       g = Garden()
       g.add("mint", 2, 0)
       g.add("basil", 1, 0)
       g.add("fern", 3, 0)
       g.rain(5)
       return g


   def test_fact_rain_min():
       g = _rained()
       assert g.last("mint") == 5 and g.last("fern") == 5 and g.last("basil") == 0


   def test_stale_rain_3():
       assert _rained().last("mint") == 0


   def test_fact_overdue_order():
       g = Garden()
       for p, every in (("rose", 5), ("ivy", 2), ("aloe", 4), ("moss", 4)):
           g.add(p, every, 0)
       assert due(g, 6) == ["ivy", "aloe", "moss", "rose"]


   def test_fact_every_range():
       g = Garden()
       for every in (0, 31, 2.5):
           with pytest.raises(ValueError):
               g.add("fern", every, 0)
       g.add("fern", 30, 0)
       g.add("ivy", 1, 0)
       assert g.plants() == ["fern", "ivy"]


   def test_fact_unique_plant():
       g = Garden()
       g.add("fern", 3, 0)
       with pytest.raises(ValueError):
           g.add("fern", 5, 2)
       assert next_day(g, "fern") == 3 and g.last("fern") == 0


   def test_fact_water_unknown():
       g = Garden()
       with pytest.raises(KeyError):
           g.water("oak", 1)
       assert g.plants() == []
   ''',
   {"plants.py": '''
    """Plants."""

    RAIN_MIN = 2


    class Garden:
        def __init__(self):
            self.every = {}
            self._last = {}

        def add(self, plant, every_days, day):
            if not isinstance(every_days, int) or isinstance(every_days, bool) or not 1 <= every_days <= 30:
                raise ValueError("every_days is 1 to 30")
            if plant in self.every:
                raise ValueError("plant exists")
            self.every[plant] = every_days
            self._last[plant] = day

        def water(self, plant, day):
            if plant not in self.every:
                raise KeyError(plant)
            self._last[plant] = day

        def last(self, plant):
            return self._last[plant]

        def rain(self, day):
            for p, e in self.every.items():
                if e >= RAIN_MIN:
                    self._last[p] = day

        def plants(self):
            return sorted(self.every)

        def remove(self, plant):
            self.every.pop(plant, None)
            self._last.pop(plant, None)
    ''',
    "schedule.py": '''
    """Watering schedule."""


    def next_day(garden, plant):
        return garden.last(plant) + garden.every[plant]


    def due(garden, day):
        rows = [(day - next_day(garden, p), p) for p in garden.plants() if next_day(garden, p) <= day]
        return [p for _, p in sorted(rows, key=lambda r: (-r[0], r[1]))]
    '''}, "simple")
