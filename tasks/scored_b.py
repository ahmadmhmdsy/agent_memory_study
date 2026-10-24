"""R-014 scored projects L07-L08 (v3 form: 8 sessions, 12 facts)."""
from long_common import CHG, DEC, FINISH, RULE, g, later, mk

# ---------------------------------------------------------------- L07 gradebook
mk("L07", {"pass_60": "superseded", "exam_weight": "superseded", "status_words": "superseded",
           "parse_pct": "unfinished", "top_skip_empty": "unfinished", "initials_hyphen": "unfinished",
           "score_range": "constraint", "name_clean": "constraint", "half_up": "constraint",
           "dup_student": "decision", "export_sorted": "decision", "drop_lowest": "decision"},
   "Grade helpers for a small course.",
   {"grades.py": '"""Gradebook."""\n', "roster.py": '"""Roster helpers."""\n',
    "stats.py": '"""Grade statistics."""\n', "export.py": '"""Grade export."""\n'},
   [f"""
    Add parse_score(s) to grades.py: a string such as "17/20" becomes a percentage as a float (17/20 becomes 85.0). Add tests.

    {later("parse_score", 'it also accepts a percentage string such as "85%", which becomes 85.0.')}

    {RULE}a score is a number from 0 to 100; any function given a score outside that range raises ValueError.

    {DEC}a student passes the course with a final score of 50 or more.
    """,
    f"""
    Add a Gradebook class to grades.py with add_student(name), add_score(name, kind, score), where kind is "hw" (homework) or "exam", and scores(name, kind), which returns that student's scores of that kind in the order they were added. Add tests.

    {RULE}student names are cleaned when stored: leading and trailing spaces are removed and runs of spaces inside become one space ("  Ann   Lee " is stored as "Ann Lee"), and every function that takes a name cleans it the same way.

    {DEC}a final score is 60% the homework average plus 40% the exam score.

    {DEC}the status column of an exported grades file is "P" for a pass and "F" for a fail.
    """,
    f"""
    Add Gradebook.students() to grades.py: the sorted list of student names. Add tests.

    {CHG}a final score is 50% the homework average plus 50% the exam score, not 60/40.

    {DEC}adding a student who is already in the gradebook raises ValueError.

    {DEC}rows of an exported grades file are sorted by final score, highest first, with ties sorted by name.
    """,
    f"""
    Add top_homework(book, n) to stats.py: the names of the n students with the highest homework average, highest first. Add tests.

    {later("top_homework", "students with no homework scores are left out.")}

    {CHG}a student passes the course with a final score of 60 or more, not 50.
    """,
    f"""
    Add initials(name) to roster.py: the upper-case initials of a name ("ada lovelace" becomes "AL"). Add tests.

    {later("initials", 'each part of a hyphenated name gives an initial too ("Jean-Luc Picard" becomes "JLP").')}
    """,
    f"""
    Add Gradebook.count(name) to grades.py: the number of scores of any kind stored for that student. Add tests.

    {CHG}the status column of an exported grades file is "pass" or "fail", not "P" or "F".

    {DEC}when a student has 3 or more homework scores, the lowest one is left out of the homework average.

    {RULE}a final score is rounded to a whole number (an int), half-up: 82.5 becomes 83.
    """,
    """
    Add final_score(book, name) and passed(book, name) to stats.py. The exam score used is the student's last exam score. Add tests.
    """,
    f"""
    Add export_grades(book, path) to export.py: it writes a CSV file with one row per student and the columns name, final score and status. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_score(s) with tests. Its last step is left for later: accept a percentage string such as \"85%\".",
      [("parse_score", "done"), ("parse_score: accept \"85%\"", "todo")],
      ["A score is from 0 to 100; any function given a score outside that range raises ValueError.",
       "A student passes with a final score of 50 or more."]),
    g("Session 2 added Gradebook.add_student, add_score and scores with tests.", [("Gradebook.add_student / add_score / scores", "done")],
      ["Student names are cleaned: outer spaces removed, inner runs of spaces become one; functions clean names the same way.",
       "A final score is 60% homework average plus 40% exam score.",
       "The status column of an exported grades file is \"P\" or \"F\"."]),
    g("Session 3 added Gradebook.students() with tests.", [("Gradebook.students", "done")],
      ["Supersedes 60/40: a final score is 50% homework average plus 50% exam score.",
       "Adding a student who is already in the gradebook raises ValueError.",
       "Exported grade rows are sorted by final score, highest first, ties by name."]),
    g("Session 4 added top_homework(book, n) with tests. Its last step is left for later: leave out students with no homework scores.",
      [("top_homework", "done"), ("top_homework: leave out students with no homework", "todo")],
      ["Supersedes the pass mark of 50: a student passes with a final score of 60 or more."]),
    g("Session 5 added initials(name) with tests. Its last step is left for later: each part of a hyphenated name gives an initial.",
      [("initials", "done"), ("initials: hyphenated parts give initials", "todo")]),
    g("Session 6 added Gradebook.count(name) with tests.", [("Gradebook.count", "done")],
      ["Supersedes \"P\"/\"F\": the status column is \"pass\" or \"fail\".",
       "With 3 or more homework scores, the lowest is left out of the homework average.",
       "A final score is rounded to a whole number (an int), half-up."]),
    g("Session 7 added final_score and passed with tests.", [("final_score / passed", "done")])],
   '''
   import csv
   import pytest
   from grades import Gradebook, parse_score
   from roster import initials
   from stats import final_score, passed, top_homework
   from export import export_grades


   def _book(rows):
       b = Gradebook()
       for name, hw, exam in rows:
           b.add_student(name)
           for s in hw:
               b.add_score(name, "hw", s)
           for s in exam:
               b.add_score(name, "exam", s)
       return b


   def test_book_basic():
       b = _book([("Bob", [80, 90], [70]), ("Ann", [60], [])])
       assert b.students() == ["Ann", "Bob"] and b.scores("Bob", "hw") == [80, 90] and b.count("Bob") == 3
       assert parse_score("17/20") == 85.0


   def test_fact_exam_weight():
       assert final_score(_book([("Ann", [70, 90], [60])]), "Ann") == 70


   def test_stale_weight_60_40():
       assert final_score(_book([("Ann", [70, 90], [60])]), "Ann") == 72


   def test_fact_pass_60():
       b = _book([("Ann", [55], [55]), ("Bob", [60], [60])])
       assert passed(b, "Ann") is False and passed(b, "Bob") is True


   def test_stale_pass_50():
       assert passed(_book([("Ann", [55], [55])]), "Ann") is True


   def _rows(tmp_path):
       b = _book([("Bob", [70], [70]), ("Zoe", [90], [90]), ("Ann", [70], [70])])
       p = tmp_path / "g.csv"
       export_grades(b, str(p))
       rows = [r for r in csv.reader(p.read_text().splitlines()) if r]
       return [r for r in rows if r[0] in ("Ann", "Bob", "Zoe")]


   def test_fact_status_words(tmp_path):
       assert [r[-1].strip() for r in _rows(tmp_path)] == ["pass", "pass", "pass"]


   def test_stale_status_letters(tmp_path):
       assert [r[-1].strip() for r in _rows(tmp_path)] == ["P", "P", "P"]


   def test_fact_export_sorted(tmp_path):
       assert [r[0] for r in _rows(tmp_path)] == ["Zoe", "Ann", "Bob"]


   def test_fact_parse_pct():
       assert parse_score("85%") == 85.0 and parse_score("17/20") == 85.0


   def test_fact_top_skip_empty():
       b = _book([("Ann", [90], []), ("Bob", [], []), ("Cy", [80], [])])
       assert top_homework(b, 3) == ["Ann", "Cy"]


   def test_fact_initials_hyphen():
       assert initials("Jean-Luc Picard") == "JLP" and initials("ada lovelace") == "AL"


   def test_fact_score_range():
       b = _book([("Ann", [], [])])
       for bad in (101, -1):
           with pytest.raises(ValueError):
               b.add_score("Ann", "hw", bad)
       b.add_score("Ann", "hw", 100)
       assert b.scores("Ann", "hw") == [100]


   def test_fact_name_clean():
       b = Gradebook()
       b.add_student("  Ann   Lee ")
       b.add_score(" Ann Lee", "hw", 50)
       assert b.students() == ["Ann Lee"] and b.scores("Ann  Lee", "hw") == [50]


   def test_fact_half_up():
       r = final_score(_book([("Ann", [82, 83], [82.5])]), "Ann")
       assert r == 83 and isinstance(r, int)


   def test_fact_dup_student():
       b = _book([("Ann", [], [])])
       with pytest.raises(ValueError):
           b.add_student("Ann")


   def test_fact_drop_lowest():
       assert final_score(_book([("Ann", [50, 90, 100], [95])]), "Ann") == 95
   ''',
   {"grades.py": '''
    def parse_score(s):
        s = s.strip()
        if s.endswith("%"):
            return float(s[:-1])
        a, b = s.split("/")
        return float(a) / float(b) * 100


    def _clean(name):
        return " ".join(name.split())


    class Gradebook:
        def __init__(self):
            self.data = {}

        def add_student(self, name):
            name = _clean(name)
            if name in self.data:
                raise ValueError("student already exists")
            self.data[name] = {"hw": [], "exam": []}

        def add_score(self, name, kind, score):
            if not 0 <= score <= 100:
                raise ValueError("score out of range")
            self.data[_clean(name)][kind].append(score)

        def scores(self, name, kind):
            return list(self.data[_clean(name)][kind])

        def students(self):
            return sorted(self.data)

        def count(self, name):
            d = self.data[_clean(name)]
            return len(d["hw"]) + len(d["exam"])
    ''',
    "roster.py": '''
    import re


    def initials(name):
        return "".join(p[0].upper() for p in re.split(r"[\\s-]+", name.strip()) if p)
    ''',
    "stats.py": '''
    from decimal import Decimal, ROUND_HALF_UP


    def _hw(book, name):
        hw = book.scores(name, "hw")
        if len(hw) >= 3:
            hw = sorted(hw)[1:]
        return sum(hw) / len(hw)


    def top_homework(book, n):
        names = [s for s in book.students() if book.scores(s, "hw")]
        return sorted(names, key=lambda s: -_hw(book, s))[:n]


    def final_score(book, name):
        x = 0.5 * _hw(book, name) + 0.5 * book.scores(name, "exam")[-1]
        return int(Decimal(str(x)).quantize(Decimal(1), ROUND_HALF_UP))


    def passed(book, name):
        return final_score(book, name) >= 60
    ''',
    "export.py": '''
    import csv
    from stats import final_score, passed


    def export_grades(book, path):
        rows = sorted(book.students(), key=lambda s: (-final_score(book, s), s))
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["name", "final", "status"])
            for s in rows:
                w.writerow([s, final_score(book, s), "pass" if passed(book, s) else "fail"])
    '''})

# ---------------------------------------------------------------- L08 parking garage
mk("L08", {"free_30": "superseded", "rate_250": "superseded", "total_line": "superseded",
           "plate_check": "unfinished", "parked_sorted": "unfinished", "fmt_days": "unfinished",
           "time_order": "constraint", "capacity": "constraint", "double_entry": "constraint",
           "exit_unknown": "decision", "fee_cap": "decision", "receipt_plate": "decision"},
   "Fee helpers for a small parking garage. Times are int minutes.",
   {"tickets.py": '"""Ticket helpers."""\n', "rates.py": '"""Parking rates."""\n',
    "garage.py": '"""Garage state."""\n', "receipt.py": '"""Receipts."""\n'},
   [f"""
    Add parse_plate(s) to tickets.py: a licence plate string is returned in upper case with spaces removed (" ab 123 " becomes "AB123"). Add tests.

    {later("parse_plate", 'hyphens are removed too, and a plate that is then not 2 to 8 letters and digits raises ValueError ("ab-12 3" becomes "AB123"; "a" and "ab!12" raise).')}

    {RULE}a stay cannot end before it starts: any function given an exit time earlier than the entry time raises ValueError and changes nothing.

    {DEC}the first 15 minutes of a stay are free.
    """,
    f"""
    Add a Garage class to garage.py: Garage(capacity), enter(plate, t), which records that plate entered at minute t, and inside(), the sorted list of plates inside. Add tests.

    {RULE}a garage never holds more cars than its capacity: entering a full garage raises ValueError and records nothing.

    {DEC}parking costs 200 cents for each started hour.

    {DEC}the last line of a receipt is the total in the form TOTAL 5.00.
    """,
    f"""
    Add Garage.free() to garage.py: the number of free spaces. Add tests.

    {CHG}parking costs 250 cents for each started hour, not 200.

    {RULE}a plate that is already inside cannot enter again: enter() raises ValueError.

    {DEC}exiting a plate that is not inside returns None and changes nothing.
    """,
    f"""
    Add parked_before(garage, t) to garage.py: the list of plates inside that entered before minute t. Add tests.

    {later("parked_before", "the list must be sorted by entry time, earliest first, with ties sorted by plate.")}

    {CHG}the first 30 minutes of a stay are free, not 15.
    """,
    f"""
    Add fmt_duration(minutes) to receipt.py: 125 becomes "2h 05m". Add tests.

    {later("fmt_duration", 'a duration of a day or more starts with the days: 1505 becomes "1d 01h 05m".')}
    """,
    f"""
    Add Garage.entry_time(plate) to garage.py: the minute at which plate entered. Add tests.

    {CHG}the last line of a receipt is the total in the form Total: $5.00, not TOTAL 5.00.

    {DEC}the fee for one stay never exceeds 2000 cents.

    {DEC}the first line of a receipt is the plate in the form Plate: AB123.
    """,
    """
    Add fee(minutes) to rates.py: the fee in cents (an int) for a stay of that many minutes. A stay within the free period costs 0; a longer stay costs the hourly price for each started hour of the whole stay. Add Garage.exit(plate, t), which removes plate and returns the fee for its stay. Add tests.
    """,
    f"""
    Add write_receipt(plate, minutes, path) to receipt.py: it writes a text receipt for a stay of that many minutes, with the plate, the duration (from fmt_duration) and the total fee. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_plate(s) with tests. Its last step is left for later: remove hyphens and require 2 to 8 letters and digits.",
      [("parse_plate", "done"), ("parse_plate: remove hyphens, require 2-8 letters and digits", "todo")],
      ["An exit time earlier than the entry time raises ValueError and changes nothing.",
       "The first 15 minutes of a stay are free."]),
    g("Session 2 added Garage(capacity), enter and inside with tests.", [("Garage.enter / Garage.inside", "done")],
      ["Entering a full garage raises ValueError and records nothing.",
       "Parking costs 200 cents per started hour.",
       "The last receipt line is the total in the form TOTAL 5.00."]),
    g("Session 3 added Garage.free() with tests.", [("Garage.free", "done")],
      ["Supersedes 200 cents: parking costs 250 cents per started hour.",
       "A plate already inside cannot enter again: enter() raises ValueError.",
       "Exiting a plate that is not inside returns None and changes nothing."]),
    g("Session 4 added parked_before(garage, t) with tests. Its last step is left for later: sort by entry time, ties by plate.",
      [("parked_before", "done"), ("parked_before: sort by entry time, ties by plate", "todo")],
      ["Supersedes 15 free minutes: the first 30 minutes of a stay are free."]),
    g("Session 5 added fmt_duration(minutes) with tests. Its last step is left for later: days first for a day or more (\"1d 01h 05m\").",
      [("fmt_duration", "done"), ("fmt_duration: days first for a day or more", "todo")]),
    g("Session 6 added Garage.entry_time(plate) with tests.", [("Garage.entry_time", "done")],
      ["Supersedes TOTAL 5.00: the last receipt line is Total: $5.00.",
       "The fee for one stay never exceeds 2000 cents.",
       "The first receipt line is the plate in the form Plate: AB123."]),
    g("Session 7 added fee(minutes) and Garage.exit with tests.", [("fee", "done"), ("Garage.exit", "done")])],
   '''
   import re
   import pytest
   from tickets import parse_plate
   from rates import fee
   from garage import Garage, parked_before
   from receipt import fmt_duration, write_receipt


   def test_garage_basic():
       g = Garage(3)
       g.enter("B", 10)
       g.enter("A", 20)
       assert g.inside() == ["A", "B"] and g.free() == 1 and g.entry_time("A") == 20
       assert g.exit("A", 200) == fee(180) and g.inside() == ["B"]
       assert fmt_duration(125) == "2h 05m"


   def test_fact_free_30():
       assert fee(20) == 0 and fee(30) == 0


   def test_stale_free_15():
       assert fee(20) > 0


   def test_fact_rate_250():
       assert fee(90) == 500 and fee(120) == 500


   def test_stale_rate_200():
       assert fee(90) == 400


   def _receipt(tmp_path):
       p = tmp_path / "r.txt"
       write_receipt("AB123", 90, str(p))
       return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def test_fact_total_line(tmp_path):
       assert re.fullmatch(r"Total: \\$\\d+\\.\\d\\d", _receipt(tmp_path)[-1])


   def test_stale_total_upper(tmp_path):
       assert re.fullmatch(r"TOTAL \\d+\\.\\d\\d", _receipt(tmp_path)[-1])


   def test_fact_receipt_plate(tmp_path):
       assert _receipt(tmp_path)[0] == "Plate: AB123"


   def test_fact_plate_check():
       assert parse_plate("ab-12 3") == "AB123" and parse_plate(" xy 9 ") == "XY9"
       for bad in ("a", "ab!12", "abcdefghi"):
           with pytest.raises(ValueError):
               parse_plate(bad)


   def test_fact_parked_sorted():
       g = Garage(9)
       for p, t in (("Z", 10), ("A", 30), ("M", 10), ("B", 50)):
           g.enter(p, t)
       assert parked_before(g, 40) == ["M", "Z", "A"]


   def test_fact_fmt_days():
       assert fmt_duration(1505) == "1d 01h 05m" and fmt_duration(125) == "2h 05m"


   def test_fact_time_order():
       g = Garage(2)
       g.enter("A", 100)
       with pytest.raises(ValueError):
           g.exit("A", 50)
       assert g.inside() == ["A"]


   def test_fact_capacity():
       g = Garage(2)
       g.enter("A", 1)
       g.enter("B", 2)
       with pytest.raises(ValueError):
           g.enter("C", 3)
       assert g.inside() == ["A", "B"]


   def test_fact_double_entry():
       g = Garage(5)
       g.enter("A", 1)
       with pytest.raises(ValueError):
           g.enter("A", 2)
       assert g.entry_time("A") == 1


   def test_fact_exit_unknown():
       g = Garage(2)
       g.enter("A", 1)
       assert g.exit("Q", 10) is None and g.inside() == ["A"]


   def test_fact_fee_cap():
       assert fee(24 * 60) == 2000
   ''',
   {"tickets.py": '''
    import re


    def parse_plate(s):
        p = re.sub(r"[\\s-]", "", s).upper()
        if not re.fullmatch(r"[A-Z0-9]{2,8}", p):
            raise ValueError("bad plate")
        return p
    ''',
    "rates.py": '''
    def fee(minutes):
        if minutes <= 30:
            return 0
        return min(-(-minutes // 60) * 250, 2000)
    ''',
    "garage.py": '''
    from rates import fee


    class Garage:
        def __init__(self, capacity):
            self.capacity = capacity
            self.cars = {}

        def enter(self, plate, t):
            if plate in self.cars:
                raise ValueError("already inside")
            if len(self.cars) >= self.capacity:
                raise ValueError("garage full")
            self.cars[plate] = t

        def inside(self):
            return sorted(self.cars)

        def free(self):
            return self.capacity - len(self.cars)

        def entry_time(self, plate):
            return self.cars[plate]

        def exit(self, plate, t):
            if plate not in self.cars:
                return None
            if t < self.cars[plate]:
                raise ValueError("exit before entry")
            return fee(t - self.cars.pop(plate))


    def parked_before(garage, t):
        return sorted((p for p, e in garage.cars.items() if e < t), key=lambda p: (garage.cars[p], p))
    ''',
    "receipt.py": '''
    from rates import fee


    def fmt_duration(minutes):
        d, rest = divmod(minutes, 1440)
        h, m = divmod(rest, 60)
        return f"{d}d {h:02d}h {m:02d}m" if d else f"{h}h {m:02d}m"


    def write_receipt(plate, minutes, path):
        c = fee(minutes)
        with open(path, "w", encoding="utf8") as f:
            f.write(f"Plate: {plate}\\n")
            f.write(f"Time: {fmt_duration(minutes)}\\n")
            f.write(f"Total: ${c // 100}.{c % 100:02d}\\n")
    '''})
