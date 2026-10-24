"""R-014 long projects: 6 sessions, a repo of several modules, 5 facts stated in sessions 1-4.
Each project gets repo/, sessions.json, hidden/ and, outside repo/, ref/ (full reference modules,
used only by check_long.py). Usage: python make_long_tasks.py"""
import json
import os
import textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))

RULE = "Project rule (it applies to all later work too): "
DEC = "Design decision for this project (nothing implements it yet; record it for later work): "
CHG = "Change to an earlier decision (it replaces the old one; record it for later work): "
FINISH = "Then finish any work that earlier sessions left for later."


def _w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf8", newline="\n") as f:
        f.write(textwrap.dedent(text).lstrip("\n"))


def g(handoff, tasks, decisions=None):
    out = {"tasks": [{"task": t, "status": s} for t, s in tasks], "handoff": handoff}
    if decisions:
        out["decisions"] = decisions
    return out


def mk(tid, kinds, readme, modules, prompts, given, hidden, ref):
    """modules: {file: start text}; prompts: 6 session prompts; given: C2g facts for sessions 1-5;
    ref: {file: reference text}."""
    assert len(prompts) == 6 and len(given) == 5
    base = os.path.join(ROOT, tid)
    _w(os.path.join(base, "repo", "README.md"), f"# {tid.lower()}\n\n{readme}\n")
    for name, text in modules.items():
        _w(os.path.join(base, "repo", name), text)
    names = ", ".join(m[:-3] for m in modules)
    _w(os.path.join(base, "repo", "tests", "test_smoke.py"), f"def test_import():\n    import {names}\n")
    _w(os.path.join(base, "repo", "conftest.py"), "")
    _w(os.path.join(base, "repo", "pytest.ini"), "[pytest]\ntestpaths = tests\n")
    sessions = [{"prompt": textwrap.dedent(p).strip()} for p in prompts]
    for s, gv in zip(sessions, given):
        s["given"] = gv
    with open(os.path.join(base, "sessions.json"), "w", encoding="utf8", newline="\n") as f:
        json.dump({"id": tid, "kind": "long", "facts": kinds, "sessions": sessions}, f, indent=1)
        f.write("\n")
    _w(os.path.join(base, "hidden", "test_hidden.py"), hidden)
    for name, text in ref.items():
        _w(os.path.join(base, "ref", name), text)


# ---------------------------------------------------------------- L01 shop stock
mk("L01", {"half_up": "constraint", "tab_csv": "superseded", "zero_removed": "decision",
           "overdraw": "constraint", "low_stock_sorted": "unfinished"},
   "Stock and money helpers for a small shop.",
   {"money.py": '"""Money helpers."""\n', "store.py": '"""Stock store."""\n',
    "report.py": '"""Stock reports."""\n', "io_csv.py": '"""CSV export."""\n'},
   [f"""
    Add parse_cents(s) to money.py: a price string such as "12.34" becomes the int 1234. Add tests.

    {RULE}money is always an int number of cents, and a fractional cent is rounded half-up (half a cent goes up).

    {DEC}CSV files this project writes use ";" (semicolon) as the delimiter, and their first line is a header row.
    """,
    f"""
    Add a Store class to store.py with add(sku, qty), which adds qty units of stock for sku, and qty(sku), which returns the stock of sku (0 for a SKU it does not hold). Add tests.

    {RULE}removing more stock than a SKU has must raise ValueError and leave the stock unchanged.
    """,
    f"""
    Add Store.skus() to store.py: the list of SKUs the store holds, sorted. Add tests.

    {DEC}when a SKU's stock reaches 0, the SKU is removed from the store entirely.

    {CHG}CSV files this project writes use a tab character as the delimiter, not ";". Their first line is still a header row.
    """,
    """
    Add low_stock(store, threshold) to report.py: the list of SKUs whose stock is below threshold. Add tests.

    The plan for low_stock has one more step: the list must be sorted by stock, lowest first, with ties sorted by SKU. Do not do that step now; leave it for a later session.
    """,
    """
    Add Store.remove(sku, qty) to store.py, which takes qty units of stock away from sku. Add export_stock(store, path) to io_csv.py: it writes a CSV file with the columns sku, qty and one row per SKU, in sorted SKU order. Add tests.
    """,
    f"""
    Add invoice_total(lines, rate) to money.py: lines is a list of (unit_cents, qty) pairs, and the result is the subtotal plus tax at rate (for example 0.05 for 5%) on the subtotal. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_cents(s) with tests.", [("parse_cents", "done")],
      ["Money is always an int number of cents; a fractional cent is rounded half-up.",
       "CSV files use \";\" as the delimiter, and their first line is a header row."]),
    g("Session 2 added Store.add and Store.qty with tests.", [("Store.add / Store.qty", "done")],
      ["Removing more stock than a SKU has raises ValueError and leaves the stock unchanged."]),
    g("Session 3 added Store.skus() with tests.", [("Store.skus", "done")],
      ["When a SKU's stock reaches 0, the SKU is removed from the store entirely.",
       "Supersedes the \";\" CSV decision: CSV files use a tab as the delimiter; the first line is still a header row."]),
    g("Session 4 added low_stock(store, threshold) with tests. Its last step is left for later: sort the list by stock, lowest first, ties by SKU.",
      [("low_stock", "done"), ("low_stock: sort by stock, lowest first, ties by SKU", "todo")]),
    g("Session 5 added Store.remove and export_stock with tests.", [("Store.remove", "done"), ("export_stock", "done")])],
   '''
   import pytest
   from money import invoice_total
   from store import Store
   from report import low_stock
   from io_csv import export_stock


   def test_store_basic():
       s = Store()
       s.add("A", 5)
       s.add("A", 2)
       s.remove("A", 3)
       assert s.qty("A") == 4 and s.qty("Z") == 0


   def test_fact_half_up():
       assert invoice_total([(5, 2)], 0.25) == 13
       assert invoice_total([(25, 2)], 0.25) == 63
       assert invoice_total([(250, 1)], 0.05) == 263
       assert isinstance(invoice_total([(100, 1)], 0.1), int)


   def _lines(tmp_path):
       s = Store()
       s.add("B", 5)
       s.add("A", 2)
       p = tmp_path / "s.csv"
       export_stock(s, str(p))
       return [l.rstrip("\\r") for l in p.read_text().splitlines() if l.strip()]


   def test_fact_tab_csv(tmp_path):
       assert _lines(tmp_path) == ["sku\\tqty", "A\\t2", "B\\t5"]


   def test_stale_semicolon_csv(tmp_path):
       assert _lines(tmp_path)[0] == "sku;qty"


   def test_fact_zero_removed():
       s = Store()
       s.add("A", 2)
       s.add("B", 1)
       s.remove("A", 2)
       assert s.skus() == ["B"] and s.qty("A") == 0


   def test_fact_overdraw():
       s = Store()
       s.add("A", 2)
       with pytest.raises(ValueError):
           s.remove("A", 3)
       assert s.qty("A") == 2


   def test_fact_low_stock_sorted():
       s = Store()
       s.add("b", 1)
       s.add("d", 3)
       s.add("c", 2)
       s.add("a", 3)
       s.add("e", 9)
       assert low_stock(s, 5) == ["b", "c", "a", "d"]
   ''',
   {"money.py": '''
    from decimal import Decimal, ROUND_HALF_UP


    def parse_cents(s):
        return int((Decimal(s) * 100).quantize(Decimal(1), ROUND_HALF_UP))


    def invoice_total(lines, rate):
        sub = sum(c * q for c, q in lines)
        tax = (Decimal(sub) * Decimal(str(rate))).quantize(Decimal(1), ROUND_HALF_UP)
        return sub + int(tax)
    ''',
    "store.py": '''
    class Store:
        def __init__(self):
            self.stock = {}

        def add(self, sku, qty):
            self.stock[sku] = self.stock.get(sku, 0) + qty

        def qty(self, sku):
            return self.stock.get(sku, 0)

        def skus(self):
            return sorted(self.stock)

        def remove(self, sku, qty):
            if qty > self.qty(sku):
                raise ValueError("not enough stock")
            self.stock[sku] -= qty
            if self.stock[sku] == 0:
                del self.stock[sku]
    ''',
    "report.py": '''
    def low_stock(store, threshold):
        return sorted((s for s in store.skus() if store.qty(s) < threshold), key=lambda s: (store.qty(s), s))
    ''',
    "io_csv.py": '''
    import csv


    def export_stock(store, path):
        with open(path, "w", newline="") as f:
            w = csv.writer(f, delimiter="\\t")
            w.writerow(["sku", "qty"])
            for s in store.skus():
                w.writerow([s, store.qty(s)])
    '''})

# ---------------------------------------------------------------- L02 calendar
mk("L02", {"ids": "superseded", "empty_title": "constraint", "sorted": "decision",
           "minutes": "decision", "slug": "unfinished"},
   "A small calendar of events.",
   {"timeutil.py": '"""Time helpers."""\n', "text.py": '"""Text helpers."""\n',
    "events.py": '"""The calendar."""\n'},
   [f"""
    Add parse_ts(s) to timeutil.py: it parses a "YYYY-MM-DD HH:MM:SS" string into a datetime. Add tests.

    {DEC}durations this project reports are whole minutes, as an int, rounded down.
    """,
    f"""
    Add fmt_ts(dt) to timeutil.py: the inverse of parse_ts. Add tests.

    {DEC}event IDs are "E" followed by a 4-digit counter that starts at 1 (E0001, E0002, ...).
    """,
    f"""
    Add clean_title(s) to text.py: it strips both ends and turns every run of whitespace inside into one space. Add tests.

    {RULE}an event title that is empty after clean_title is rejected with ValueError.

    {DEC}listings of events are sorted by start time, then by title.
    """,
    f"""
    Add slug(title) to text.py: the title in lower case, with spaces replaced by "-". Add tests.

    The plan for slug has one more step: characters other than a-z, 0-9 and "-" are dropped. Do not do that step now; leave it for a later session.

    {CHG}event IDs are "EVT-" followed by a 5-digit counter that starts at 1 (EVT-00001, EVT-00002, ...).
    """,
    """
    Add a Calendar class to events.py. add(title, start, end) stores an event and returns its ID; start and end are "YYYY-MM-DD HH:MM:SS" strings, and the title is cleaned with clean_title. events() returns the stored events as a list of dicts with the keys id, title, start and end. Add tests.
    """,
    f"""
    Add Calendar.duration(event_id) to events.py: the length of that event. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_ts(s) with tests.", [("parse_ts", "done")],
      ["Durations are whole minutes, as an int, rounded down."]),
    g("Session 2 added fmt_ts(dt) with tests.", [("fmt_ts", "done")],
      ["Event IDs are \"E\" plus a 4-digit counter from 1 (E0001, E0002, ...)."]),
    g("Session 3 added clean_title(s) with tests.", [("clean_title", "done")],
      ["An event title that is empty after clean_title is rejected with ValueError.",
       "Listings of events are sorted by start time, then by title."]),
    g("Session 4 added slug(title) with tests. Its last step is left for later: drop characters other than a-z, 0-9 and \"-\".",
      [("slug", "done"), ("slug: drop characters other than a-z, 0-9 and \"-\"", "todo")],
      ["Supersedes the E0001 ID decision: event IDs are \"EVT-\" plus a 5-digit counter from 1 (EVT-00001, ...)."]),
    g("Session 5 added the Calendar class (add, events) with tests.", [("Calendar.add / Calendar.events", "done")])],
   '''
   import pytest
   from events import Calendar
   from text import slug


   def test_calendar_basic():
       c = Calendar()
       c.add("  team   sync ", "2026-01-05 10:00:00", "2026-01-05 10:30:00")
       (e,) = c.events()
       assert e["title"] == "team sync" and e["start"] == "2026-01-05 10:00:00" and e["end"] == "2026-01-05 10:30:00"


   def _ids():
       c = Calendar()
       a = c.add("a", "2026-01-05 10:00:00", "2026-01-05 11:00:00")
       b = c.add("b", "2026-01-06 10:00:00", "2026-01-06 11:00:00")
       return a, b


   def test_fact_ids():
       assert _ids() == ("EVT-00001", "EVT-00002")


   def test_stale_ids():
       assert _ids() == ("E0001", "E0002")


   def test_fact_empty_title():
       c = Calendar()
       with pytest.raises(ValueError):
           c.add("   ", "2026-01-05 10:00:00", "2026-01-05 11:00:00")


   def test_fact_sorted():
       c = Calendar()
       c.add("late", "2026-01-07 09:00:00", "2026-01-07 10:00:00")
       c.add("zeta", "2026-01-05 09:00:00", "2026-01-05 10:00:00")
       c.add("alpha", "2026-01-05 09:00:00", "2026-01-05 10:00:00")
       assert [e["title"] for e in c.events()] == ["alpha", "zeta", "late"]


   def test_fact_minutes():
       c = Calendar()
       a = c.add("a", "2026-01-05 10:00:00", "2026-01-05 10:01:30")
       b = c.add("b", "2026-01-05 12:00:00", "2026-01-05 14:00:59")
       assert c.duration(a) == 1 and c.duration(b) == 120
       assert type(c.duration(a)) is int


   def test_fact_slug():
       assert slug("Hi, There!") == "hi-there"
       assert slug("Q3 plan (draft)") == "q3-plan-draft"
   ''',
   {"timeutil.py": '''
    from datetime import datetime

    FMT = "%Y-%m-%d %H:%M:%S"


    def parse_ts(s):
        return datetime.strptime(s, FMT)


    def fmt_ts(dt):
        return dt.strftime(FMT)
    ''',
    "text.py": '''
    import re


    def clean_title(s):
        return " ".join(s.split())


    def slug(title):
        return re.sub(r"[^a-z0-9-]", "", title.lower().replace(" ", "-"))
    ''',
    "events.py": '''
    from text import clean_title
    from timeutil import parse_ts


    class Calendar:
        def __init__(self):
            self.items = []

        def add(self, title, start, end):
            title = clean_title(title)
            if not title:
                raise ValueError("empty title")
            eid = f"EVT-{len(self.items) + 1:05d}"
            self.items.append({"id": eid, "title": title, "start": start, "end": end})
            return eid

        def events(self):
            return sorted(self.items, key=lambda e: (parse_ts(e["start"]), e["title"]))

        def duration(self, event_id):
            e = next(e for e in self.items if e["id"] == event_id)
            return int((parse_ts(e["end"]) - parse_ts(e["start"])).total_seconds() // 60)
    '''})

# ---------------------------------------------------------------- L03 grade book
mk("L03", {"range": "constraint", "ids": "decision", "plain_mean": "superseded",
           "ranking_ties": "decision", "truncate": "unfinished"},
   "A small grade book for a class.",
   {"students.py": '"""Student helpers."""\n', "grades.py": '"""The grade book."""\n',
    "report.py": '"""Report formatting."""\n', "io_util.py": '"""File helpers."""\n'},
   [f"""
    Add normalize_name(s) to students.py: it strips both ends, turns runs of inner whitespace into one space and capitalizes each word ("  ada  LOVELACE " becomes "Ada Lovelace"). Add tests.

    {RULE}a score is an int from 0 to 100; any function given a score outside that range raises ValueError.

    {DEC}a student's average drops their single lowest score when they have 3 or more scores.
    """,
    f"""
    Add read_lines(path) to io_util.py: the file's lines without line endings, skipping blank lines. Add tests.

    {DEC}student IDs are case-insensitive: they are stored in upper case, and lookups accept any case.
    """,
    f"""
    Add bar(n) to report.py: a string of n "#" characters. Add tests.

    {CHG}a student's average is the plain mean of all their scores (no score is dropped), rounded to 1 decimal place.

    {DEC}rankings sort students by average, highest first, and break ties by student ID in ascending order.
    """,
    """
    Add format_row(name, avg) to report.py: the name left-aligned in 20 characters, then the average right-aligned in 6 characters with 1 decimal place. Add tests.

    The plan for format_row has one more step: a name longer than 20 characters is cut to its first 17 characters followed by "...". Do not do that step now; leave it for a later session.
    """,
    """
    Add a Gradebook class to grades.py with add_score(student_id, score), which records a score for a student, and average(student_id), which returns the student's average (None for a student with no scores). Add tests.
    """,
    f"""
    Add Gradebook.ranking() to grades.py: the list of student IDs in ranking order. Add tests. {FINISH}
    """],
   [g("Session 1 added normalize_name(s) with tests.", [("normalize_name", "done")],
      ["A score is an int from 0 to 100; any function given a score outside that range raises ValueError.",
       "A student's average drops their single lowest score when they have 3 or more scores."]),
    g("Session 2 added read_lines(path) with tests.", [("read_lines", "done")],
      ["Student IDs are case-insensitive: stored in upper case, lookups accept any case."]),
    g("Session 3 added bar(n) with tests.", [("bar", "done")],
      ["Supersedes the drop-lowest decision: the average is the plain mean of all scores, rounded to 1 decimal place.",
       "Rankings sort by average, highest first; ties by student ID, ascending."]),
    g("Session 4 added format_row(name, avg) with tests. Its last step is left for later: cut names longer than 20 characters to 17 characters plus \"...\".",
      [("format_row", "done"), ("format_row: cut names over 20 characters to 17 + \"...\"", "todo")]),
    g("Session 5 added the Gradebook class (add_score, average) with tests.", [("Gradebook.add_score / Gradebook.average", "done")])],
   '''
   import pytest
   from grades import Gradebook
   from report import format_row


   def test_gradebook_basic():
       b = Gradebook()
       b.add_score("A1", 70)
       b.add_score("A1", 80)
       assert b.average("A1") == 75.0 and b.average("Z9") is None


   def test_fact_range():
       b = Gradebook()
       for bad in (101, -1):
           with pytest.raises(ValueError):
               b.add_score("A1", bad)
       b.add_score("A1", 100)
       b.add_score("A1", 0)


   def test_fact_ids():
       b = Gradebook()
       b.add_score("s1", 60)
       assert b.average("S1") == 60.0 and b.average("s1") == 60.0
       assert b.ranking() == ["S1"]


   def _avg():
       b = Gradebook()
       for s in (50, 80, 90):
           b.add_score("A1", s)
       return b.average("A1")


   def test_fact_plain_mean():
       assert _avg() == 73.3


   def test_stale_drop_lowest():
       assert _avg() == 85.0


   def test_fact_ranking_ties():
       b = Gradebook()
       b.add_score("S2", 80)
       b.add_score("S1", 80)
       b.add_score("S3", 90)
       assert b.ranking() == ["S3", "S1", "S2"]


   def test_fact_truncate():
       assert format_row("A" * 25, 1.0) == "A" * 17 + "..." + "   1.0"
       assert format_row("Bo", 75.5) == "Bo" + " " * 18 + "  75.5"
   ''',
   {"students.py": '''
    def normalize_name(s):
        return " ".join(w.capitalize() for w in s.split())
    ''',
    "io_util.py": '''
    def read_lines(path):
        with open(path) as f:
            return [l.rstrip("\\r\\n") for l in f if l.strip()]
    ''',
    "report.py": '''
    def bar(n):
        return "#" * n


    def format_row(name, avg):
        if len(name) > 20:
            name = name[:17] + "..."
        return f"{name:<20}{avg:>6.1f}"
    ''',
    "grades.py": '''
    class Gradebook:
        def __init__(self):
            self.scores = {}

        def add_score(self, student_id, score):
            if not 0 <= score <= 100:
                raise ValueError("score out of range")
            self.scores.setdefault(student_id.upper(), []).append(score)

        def average(self, student_id):
            s = self.scores.get(student_id.upper())
            return round(sum(s) / len(s), 1) if s else None

        def ranking(self):
            return sorted(self.scores, key=lambda i: (-self.average(i), i))
    '''})

# ---------------------------------------------------------------- L04 to-do list
mk("L04", {"sorted": "decision", "save_format": "superseded", "due": "constraint",
           "tags": "unfinished", "title_len": "constraint"},
   "A small to-do list.",
   {"todo.py": '"""The to-do list."""\n', "storage.py": '"""Saving and loading."""\n',
    "util.py": '"""Small helpers."""\n'},
   [f"""
    Add is_blank(s) to util.py: True if s is empty or only whitespace. Add tests.

    {DEC}task lists are sorted by priority (1 is the highest priority and comes first), then by the order the tasks were added.

    {DEC}the save file is JSON with one top-level key, "items", holding the list of tasks.
    """,
    f"""
    Add plural(n, word) to util.py: plural(1, "task") is "1 task", plural(2, "task") is "2 tasks" and plural(0, "task") is "0 tasks". Add tests.

    {RULE}a due date is a "YYYY-MM-DD" string for a real calendar date, or None for no due date; anything else raises ValueError.
    """,
    """
    Add parse_tags(s) to util.py: it splits a comma-separated string into tags, strips spaces around each tag and drops empty tags. Add tests.

    The plan for parse_tags has one more step: tags are lowercased, and duplicates are removed, keeping the first. Do not do that step now; leave it for a later session.
    """,
    f"""
    Add join_tags(tags) to util.py: the tags joined with ", ". Add tests.

    {CHG}the save file is JSON with two top-level keys: "version", set to 2, and "tasks", holding the list of tasks.

    {RULE}a task title is at most 60 characters after stripping both ends; a longer title raises ValueError.
    """,
    """
    Add a TodoList class to todo.py. add(title, priority, due=None) adds a task and returns its id (1, 2, 3, ...). tasks() returns the tasks as a list of dicts with the keys id, title, priority and due. Add tests.
    """,
    f"""
    Add save(todo, path) and load(path) to storage.py: save writes a TodoList to a JSON file, and load reads one back as a TodoList. Add tests. {FINISH}
    """],
   [g("Session 1 added is_blank(s) with tests.", [("is_blank", "done")],
      ["Task lists are sorted by priority (1 first), then by the order the tasks were added.",
       "The save file is JSON with one top-level key, \"items\", holding the list of tasks."]),
    g("Session 2 added plural(n, word) with tests.", [("plural", "done")],
      ["A due date is a \"YYYY-MM-DD\" string for a real calendar date, or None; anything else raises ValueError."]),
    g("Session 3 added parse_tags(s) with tests. Its last step is left for later: lowercase the tags and remove duplicates, keeping the first.",
      [("parse_tags", "done"), ("parse_tags: lowercase, remove duplicates keeping the first", "todo")]),
    g("Session 4 added join_tags(tags) with tests.", [("join_tags", "done")],
      ["Supersedes the \"items\" save-file decision: the save file has \"version\": 2 and \"tasks\", the list of tasks.",
       "A task title is at most 60 characters after stripping; a longer title raises ValueError."]),
    g("Session 5 added the TodoList class (add, tasks) with tests.", [("TodoList.add / TodoList.tasks", "done")])],
   '''
   import json
   import pytest
   from todo import TodoList
   from storage import save, load
   from util import parse_tags


   def test_todo_basic(tmp_path):
       t = TodoList()
       assert t.add("pay rent", 1, "2026-03-01") == 1
       assert t.add("call bob", 2) == 2
       p = tmp_path / "t.json"
       save(t, str(p))
       back = load(str(p))
       assert [x["title"] for x in back.tasks()] == ["pay rent", "call bob"]
       assert back.tasks()[0]["due"] == "2026-03-01" and back.tasks()[1]["due"] is None


   def test_fact_sorted():
       t = TodoList()
       t.add("a", 2)
       t.add("b", 1)
       t.add("c", 2)
       t.add("d", 1)
       assert [x["title"] for x in t.tasks()] == ["b", "d", "a", "c"]


   def _saved(tmp_path):
       t = TodoList()
       t.add("a", 1)
       p = tmp_path / "t.json"
       save(t, str(p))
       return json.loads(p.read_text())


   def test_fact_save_format(tmp_path):
       d = _saved(tmp_path)
       assert d.get("version") == 2 and isinstance(d.get("tasks"), list) and len(d["tasks"]) == 1


   def test_stale_items_key(tmp_path):
       assert "items" in _saved(tmp_path)


   def test_fact_due():
       t = TodoList()
       for bad in ("2026-02-30", "2026/01/01", "tomorrow"):
           with pytest.raises(ValueError):
               t.add("x", 1, bad)
       t.add("x", 1, "2026-01-31")


   def test_fact_title_len():
       t = TodoList()
       with pytest.raises(ValueError):
           t.add("x" * 61, 1)
       t.add("x" * 60, 1)
       t.add("  " + "y" * 60 + "  ", 1)


   def test_fact_tags():
       assert parse_tags("Home, work ,home,,WORK, x") == ["home", "work", "x"]
   ''',
   {"util.py": '''
    def is_blank(s):
        return not s.strip()


    def plural(n, word):
        return f"{n} {word}" if n == 1 else f"{n} {word}s"


    def parse_tags(s):
        out = []
        for t in s.split(","):
            t = t.strip().lower()
            if t and t not in out:
                out.append(t)
        return out


    def join_tags(tags):
        return ", ".join(tags)
    ''',
    "todo.py": '''
    from datetime import date


    class TodoList:
        def __init__(self):
            self.items = []

        def add(self, title, priority, due=None):
            title = title.strip()
            if len(title) > 60:
                raise ValueError("title too long")
            if due is not None:
                if len(due) != 10:
                    raise ValueError("bad due date")
                date.fromisoformat(due)
            tid = len(self.items) + 1
            self.items.append({"id": tid, "title": title, "priority": priority, "due": due})
            return tid

        def tasks(self):
            return sorted(self.items, key=lambda x: (x["priority"], x["id"]))
    ''',
    "storage.py": '''
    import json
    from todo import TodoList


    def save(todo, path):
        with open(path, "w") as f:
            json.dump({"version": 2, "tasks": todo.items}, f)


    def load(path):
        with open(path) as f:
            d = json.load(f)
        t = TodoList()
        t.items = d["tasks"]
        return t
    '''})

print("wrote L01-L04")
