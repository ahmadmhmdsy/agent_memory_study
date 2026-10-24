"""R-014 scored projects L05-L08 (v3 form: 8 sessions, 12 facts)."""
from long_common import CHG, DEC, FINISH, RULE, g, later, mk

# ---------------------------------------------------------------- L05 library loans
mk("L05", {"loan_days": "superseded", "fine_rate": "superseded", "date_iso": "superseded",
           "isbn_hyphens": "unfinished", "search_sorted": "unfinished", "member_ascii": "unfinished",
           "member_case": "constraint", "max_loans": "constraint", "double_loan": "constraint",
           "return_unknown": "decision", "fine_cap": "decision", "export_header": "decision"},
   "Loan helpers for a small lending library.",
   {"catalog.py": '"""Book catalog."""\n', "loans.py": '"""Book loans."""\n',
    "fines.py": '"""Late fines."""\n', "export.py": '"""Loan export."""\n'},
   [f"""
    Add normalize_isbn(s) to catalog.py: a string of exactly 13 digits is returned as it is; anything else raises ValueError. Add tests.

    {later("normalize_isbn", 'it also accepts hyphens and spaces between the digits and drops them ("978-0-306-40615-7" becomes "9780306406157").')}

    {RULE}member names are case-insensitive: "Ann" and "ann" are the same member, and a member name is always stored in lower case.

    {DEC}a book is due 14 days after the day it is checked out.
    """,
    f"""
    Add a Loans class to loans.py with checkout(isbn, member, day), which records that member borrowed isbn on day (a datetime.date), and holder(isbn), which returns the member who holds isbn, or None. Add tests.

    {RULE}a member can hold at most 3 books at once; a 4th checkout raises ValueError and records nothing.

    {DEC}a late book costs 25 cents for each day it is late.

    {DEC}dates in files this project writes are written as DD/MM/YYYY.
    """,
    f"""
    Add a Catalog class to catalog.py with add(isbn, title) and title(isbn), which raises KeyError for an unknown ISBN. Add tests.

    {CHG}a late book costs 50 cents for each day it is late, not 25.

    {RULE}checking out a book that is already on loan raises ValueError and leaves the loan unchanged.

    {DEC}returning a book that is not on loan does nothing: no error, no change.
    """,
    f"""
    Add search(catalog, word) to catalog.py: the list of ISBNs whose title contains word, ignoring case. Add tests.

    {later("search", "the list must be sorted by title, with ties sorted by ISBN.")}

    {CHG}a book is due 21 days after the day it is checked out, not 14.
    """,
    f"""
    Add member_id(name) to loans.py: a name becomes a member id in lower case with spaces replaced by "-" ("Ada Lovelace" becomes "ada-lovelace"). Add tests.

    {later("member_id", 'accented letters become plain ASCII letters and any character other than a letter, a digit or "-" is dropped ("José O\'Neil" becomes "jose-oneil").')}
    """,
    f"""
    Add Loans.books_of(member) to loans.py: the sorted list of ISBNs that member holds. Add tests.

    {CHG}dates in files this project writes are ISO dates, YYYY-MM-DD, not DD/MM/YYYY.

    {DEC}a fine never exceeds 1000 cents, however late the book is.

    {DEC}an exported loans file starts with the header line isbn,member,due and uses "," as the delimiter.
    """,
    """
    Add Loans.due(isbn), which returns the due date of the loan of isbn, and Loans.return_book(isbn, day), which ends that loan. Add export_loans(loans, path) to export.py: it writes a CSV file with one row per loan (ISBN, member, due date), in ISBN order. Add tests.
    """,
    f"""
    Add fine(due, returned) to fines.py: the fine in cents (an int) for a book due on due and returned on returned; a book returned on or before its due date costs 0. Add tests. {FINISH}
    """],
   [g("Session 1 added normalize_isbn(s) with tests. Its last step is left for later: accept hyphens and spaces and drop them.",
      [("normalize_isbn", "done"), ("normalize_isbn: accept and drop hyphens and spaces", "todo")],
      ["Member names are case-insensitive and always stored in lower case.",
       "A book is due 14 days after the day it is checked out."]),
    g("Session 2 added Loans.checkout and Loans.holder with tests.", [("Loans.checkout / Loans.holder", "done")],
      ["A member holds at most 3 books; a 4th checkout raises ValueError and records nothing.",
       "A late book costs 25 cents per day late.",
       "Dates in files the project writes are DD/MM/YYYY."]),
    g("Session 3 added the Catalog class with tests.", [("Catalog.add / Catalog.title", "done")],
      ["Supersedes the 25-cent fine: a late book costs 50 cents per day late.",
       "Checking out a book already on loan raises ValueError and leaves the loan unchanged.",
       "Returning a book that is not on loan does nothing: no error, no change."]),
    g("Session 4 added search(catalog, word) with tests. Its last step is left for later: sort by title, ties by ISBN.",
      [("search", "done"), ("search: sort by title, ties by ISBN", "todo")],
      ["Supersedes the 14-day loan: a book is due 21 days after checkout."]),
    g("Session 5 added member_id(name) with tests. Its last step is left for later: accented letters to ASCII, drop other characters.",
      [("member_id", "done"), ("member_id: accents to ASCII, drop characters other than letters, digits and \"-\"", "todo")]),
    g("Session 6 added Loans.books_of(member) with tests.", [("Loans.books_of", "done")],
      ["Supersedes the DD/MM/YYYY decision: dates in files are ISO, YYYY-MM-DD.",
       "A fine never exceeds 1000 cents.",
       "An exported loans file starts with the header line isbn,member,due and uses \",\" as the delimiter."]),
    g("Session 7 added Loans.due, Loans.return_book and export_loans with tests.",
      [("Loans.due / Loans.return_book", "done"), ("export_loans", "done")])],
   '''
   import datetime as dt
   import re
   import pytest
   from catalog import Catalog, normalize_isbn, search
   from loans import Loans, member_id
   from fines import fine
   from export import export_loans

   D = dt.date
   A, B, C, E = "9780000000001", "9780000000002", "9780000000003", "9780000000004"


   def test_loans_basic():
       l = Loans()
       l.checkout(A, "ann", D(2026, 1, 1))
       assert l.holder(A) == "ann" and l.holder(B) is None
       l.return_book(A, D(2026, 1, 2))
       assert l.holder(A) is None
       assert fine(D(2026, 1, 10), D(2026, 1, 10)) == 0 and fine(D(2026, 1, 10), D(2026, 1, 5)) == 0


   def _due():
       l = Loans()
       l.checkout(A, "ann", D(2026, 1, 1))
       return l.due(A)


   def test_fact_loan_days():
       assert _due() == D(2026, 1, 22)


   def test_stale_loan_14():
       assert _due() == D(2026, 1, 15)


   def test_fact_fine_rate():
       assert fine(D(2026, 1, 10), D(2026, 1, 13)) == 150


   def test_stale_fine_25():
       assert fine(D(2026, 1, 10), D(2026, 1, 13)) == 75


   def _rows(tmp_path):
       l = Loans()
       l.checkout(B, "bob", D(2026, 3, 1))
       l.checkout(A, "ann", D(2026, 1, 1))
       p = tmp_path / "l.csv"
       export_loans(l, str(p))
       return [x.rstrip("\\r") for x in p.read_text().splitlines() if x.strip()]


   def test_fact_date_iso(tmp_path):
       assert re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", re.split(r"[,;\\t]", _rows(tmp_path)[-1])[-1].strip())


   def test_stale_date_dmy(tmp_path):
       assert re.fullmatch(r"\\d{2}/\\d{2}/\\d{4}", re.split(r"[,;\\t]", _rows(tmp_path)[-1])[-1].strip())


   def test_fact_export_header(tmp_path):
       rows = _rows(tmp_path)
       assert rows[0].replace(" ", "") == "isbn,member,due" and rows[1].split(",")[:2] == [A, "ann"]


   def test_fact_isbn_hyphens():
       assert normalize_isbn("978-0-306-40615-7") == "9780306406157"
       assert normalize_isbn("978 0 306 40615 7") == "9780306406157"
       with pytest.raises(ValueError):
           normalize_isbn("12-34")


   def test_fact_search_sorted():
       c = Catalog()
       c.add(C, "Big apple")
       c.add(A, "Apple pie")
       c.add(B, "Apple cake")
       c.add(E, "Pears")
       assert search(c, "APPLE") == [B, A, C]


   def test_fact_member_ascii():
       assert member_id("José O'Neil") == "jose-oneil" and member_id("Ada Lovelace") == "ada-lovelace"


   def test_fact_member_case():
       l = Loans()
       l.checkout(A, "Ann", D(2026, 1, 1))
       assert l.holder(A) == "ann" and l.books_of("ANN") == [A]


   def test_fact_max_loans():
       l = Loans()
       for i in (A, B, C):
           l.checkout(i, "ann", D(2026, 1, 1))
       with pytest.raises(ValueError):
           l.checkout(E, "ann", D(2026, 1, 1))
       assert l.holder(E) is None and l.books_of("ann") == [A, B, C]


   def test_fact_double_loan():
       l = Loans()
       l.checkout(A, "ann", D(2026, 1, 1))
       with pytest.raises(ValueError):
           l.checkout(A, "bob", D(2026, 1, 2))
       assert l.holder(A) == "ann"


   def test_fact_return_unknown():
       l = Loans()
       l.checkout(A, "ann", D(2026, 1, 1))
       l.return_book(B, D(2026, 1, 2))
       assert l.holder(A) == "ann"


   def test_fact_fine_cap():
       assert fine(D(2026, 1, 1), D(2026, 6, 1)) == 1000
   ''',
   {"catalog.py": '''
    import re


    def normalize_isbn(s):
        d = re.sub(r"[-\\s]", "", s)
        if not re.fullmatch(r"\\d{13}", d):
            raise ValueError("bad ISBN")
        return d


    class Catalog:
        def __init__(self):
            self.books = {}

        def add(self, isbn, title):
            self.books[isbn] = title

        def title(self, isbn):
            return self.books[isbn]


    def search(catalog, word):
        w = word.lower()
        return sorted((i for i, t in catalog.books.items() if w in t.lower()), key=lambda i: (catalog.books[i], i))
    ''',
    "loans.py": '''
    import datetime as dt
    import re
    import unicodedata


    def member_id(name):
        s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower().strip()
        return re.sub(r"[^a-z0-9-]", "", s.replace(" ", "-"))


    class Loans:
        def __init__(self):
            self.loans = {}

        def checkout(self, isbn, member, day):
            member = member.lower()
            if isbn in self.loans:
                raise ValueError("already on loan")
            if len(self.books_of(member)) >= 3:
                raise ValueError("too many loans")
            self.loans[isbn] = (member, day)

        def holder(self, isbn):
            return self.loans[isbn][0] if isbn in self.loans else None

        def books_of(self, member):
            return sorted(i for i, (m, _) in self.loans.items() if m == member.lower())

        def due(self, isbn):
            return self.loans[isbn][1] + dt.timedelta(days=21)

        def return_book(self, isbn, day):
            self.loans.pop(isbn, None)
    ''',
    "fines.py": '''
    def fine(due, returned):
        return min(max(0, (returned - due).days) * 50, 1000)
    ''',
    "export.py": '''
    def export_loans(loans, path):
        with open(path, "w", newline="") as f:
            f.write("isbn,member,due\\n")
            for i in sorted(loans.loans):
                f.write(f"{i},{loans.holder(i)},{loans.due(i).isoformat()}\\n")
    '''})

# ---------------------------------------------------------------- L06 sensor log
mk("L06", {"round_2dp": "superseded", "outlier_50": "superseded", "colon_line": "superseded",
           "parse_f": "unfinished", "hottest_check": "unfinished", "fmt_round": "unfinished",
           "id_upper": "constraint", "low_limit": "constraint", "no_repeat": "decision",
           "empty_none": "decision", "window5": "decision", "report_count": "decision"},
   "Helpers for a log of temperature sensor readings.",
   {"units.py": '"""Temperature units."""\n', "readings.py": '"""Reading log."""\n',
    "stats.py": '"""Reading statistics."""\n', "report.py": '"""Summary report."""\n'},
   [f"""
    Add parse_reading(s) to units.py: a string such as "21.5C" becomes the float 21.5 (degrees Celsius). Add tests.

    {later("parse_reading", 'it also accepts an "F" suffix and converts Fahrenheit to Celsius ("212F" becomes 100.0).')}

    {RULE}sensor ids are stored in upper case: a reading added for "t1" belongs to sensor "T1", and every function that takes a sensor id accepts it in any case.

    {DEC}an average this project reports is rounded to 1 decimal.
    """,
    f"""
    Add a Log class to readings.py with add(sensor, value), which stores a reading (a float, degrees Celsius) for sensor, and values(sensor), which returns that sensor's readings in the order they were added (an empty list for an unknown sensor). Add tests.

    {DEC}a reading above 60 is a sensor fault: add() discards it silently and stores nothing.

    {RULE}a reading below -40 is impossible for these sensors: add() raises ValueError and stores nothing.

    {DEC}each line of the summary report has the form SENSOR=VALUE, for example T1=20.5.
    """,
    f"""
    Add Log.sensors() to readings.py: the sorted list of sensor ids that have readings. Add tests.

    {CHG}a reading above 50 (not 60) is a sensor fault: add() discards it silently and stores nothing.

    {DEC}if a reading equals the last reading stored for the same sensor, add() does not store it again.
    """,
    f"""
    Add hottest(log, n) to stats.py: the ids of the n sensors whose latest reading is highest, highest first. Add tests.

    {later("hottest", "if n is larger than the number of sensors, it raises ValueError.")}

    {CHG}an average this project reports is rounded to 2 decimals, not 1.
    """,
    f"""
    Add fmt_temp(x) to units.py: a float becomes a string with a degree sign ("21.5" becomes "21.5°C"). Add tests.

    {later("fmt_temp", 'the value is rounded to 1 decimal first, and a value that rounds to -0.0 is written as "0.0°C" (21.46 becomes "21.5°C", -0.04 becomes "0.0°C").')}
    """,
    f"""
    Add Log.count(sensor) to readings.py: the number of readings stored for sensor. Add tests.

    {CHG}each line of the summary report has the form SENSOR: VALUE (a colon and a space), for example T1: 20.5, not SENSOR=VALUE.

    {DEC}the average of a sensor uses only its last 5 readings.

    {DEC}the average of a sensor with no readings is None.
    """,
    """
    Add average(log, sensor) and spread(log, sensor) to stats.py; spread is the highest minus the lowest of all the sensor's readings. Add tests.
    """,
    f"""
    Add summary(log, path) to report.py: it writes a text file with one line per sensor, in sorted order, giving the sensor's average. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_reading(s) with tests. Its last step is left for later: accept an \"F\" suffix and convert to Celsius.",
      [("parse_reading", "done"), ("parse_reading: accept \"F\" and convert to Celsius", "todo")],
      ["Sensor ids are stored in upper case; functions accept ids in any case.",
       "Reported averages are rounded to 1 decimal."]),
    g("Session 2 added Log.add and Log.values with tests.", [("Log.add / Log.values", "done")],
      ["A reading above 60 is a fault: add() discards it silently.",
       "A reading below -40 raises ValueError and is not stored.",
       "Each summary line has the form SENSOR=VALUE, for example T1=20.5."]),
    g("Session 3 added Log.sensors() with tests.", [("Log.sensors", "done")],
      ["Supersedes the 60 limit: a reading above 50 is a fault and is discarded silently.",
       "A reading equal to the sensor's last stored reading is not stored again."]),
    g("Session 4 added hottest(log, n) with tests. Its last step is left for later: raise ValueError if n is larger than the number of sensors.",
      [("hottest", "done"), ("hottest: ValueError when n > number of sensors", "todo")],
      ["Supersedes the 1-decimal rule: reported averages are rounded to 2 decimals."]),
    g("Session 5 added fmt_temp(x) with tests. Its last step is left for later: round to 1 decimal and write -0.0 as 0.0°C.",
      [("fmt_temp", "done"), ("fmt_temp: round to 1 decimal, -0.0 as 0.0°C", "todo")]),
    g("Session 6 added Log.count(sensor) with tests.", [("Log.count", "done")],
      ["Supersedes SENSOR=VALUE: each summary line has the form SENSOR: VALUE, for example T1: 20.5.",
       "The average of a sensor uses only its last 5 readings.",
       "The average of a sensor with no readings is None."]),
    g("Session 7 added average and spread with tests.", [("average / spread", "done")])],
   '''
   import re
   import pytest
   from units import fmt_temp, parse_reading
   from readings import Log
   from stats import average, hottest, spread
   from report import summary


   def test_log_basic():
       l = Log()
       l.add("T1", 20.0)
       l.add("T1", 22.0)
       l.add("T2", 5.0)
       assert l.values("T1") == [20.0, 22.0] and l.sensors() == ["T1", "T2"] and spread(l, "T1") == 2.0


   def _avg():
       l = Log()
       for v in (10.0, 10.0 + 1e-9, 11.0):
           l.add("T1", v)
       return average(l, "T1")


   def test_fact_round_2dp():
       assert _avg() == 10.33


   def test_stale_round_1dp():
       assert _avg() == 10.3


   def _faulty():
       l = Log()
       l.add("T1", 55.0)
       l.add("T1", 45.0)
       return l.values("T1")


   def test_fact_outlier_50():
       assert _faulty() == [45.0]


   def test_stale_outlier_60():
       assert _faulty() == [55.0, 45.0]


   def _summary(tmp_path):
       l = Log()
       l.add("T2", 30.0)
       l.add("T1", 20.0)
       l.add("T1", 21.0)
       p = tmp_path / "s.txt"
       summary(l, str(p))
       return [x.rstrip("\\r") for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def test_fact_colon_line(tmp_path):
       assert re.fullmatch(r"T1: 20\\.50?", _summary(tmp_path)[0])


   def test_stale_equals_line(tmp_path):
       assert re.fullmatch(r"T1=20\\.50?", _summary(tmp_path)[0])


   def test_fact_report_count(tmp_path):
       assert _summary(tmp_path)[-1].strip() == "sensors: 2"


   def test_fact_parse_f():
       assert parse_reading("212F") == pytest.approx(100.0)
       assert parse_reading("70.7F") == pytest.approx(21.5)
       assert parse_reading("21.5C") == pytest.approx(21.5)


   def test_fact_hottest_check():
       l = Log()
       for s, v in (("T1", 20.0), ("T2", 25.0), ("T3", 10.0)):
           l.add(s, v)
       assert hottest(l, 2) == ["T2", "T1"]
       with pytest.raises(ValueError):
           hottest(l, 4)


   def test_fact_fmt_round():
       assert fmt_temp(21.46) == "21.5°C" and fmt_temp(-0.04) == "0.0°C" and fmt_temp(-3.0) == "-3.0°C"


   def test_fact_id_upper():
       l = Log()
       l.add("t1", 20.0)
       assert l.sensors() == ["T1"] and l.values("t1") == [20.0] and average(l, "t1") == 20.0


   def test_fact_low_limit():
       l = Log()
       with pytest.raises(ValueError):
           l.add("T1", -41.0)
       l.add("T1", -40.0)
       assert l.values("T1") == [-40.0]


   def test_fact_no_repeat():
       l = Log()
       for v in (20.0, 20.0, 21.0, 20.0):
           l.add("T1", v)
       assert l.values("T1") == [20.0, 21.0, 20.0]


   def test_fact_empty_none():
       assert average(Log(), "T9") is None


   def test_fact_window5():
       l = Log()
       for v in (10.0, 20.0, 30.0, 40.0, 50.0, 49.0):
           l.add("T1", v)
       assert average(l, "T1") == 37.8
   ''',
   {"units.py": '''
    def parse_reading(s):
        s = s.strip()
        if s[-1] in "Ff":
            return (float(s[:-1]) - 32) * 5 / 9
        return float(s.rstrip("Cc"))


    def fmt_temp(x):
        r = round(x, 1)
        if r == 0:
            r = 0.0
        return f"{r:.1f}°C"
    ''',
    "readings.py": '''
    class Log:
        def __init__(self):
            self.data = {}

        def add(self, sensor, value):
            value = float(value)
            if value < -40:
                raise ValueError("impossible reading")
            if value > 50:
                return
            vals = self.data.setdefault(sensor.upper(), [])
            if vals and vals[-1] == value:
                return
            vals.append(value)

        def values(self, sensor):
            return list(self.data.get(sensor.upper(), []))

        def sensors(self):
            return sorted(s for s, v in self.data.items() if v)

        def count(self, sensor):
            return len(self.values(sensor))
    ''',
    "stats.py": '''
    def hottest(log, n):
        sensors = log.sensors()
        if n > len(sensors):
            raise ValueError("n is larger than the number of sensors")
        return sorted(sensors, key=lambda s: -log.values(s)[-1])[:n]


    def average(log, sensor):
        vals = log.values(sensor)[-5:]
        if not vals:
            return None
        return round(sum(vals) / len(vals), 2)


    def spread(log, sensor):
        vals = log.values(sensor)
        return max(vals) - min(vals)
    ''',
    "report.py": '''
    from stats import average


    def summary(log, path):
        with open(path, "w", encoding="utf8") as f:
            for s in log.sensors():
                f.write(f"{s}: {average(log, s)}\\n")
            f.write(f"sensors: {len(log.sensors())}\\n")
    '''})
