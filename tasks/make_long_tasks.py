"""R-014 long projects: 8 sessions, a repo of several modules, 12 facts stated in sessions 1-6.
Each project gets repo/, sessions.json, hidden/ and, outside repo/, ref/ (full reference modules,
used only by check_long.py). Usage: python make_long_tasks.py
v2 (2026-10-19): the prompts no longer say "record it for later work", and each project has 9
facts (2 superseded, 2 unfinished) instead of 5. v1 is in _aside/v1_5facts.
v3 (2026-10-20): 8 sessions and 12 facts (3 superseded, 3 unfinished); sessions 5 and 6 are new
fact sessions, and the old sessions 5 and 6 are now 7 and 8. v2 is in _aside/v2_9facts."""
import json
import os
import textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))

RULE = "Project rule (it applies to all later work too): "
DEC = "Design decision for this project: "
CHG = "Change to an earlier decision (it replaces the old one): "
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


def later(fn, step):
    return f"The plan for {fn} has one more step: {step} Do not do that step now; leave it for a later session."


def mk(tid, kinds, readme, modules, prompts, given, hidden, ref):
    """modules: {file: start text}; prompts: 8 session prompts; given: C2g facts for sessions 1-7;
    ref: {file: reference text}."""
    assert len(prompts) == 8 and len(given) == 7
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
           "overdraw": "constraint", "low_stock_sorted": "unfinished", "parse_dollar": "unfinished",
           "bulk": "superseded", "csv_footer": "decision", "rate_range": "constraint",
           "fmt_sep": "unfinished", "header_upper": "superseded", "qty_positive": "constraint"},
   "Stock and money helpers for a small shop.",
   {"money.py": '"""Money helpers."""\n', "store.py": '"""Stock store."""\n',
    "report.py": '"""Stock reports."""\n', "io_csv.py": '"""CSV export."""\n'},
   [f"""
    Add parse_cents(s) to money.py: a price string such as "12.34" becomes the int 1234. Add tests.

    {later("parse_cents", 'it also accepts a leading "$" and "," thousands separators ("$1,234.50" becomes 123450).')}

    {RULE}money is always an int number of cents, and a fractional cent is rounded half-up (half a cent goes up).

    {DEC}CSV files this project writes use ";" (semicolon) as the delimiter, and their first line is a header row.
    """,
    f"""
    Add a Store class to store.py with add(sku, qty), which adds qty units of stock for sku, and qty(sku), which returns the stock of sku (0 for a SKU it does not hold). Add tests.

    {RULE}removing more stock than a SKU has must raise ValueError and leave the stock unchanged.

    {DEC}an invoice line of 10 or more units gets 5% off that line (unit price times quantity), before tax.

    {DEC}a stock CSV file ends with a footer row: the word "total", then the sum of all quantities.

    {DEC}the header row of a stock CSV file is in lower case: sku, qty.
    """,
    f"""
    Add Store.skus() to store.py: the list of SKUs the store holds, sorted. Add tests.

    {DEC}when a SKU's stock reaches 0, the SKU is removed from the store entirely.

    {CHG}CSV files this project writes use a tab character as the delimiter, not ";". Their first line is still a header row.

    {RULE}a tax rate is a number from 0 to 1; any function given a rate outside that range raises ValueError.
    """,
    f"""
    Add low_stock(store, threshold) to report.py: the list of SKUs whose stock is below threshold. Add tests.

    {later("low_stock", "the list must be sorted by stock, lowest first, with ties sorted by SKU.")}

    {CHG}the bulk discount is 10% off an invoice line of 10 or more units, not 5%.
    """,
    f"""
    Add fmt_cents(c) to money.py: an int number of cents becomes a price string with 2 decimals (1234 becomes "12.34", 5 becomes "0.05"). Add tests.

    {later("fmt_cents", 'amounts of 1,000.00 or more get "," thousands separators (123450 becomes "1,234.50").')}
    """,
    f"""
    Add Store.total_units() to store.py: the sum of the stock of every SKU. Add tests.

    {CHG}the header row of a stock CSV file is in upper case: SKU, QTY.

    {RULE}a quantity removed from stock must be a positive int; 0, a negative number or a non-int raises ValueError.
    """,
    """
    Add Store.remove(sku, qty) to store.py, which takes qty units of stock away from sku. Add export_stock(store, path) to io_csv.py: it writes a CSV file with a column for the SKU, a column for the quantity and one row per SKU, in sorted SKU order. Add tests.
    """,
    f"""
    Add invoice_total(lines, rate) to money.py: lines is a list of (unit_cents, qty) pairs, and the result is the subtotal plus tax at rate (for example 0.05 for 5%) on the subtotal. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_cents(s) with tests. Its last step is left for later: accept a leading \"$\" and \",\" thousands separators.",
      [("parse_cents", "done"), ("parse_cents: accept a leading \"$\" and \",\" thousands separators", "todo")],
      ["Money is always an int number of cents; a fractional cent is rounded half-up.",
       "CSV files use \";\" as the delimiter, and their first line is a header row."]),
    g("Session 2 added Store.add and Store.qty with tests.", [("Store.add / Store.qty", "done")],
      ["Removing more stock than a SKU has raises ValueError and leaves the stock unchanged.",
       "An invoice line of 10 or more units gets 5% off that line, before tax.",
       "A stock CSV file ends with a footer row: \"total\", then the sum of all quantities.",
       "The header row of a stock CSV file is in lower case: sku, qty."]),
    g("Session 3 added Store.skus() with tests.", [("Store.skus", "done")],
      ["When a SKU's stock reaches 0, the SKU is removed from the store entirely.",
       "Supersedes the \";\" CSV decision: CSV files use a tab as the delimiter; the first line is still a header row.",
       "A tax rate is from 0 to 1; any function given a rate outside that range raises ValueError."]),
    g("Session 4 added low_stock(store, threshold) with tests. Its last step is left for later: sort the list by stock, lowest first, ties by SKU.",
      [("low_stock", "done"), ("low_stock: sort by stock, lowest first, ties by SKU", "todo")],
      ["Supersedes the 5% bulk discount: an invoice line of 10 or more units gets 10% off, before tax."]),
    g("Session 5 added fmt_cents(c) with tests. Its last step is left for later: \",\" thousands separators for 1,000.00 or more.",
      [("fmt_cents", "done"), ("fmt_cents: \",\" thousands separators for 1,000.00 or more", "todo")]),
    g("Session 6 added Store.total_units() with tests.", [("Store.total_units", "done")],
      ["Supersedes the lower-case header decision: the stock CSV header row is in upper case: SKU, QTY.",
       "A quantity removed from stock must be a positive int; 0, a negative number or a non-int raises ValueError."]),
    g("Session 7 added Store.remove and export_stock with tests.", [("Store.remove", "done"), ("export_stock", "done")])],
   '''
   import re
   import pytest
   from money import fmt_cents, invoice_total, parse_cents
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
       assert _lines(tmp_path)[1:3] == ["A\\t2", "B\\t5"]


   def test_stale_semicolon_csv(tmp_path):
       assert _lines(tmp_path)[1] == "A;2"


   def test_fact_header_upper(tmp_path):
       assert re.split(r"[\\t;,]", _lines(tmp_path)[0]) == ["SKU", "QTY"]


   def test_stale_header_lower(tmp_path):
       assert re.split(r"[\\t;,]", _lines(tmp_path)[0]) == ["sku", "qty"]


   def test_fact_fmt_sep():
       assert fmt_cents(123450) == "1,234.50" and fmt_cents(100000000) == "1,000,000.00"
       assert fmt_cents(5) == "0.05" and fmt_cents(99999) == "999.99"


   def test_fact_qty_positive():
       s = Store()
       s.add("A", 5)
       for bad in (0, -1, 1.5):
           with pytest.raises(ValueError):
               s.remove("A", bad)
       assert s.qty("A") == 5


   def test_fact_csv_footer(tmp_path):
       assert re.split(r"[\\t;,]", _lines(tmp_path)[-1]) == ["total", "7"]


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


   def test_fact_parse_dollar():
       assert parse_cents("$1,234.50") == 123450
       assert parse_cents("2.5") == 250


   def test_fact_bulk():
       assert invoice_total([(100, 10)], 0) == 900
       assert invoice_total([(100, 9)], 0) == 900


   def test_stale_bulk_5pct():
       assert invoice_total([(100, 10)], 0) == 950


   def test_fact_rate_range():
       for bad in (1.5, -0.1):
           with pytest.raises(ValueError):
               invoice_total([(100, 1)], bad)
       assert invoice_total([(100, 1)], 1) == 200
   ''',
   {"money.py": '''
    from decimal import Decimal, ROUND_HALF_UP


    def _round(x):
        return int(Decimal(x).quantize(Decimal(1), ROUND_HALF_UP))


    def parse_cents(s):
        return _round(Decimal(s.strip().lstrip("$").replace(",", "")) * 100)


    def fmt_cents(c):
        return f"{c // 100:,}.{c % 100:02d}"


    def invoice_total(lines, rate):
        if not 0 <= rate <= 1:
            raise ValueError("rate out of range")
        sub = 0
        for c, q in lines:
            line = Decimal(c * q)
            if q >= 10:
                line *= Decimal("0.9")
            sub += _round(line)
        return sub + _round(Decimal(sub) * Decimal(str(rate)))
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

        def total_units(self):
            return sum(self.stock.values())

        def remove(self, sku, qty):
            if type(qty) is not int or qty <= 0:
                raise ValueError("quantity must be a positive int")
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
            w.writerow(["SKU", "QTY"])
            for s in store.skus():
                w.writerow([s, store.qty(s)])
            w.writerow(["total", sum(store.qty(s) for s in store.skus())])
    '''})

# ---------------------------------------------------------------- L02 calendar
mk("L02", {"ids": "superseded", "empty_title": "constraint", "sorted": "decision",
           "minutes": "decision", "slug": "unfinished", "iso_t": "unfinished",
           "end_order": "constraint", "overlap": "superseded", "slug_key": "decision",
           "fmt_minutes": "unfinished", "title_max": "superseded", "max_24h": "constraint"},
   "A small calendar of events.",
   {"timeutil.py": '"""Time helpers."""\n', "text.py": '"""Text helpers."""\n',
    "events.py": '"""The calendar."""\n'},
   [f"""
    Add parse_ts(s) to timeutil.py: it parses a "YYYY-MM-DD HH:MM:SS" string into a datetime. Add tests.

    {later("parse_ts", 'it also accepts a "T" in place of the space between the date and the time ("2026-01-05T10:00:00").')}

    {DEC}durations this project reports are whole minutes, as an int, rounded down.

    {RULE}an event whose end is before its start is rejected with ValueError (an end equal to the start is allowed).
    """,
    f"""
    Add fmt_ts(dt) to timeutil.py: the inverse of parse_ts. Add tests.

    {DEC}event IDs are "E" followed by a 4-digit counter that starts at 1 (E0001, E0002, ...).

    {DEC}events may overlap in time; the calendar does not check for overlaps.

    {DEC}an event title is at most 80 characters after clean_title; a longer title is rejected with ValueError.
    """,
    f"""
    Add clean_title(s) to text.py: it strips both ends and turns every run of whitespace inside into one space. Add tests.

    {RULE}an event title that is empty after clean_title is rejected with ValueError.

    {DEC}listings of events are sorted by start time, then by title.

    {CHG}the calendar rejects an event that overlaps an existing one with ValueError. Two events overlap when each starts before the other ends, so an event that starts exactly when another ends is allowed.
    """,
    f"""
    Add slug(title) to text.py: the title in lower case, with spaces replaced by "-". Add tests.

    {later("slug", 'characters other than a-z, 0-9 and "-" are dropped.')}

    {CHG}event IDs are "EVT-" followed by a 5-digit counter that starts at 1 (EVT-00001, EVT-00002, ...).

    {DEC}every event dict that a listing returns also has a "slug" key holding slug(title).
    """,
    f"""
    Add fmt_minutes(n) to timeutil.py: a number of minutes as hours and minutes, "1h 30m" for 90 and "0h 45m" for 45. Add tests.

    {later("fmt_minutes", 'a part that is zero is left out: 45 becomes "45m" and 120 becomes "2h".')}
    """,
    f"""
    Add is_weekend(s) to timeutil.py: True if the "YYYY-MM-DD HH:MM:SS" timestamp s falls on a Saturday or a Sunday. Add tests.

    {CHG}an event title is at most 40 characters after clean_title, not 80; a longer title is rejected with ValueError.

    {RULE}an event lasts at most 24 hours; a longer event is rejected with ValueError (exactly 24 hours is allowed).
    """,
    """
    Add a Calendar class to events.py. add(title, start, end) stores an event and returns its ID; start and end are "YYYY-MM-DD HH:MM:SS" strings, and the title is cleaned with clean_title. events() returns the stored events as a list of dicts with the keys id, title, start and end. Add tests.
    """,
    f"""
    Add Calendar.duration(event_id) to events.py: the length of that event. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_ts(s) with tests. Its last step is left for later: also accept \"T\" between date and time.",
      [("parse_ts", "done"), ("parse_ts: also accept \"T\" between date and time", "todo")],
      ["Durations are whole minutes, as an int, rounded down.",
       "An event whose end is before its start is rejected with ValueError; end equal to start is allowed."]),
    g("Session 2 added fmt_ts(dt) with tests.", [("fmt_ts", "done")],
      ["Event IDs are \"E\" plus a 4-digit counter from 1 (E0001, E0002, ...).",
       "Events may overlap in time; the calendar does not check for overlaps.",
       "An event title is at most 80 characters after clean_title; a longer title is rejected with ValueError."]),
    g("Session 3 added clean_title(s) with tests.", [("clean_title", "done")],
      ["An event title that is empty after clean_title is rejected with ValueError.",
       "Listings of events are sorted by start time, then by title.",
       "Supersedes the overlap decision: an event that overlaps an existing one is rejected with ValueError; touching (one starts when the other ends) is allowed."]),
    g("Session 4 added slug(title) with tests. Its last step is left for later: drop characters other than a-z, 0-9 and \"-\".",
      [("slug", "done"), ("slug: drop characters other than a-z, 0-9 and \"-\"", "todo")],
      ["Supersedes the E0001 ID decision: event IDs are \"EVT-\" plus a 5-digit counter from 1 (EVT-00001, ...).",
       "Every event dict a listing returns also has a \"slug\" key holding slug(title)."]),
    g("Session 5 added fmt_minutes(n) with tests. Its last step is left for later: leave out a part that is zero (\"45m\", \"2h\").",
      [("fmt_minutes", "done"), ("fmt_minutes: leave out a zero part (\"45m\", \"2h\")", "todo")]),
    g("Session 6 added is_weekend(s) with tests.", [("is_weekend", "done")],
      ["Supersedes the 80-character title decision: an event title is at most 40 characters after clean_title; longer raises ValueError.",
       "An event lasts at most 24 hours; a longer event is rejected with ValueError (exactly 24 hours is allowed)."]),
    g("Session 7 added the Calendar class (add, events) with tests.", [("Calendar.add / Calendar.events", "done")])],
   '''
   from datetime import datetime
   import pytest
   from events import Calendar
   from text import slug
   from timeutil import fmt_minutes, parse_ts


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
       c.add("mid", "2026-01-05 09:00:00", "2026-01-05 10:00:00")
       c.add("early", "2026-01-05 08:00:00", "2026-01-05 09:00:00")
       assert [e["title"] for e in c.events()] == ["early", "mid", "late"]


   def test_fact_minutes():
       c = Calendar()
       a = c.add("a", "2026-01-05 10:00:00", "2026-01-05 10:01:30")
       b = c.add("b", "2026-01-05 12:00:00", "2026-01-05 14:00:59")
       assert c.duration(a) == 1 and c.duration(b) == 120
       assert type(c.duration(a)) is int


   def test_fact_slug():
       assert slug("Hi, There!") == "hi-there"
       assert slug("Q3 plan (draft)") == "q3-plan-draft"


   def test_fact_iso_t():
       assert parse_ts("2026-01-05T10:00:00") == datetime(2026, 1, 5, 10, 0, 0)
       assert parse_ts("2026-01-05 10:00:00") == datetime(2026, 1, 5, 10, 0, 0)


   def test_fact_end_order():
       c = Calendar()
       with pytest.raises(ValueError):
           c.add("x", "2026-01-05 10:00:00", "2026-01-05 09:59:00")
       c.add("y", "2026-01-05 12:00:00", "2026-01-05 12:00:00")


   def test_fact_overlap():
       c = Calendar()
       c.add("a", "2026-01-05 10:00:00", "2026-01-05 11:00:00")
       with pytest.raises(ValueError):
           c.add("b", "2026-01-05 10:30:00", "2026-01-05 11:30:00")
       c.add("c", "2026-01-05 11:00:00", "2026-01-05 12:00:00")


   def test_stale_overlap_allowed():
       c = Calendar()
       c.add("a", "2026-01-05 10:00:00", "2026-01-05 11:00:00")
       c.add("b", "2026-01-05 10:30:00", "2026-01-05 11:30:00")
       assert len(c.events()) == 2


   def test_fact_slug_key():
       c = Calendar()
       c.add("Team Sync", "2026-01-05 10:00:00", "2026-01-05 11:00:00")
       assert c.events()[0]["slug"] == "team-sync"


   def test_fact_fmt_minutes():
       assert fmt_minutes(90) == "1h 30m"
       assert fmt_minutes(45) == "45m" and fmt_minutes(120) == "2h"


   def _add_title(n):
       c = Calendar()
       c.add("t" * n, "2026-01-05 10:00:00", "2026-01-05 11:00:00")
       return len(c.events())


   def test_fact_title_max():
       assert _add_title(40) == 1
       with pytest.raises(ValueError):
           _add_title(41)


   def test_stale_title_80():
       assert _add_title(60) == 1


   def test_fact_max_24h():
       c = Calendar()
       with pytest.raises(ValueError):
           c.add("x", "2026-01-05 10:00:00", "2026-01-06 10:01:00")
       c.add("y", "2026-01-07 10:00:00", "2026-01-08 10:00:00")
   ''',
   {"timeutil.py": '''
    from datetime import datetime

    FMT = "%Y-%m-%d %H:%M:%S"


    def parse_ts(s):
        return datetime.strptime(s.replace("T", " "), FMT)


    def fmt_ts(dt):
        return dt.strftime(FMT)


    def fmt_minutes(n):
        h, m = divmod(n, 60)
        return " ".join(p for p in (f"{h}h" if h else "", f"{m}m" if m else "") if p) or "0m"


    def is_weekend(s):
        return parse_ts(s).weekday() >= 5
    ''',
    "text.py": '''
    import re


    def clean_title(s):
        return " ".join(s.split())


    def slug(title):
        return re.sub(r"[^a-z0-9-]", "", title.lower().replace(" ", "-"))
    ''',
    "events.py": '''
    from text import clean_title, slug
    from timeutil import parse_ts


    class Calendar:
        def __init__(self):
            self.items = []

        def add(self, title, start, end):
            title = clean_title(title)
            if not title:
                raise ValueError("empty title")
            if len(title) > 40:
                raise ValueError("title too long")
            s, e = parse_ts(start), parse_ts(end)
            if e < s:
                raise ValueError("end before start")
            if (e - s).total_seconds() > 24 * 3600:
                raise ValueError("event longer than 24 hours")
            for x in self.items:
                if s < parse_ts(x["end"]) and parse_ts(x["start"]) < e:
                    raise ValueError("overlaps an existing event")
            eid = f"EVT-{len(self.items) + 1:05d}"
            self.items.append({"id": eid, "title": title, "start": start, "end": end})
            return eid

        def events(self):
            items = sorted(self.items, key=lambda e: (parse_ts(e["start"]), e["title"]))
            return [dict(e, slug=slug(e["title"])) for e in items]

        def duration(self, event_id):
            e = next(e for e in self.items if e["id"] == event_id)
            return int((parse_ts(e["end"]) - parse_ts(e["start"])).total_seconds() // 60)
    '''})

# ---------------------------------------------------------------- L03 grade book
mk("L03", {"range": "constraint", "ids": "decision", "plain_mean": "superseded",
           "ranking_ties": "decision", "truncate": "unfinished", "comments": "unfinished",
           "min_scores": "superseded", "int_type": "constraint", "max_scores": "decision",
           "letter_none": "unfinished", "id_len": "superseded", "id_alnum": "constraint"},
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

    {later("read_lines", 'lines whose first non-space character is "#" are comments and are skipped too.')}

    {DEC}student IDs are case-insensitive: they are stored in upper case, and lookups accept any case.

    {DEC}rankings include only students with at least 3 scores.

    {DEC}a student ID is at most 8 characters; recording a score for a longer ID raises ValueError.
    """,
    f"""
    Add bar(n) to report.py: a string of n "#" characters. Add tests.

    {CHG}a student's average is the plain mean of all their scores (no score is dropped), rounded to 1 decimal place.

    {DEC}rankings sort students by average, highest first, and break ties by student ID in ascending order.

    {RULE}a score must be an int; a float or a bool raises TypeError, before any range check.
    """,
    f"""
    Add format_row(name, avg) to report.py: the name left-aligned in 20 characters, then the average right-aligned in 6 characters with 1 decimal place. Add tests.

    {later("format_row", 'a name longer than 20 characters is cut to its first 17 characters followed by "...".')}

    {CHG}rankings include only students with at least 2 scores, not 3.

    {DEC}a student holds at most 10 scores; adding an 11th score raises ValueError.
    """,
    f"""
    Add letter(avg) to report.py: the letter grade for an average: "A" from 90, "B" from 80, "C" from 70, "D" from 60, otherwise "F". Add tests.

    {later("letter", 'letter(None), for a student with no average, returns "-".')}
    """,
    f"""
    Add pct(part, whole) to report.py: part as a percent of whole, rounded to 1 decimal place. Add tests.

    {CHG}a student ID is at most 6 characters, not 8; recording a score for a longer ID raises ValueError.

    {RULE}a student ID holds only letters and digits; recording a score for an ID with any other character raises ValueError.
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
    g("Session 2 added read_lines(path) with tests. Its last step is left for later: skip comment lines (first non-space character \"#\").",
      [("read_lines", "done"), ("read_lines: skip lines whose first non-space character is \"#\"", "todo")],
      ["Student IDs are case-insensitive: stored in upper case, lookups accept any case.",
       "Rankings include only students with at least 3 scores.",
       "A student ID is at most 8 characters; recording a score for a longer ID raises ValueError."]),
    g("Session 3 added bar(n) with tests.", [("bar", "done")],
      ["Supersedes the drop-lowest decision: the average is the plain mean of all scores, rounded to 1 decimal place.",
       "Rankings sort by average, highest first; ties by student ID, ascending.",
       "A score must be an int; a float or a bool raises TypeError, before any range check."]),
    g("Session 4 added format_row(name, avg) with tests. Its last step is left for later: cut names longer than 20 characters to 17 characters plus \"...\".",
      [("format_row", "done"), ("format_row: cut names over 20 characters to 17 + \"...\"", "todo")],
      ["Supersedes the 3-score ranking decision: rankings include only students with at least 2 scores.",
       "A student holds at most 10 scores; adding an 11th raises ValueError."]),
    g("Session 5 added letter(avg) with tests. Its last step is left for later: letter(None) returns \"-\".",
      [("letter", "done"), ("letter: letter(None) returns \"-\"", "todo")]),
    g("Session 6 added pct(part, whole) with tests.", [("pct", "done")],
      ["Supersedes the 8-character ID decision: a student ID is at most 6 characters; a longer ID raises ValueError.",
       "A student ID holds only letters and digits; any other character raises ValueError."]),
    g("Session 7 added the Gradebook class (add_score, average) with tests.", [("Gradebook.add_score / Gradebook.average", "done")])],
   '''
   import pytest
   from grades import Gradebook
   from report import format_row, letter
   from io_util import read_lines


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
       b.add_score("S1", 60)
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
       for sid, s in (("S2", 80), ("S1", 80), ("S3", 90)):
           b.add_score(sid, s)
           b.add_score(sid, s)
       assert b.ranking() == ["S3", "S1", "S2"]


   def test_fact_truncate():
       assert format_row("A" * 25, 1.0) == "A" * 17 + "..." + "   1.0"
       assert format_row("Bo", 75.5) == "Bo" + " " * 18 + "  75.5"


   def test_fact_comments(tmp_path):
       p = tmp_path / "x.txt"
       p.write_text("a\\n# note\\n   # indented note\\n\\nb\\n")
       assert read_lines(str(p)) == ["a", "b"]


   def _two_scores_ranking():
       b = Gradebook()
       b.add_score("S1", 70)
       b.add_score("S1", 80)
       b.add_score("S2", 90)
       return b.ranking()


   def test_fact_min_scores():
       assert _two_scores_ranking() == ["S1"]


   def test_stale_min_3_scores():
       assert _two_scores_ranking() == []


   def test_fact_int_type():
       b = Gradebook()
       for bad in (80.0, True, 500.5):
           with pytest.raises(TypeError):
               b.add_score("A1", bad)
       assert b.average("A1") is None


   def test_fact_max_scores():
       b = Gradebook()
       for _ in range(10):
           b.add_score("A1", 50)
       with pytest.raises(ValueError):
           b.add_score("A1", 50)
       assert b.average("A1") == 50.0


   def test_fact_letter_none():
       assert letter(None) == "-"
       assert letter(90) == "A" and letter(59.9) == "F"


   def test_fact_id_len():
       b = Gradebook()
       with pytest.raises(ValueError):
           b.add_score("ABCDEFG", 50)
       b.add_score("ABCDEF", 50)
       assert b.average("ABCDEF") == 50.0


   def test_stale_id_8():
       b = Gradebook()
       b.add_score("ABCDEFGH", 50)
       assert b.average("ABCDEFGH") == 50.0


   def test_fact_id_alnum():
       b = Gradebook()
       for bad in ("A-1", "A 1", "A_1"):
           with pytest.raises(ValueError):
               b.add_score(bad, 50)
       b.add_score("Ab12", 50)
   ''',
   {"students.py": '''
    def normalize_name(s):
        return " ".join(w.capitalize() for w in s.split())
    ''',
    "io_util.py": '''
    def read_lines(path):
        with open(path) as f:
            return [l.rstrip("\\r\\n") for l in f if l.strip() and not l.lstrip().startswith("#")]
    ''',
    "report.py": '''
    def bar(n):
        return "#" * n


    def format_row(name, avg):
        if len(name) > 20:
            name = name[:17] + "..."
        return f"{name:<20}{avg:>6.1f}"


    def letter(avg):
        if avg is None:
            return "-"
        for cut, g in ((90, "A"), (80, "B"), (70, "C"), (60, "D")):
            if avg >= cut:
                return g
        return "F"


    def pct(part, whole):
        return round(100 * part / whole, 1)
    ''',
    "grades.py": '''
    class Gradebook:
        def __init__(self):
            self.scores = {}

        def add_score(self, student_id, score):
            if len(student_id) > 6 or not student_id.isalnum():
                raise ValueError("bad student ID")
            if type(score) is not int:
                raise TypeError("score must be an int")
            if not 0 <= score <= 100:
                raise ValueError("score out of range")
            s = self.scores.setdefault(student_id.upper(), [])
            if len(s) >= 10:
                raise ValueError("too many scores")
            s.append(score)

        def average(self, student_id):
            s = self.scores.get(student_id.upper())
            return round(sum(s) / len(s), 1) if s else None

        def ranking(self):
            ids = [i for i, s in self.scores.items() if len(s) >= 2]
            return sorted(ids, key=lambda i: (-self.average(i), i))
    '''})

# ---------------------------------------------------------------- L04 to-do list
mk("L04", {"sorted": "decision", "save_format": "superseded", "due": "constraint",
           "tags": "unfinished", "title_len": "constraint", "plural_y": "unfinished",
           "priority_range": "constraint", "indent": "superseded", "done_key": "decision",
           "truncate": "unfinished", "save_order": "superseded", "unique_title": "constraint"},
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

    {later("plural", 'a word that ends in a consonant followed by "y" takes "ies" ("2 entries"), while a word that ends in a vowel followed by "y" just adds "s" ("2 days").')}

    {RULE}a due date is a "YYYY-MM-DD" string for a real calendar date, or None for no due date; anything else raises ValueError.

    {DEC}the save file is compact JSON, written on a single line with no indentation.

    {DEC}the save file lists the tasks in the order they were added.
    """,
    f"""
    Add parse_tags(s) to util.py: it splits a comma-separated string into tags, strips spaces around each tag and drops empty tags. Add tests.

    {later("parse_tags", "tags are lowercased, and duplicates are removed, keeping the first.")}

    {RULE}a task priority is an int from 1 to 3; anything else raises ValueError.

    {DEC}every task dict has a "done" key, which is False when the task is added.
    """,
    f"""
    Add join_tags(tags) to util.py: the tags joined with ", ". Add tests.

    {CHG}the save file is JSON with two top-level keys: "version", set to 2, and "tasks", holding the list of tasks.

    {RULE}a task title is at most 60 characters after stripping both ends; a longer title raises ValueError.

    {CHG}the save file is indented JSON with an indent of 2 spaces, not compact.
    """,
    f"""
    Add truncate(s, n) to util.py: the first n characters of s. Add tests.

    {later("truncate", 'when s is longer than n, it is cut to n - 3 characters followed by "...", so the result is n characters long ("abcdefgh" with n = 5 gives "ab...").')}
    """,
    f"""
    Add word_count(s) to util.py: the number of whitespace-separated words in s. Add tests.

    {CHG}the save file lists the tasks in list order (sorted as tasks() returns them), not in the order they were added.

    {RULE}task titles are unique, compared after stripping both ends and ignoring case; adding a duplicate title raises ValueError.
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
    g("Session 2 added plural(n, word) with tests. Its last step is left for later: consonant + \"y\" takes \"ies\"; vowel + \"y\" just adds \"s\".",
      [("plural", "done"), ("plural: consonant + \"y\" takes \"ies\", vowel + \"y\" adds \"s\"", "todo")],
      ["A due date is a \"YYYY-MM-DD\" string for a real calendar date, or None; anything else raises ValueError.",
       "The save file is compact JSON on a single line, with no indentation.",
       "The save file lists the tasks in the order they were added."]),
    g("Session 3 added parse_tags(s) with tests. Its last step is left for later: lowercase the tags and remove duplicates, keeping the first.",
      [("parse_tags", "done"), ("parse_tags: lowercase, remove duplicates keeping the first", "todo")],
      ["A task priority is an int from 1 to 3; anything else raises ValueError.",
       "Every task dict has a \"done\" key, False when the task is added."]),
    g("Session 4 added join_tags(tags) with tests.", [("join_tags", "done")],
      ["Supersedes the \"items\" save-file decision: the save file has \"version\": 2 and \"tasks\", the list of tasks.",
       "A task title is at most 60 characters after stripping; a longer title raises ValueError.",
       "Supersedes the compact save-file decision: the save file is indented JSON with an indent of 2 spaces."]),
    g("Session 5 added truncate(s, n) with tests. Its last step is left for later: a longer s is cut to n - 3 characters plus \"...\".",
      [("truncate", "done"), ("truncate: cut a longer s to n - 3 characters plus \"...\"", "todo")]),
    g("Session 6 added word_count(s) with tests.", [("word_count", "done")],
      ["Supersedes the added-order save decision: the save file lists tasks in list order (as tasks() returns them).",
       "Task titles are unique, compared after stripping and ignoring case; a duplicate raises ValueError."]),
    g("Session 7 added the TodoList class (add, tasks) with tests.", [("TodoList.add / TodoList.tasks", "done")])],
   '''
   import json
   import pytest
   from todo import TodoList
   from storage import save, load
   from util import parse_tags, plural, truncate


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


   def _saved_text(tmp_path):
       t = TodoList()
       t.add("a", 1)
       p = tmp_path / "t.json"
       save(t, str(p))
       return p.read_text()


   def test_fact_save_format(tmp_path):
       d = json.loads(_saved_text(tmp_path))
       assert d.get("version") == 2 and isinstance(d.get("tasks"), list) and len(d["tasks"]) == 1


   def test_stale_items_key(tmp_path):
       assert "items" in json.loads(_saved_text(tmp_path))


   def test_fact_indent(tmp_path):
       assert '\\n  "' in _saved_text(tmp_path)


   def test_stale_compact(tmp_path):
       assert "\\n" not in _saved_text(tmp_path).strip()


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


   def test_fact_plural_y():
       assert plural(2, "entry") == "2 entries" and plural(1, "entry") == "1 entry"
       assert plural(2, "day") == "2 days" and plural(2, "task") == "2 tasks"


   def test_fact_priority_range():
       t = TodoList()
       for bad in (0, 4, "1"):
           with pytest.raises(ValueError):
               t.add("x", bad)
       t.add("x", 3)


   def test_fact_done_key():
       t = TodoList()
       t.add("a", 1)
       assert t.tasks()[0]["done"] is False


   def test_fact_truncate():
       assert truncate("abcdefgh", 5) == "ab..." and truncate("abc", 5) == "abc"
       assert truncate("abcde", 5) == "abcde"


   def _saved_titles(tmp_path):
       t = TodoList()
       t.add("a", 2)
       t.add("b", 1)
       p = tmp_path / "t.json"
       save(t, str(p))
       d = json.loads(p.read_text())
       return [x["title"] for x in d.get("tasks", d.get("items", []))]


   def test_fact_save_order(tmp_path):
       assert _saved_titles(tmp_path) == ["b", "a"]


   def test_stale_added_order(tmp_path):
       assert _saved_titles(tmp_path) == ["a", "b"]


   def test_fact_unique_title():
       t = TodoList()
       t.add("Pay rent", 1)
       for dup in ("pay rent", "  PAY RENT "):
           with pytest.raises(ValueError):
               t.add(dup, 2)
       assert len(t.tasks()) == 1
   ''',
   {"util.py": '''
    def is_blank(s):
        return not s.strip()


    def plural(n, word):
        if n == 1:
            return f"{n} {word}"
        if len(word) > 1 and word.endswith("y") and word[-2] not in "aeiou":
            return f"{n} {word[:-1]}ies"
        return f"{n} {word}s"


    def parse_tags(s):
        out = []
        for t in s.split(","):
            t = t.strip().lower()
            if t and t not in out:
                out.append(t)
        return out


    def join_tags(tags):
        return ", ".join(tags)


    def truncate(s, n):
        return s if len(s) <= n else s[:n - 3] + "..."


    def word_count(s):
        return len(s.split())
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
            if any(x["title"].lower() == title.lower() for x in self.items):
                raise ValueError("duplicate title")
            if type(priority) is not int or not 1 <= priority <= 3:
                raise ValueError("bad priority")
            if due is not None:
                if len(due) != 10:
                    raise ValueError("bad due date")
                date.fromisoformat(due)
            tid = len(self.items) + 1
            self.items.append({"id": tid, "title": title, "priority": priority, "due": due, "done": False})
            return tid

        def tasks(self):
            return sorted(self.items, key=lambda x: (x["priority"], x["id"]))
    ''',
    "storage.py": '''
    import json
    from todo import TodoList


    def save(todo, path):
        with open(path, "w") as f:
            json.dump({"version": 2, "tasks": todo.tasks()}, f, indent=2)


    def load(path):
        with open(path) as f:
            d = json.load(f)
        t = TodoList()
        t.items = d["tasks"]
        return t
    '''})

print("wrote L01-L04")
