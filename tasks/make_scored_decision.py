"""Decision tasks S09-S16: a design decision recorded in session 1, implemented in session 3.
Session 3's prompt leaves the choice open, so only memory carries the decision."""
from scored_common import mk, g

DEC = "Design decision for this project (nothing implements it yet; record it for later work): "

# S09 cache: LFU eviction, ties to the oldest
mk("S09", "decision", "cache.py", "An in-memory cache for a web service.",
   '''
   """In-memory cache."""
   ''',
   '''
   from cache import Cache


   def test_put_get():
       c = Cache()
       c.put("a", 1)
       assert c.get("a") == 1
   ''',
   [f"""
    Add a Cache class to cache.py with put(key, value) and get(key, default=None). It has no size limit yet. Add tests.

    {DEC}when the cache gets a size limit, eviction will be LFU: evict the key whose value was read by get() the fewest times; on a tie, evict the key that was first added earliest.
    """,
    """
    Add stats() to Cache: it returns {"hits": h, "misses": m}, counting get() calls that found or did not find the key. Add tests.
    """,
    """
    Give Cache an optional size limit: Cache(max_items=None). When put() adds a new key and the cache is already full, one key is evicted first. Add tests.
    """],
   [g("Session 1 added Cache with put and get, with tests.", [("Cache put/get", "done")],
      ["Eviction, when added, is LFU: evict the key read by get() the fewest times; on a tie, evict the key first added earliest."]),
    g("Session 2 added Cache.stats() with tests.", [("Cache.stats", "done")])],
   '''
   from cache import Cache


   def test_basic_and_stats():
       c = Cache()
       c.put("a", 1)
       assert c.get("a") == 1 and c.get("b", 0) == 0
       assert c.stats() == {"hits": 1, "misses": 1}


   def test_limit_keeps_size():
       c = Cache(max_items=2)
       for k in "abcd":
           c.put(k, k)
       assert sum(c.get(k) is not None for k in "abcd") == 2


   def test_fact_lfu_eviction():
       c = Cache(max_items=2)
       c.put("a", 1)
       c.put("b", 2)
       c.get("a")
       c.get("a")
       c.get("b")
       c.put("c", 3)  # b has fewer reads than a, though a was read less recently
       assert c.get("a") == 1 and c.get("c") == 3 and c.get("b") is None
       # tie on reads: the key first added earliest goes, even after an update
       c = Cache(max_items=2)
       c.put("x", 1)
       c.put("y", 2)
       c.put("x", 9)  # an update, not a new key: nothing evicted
       c.put("z", 3)
       assert c.get("x") is None and c.get("y") == 2 and c.get("z") == 3
   ''',
   '''
   class Cache:
       def __init__(self, max_items=None):
           self.max_items = max_items
           self.data = {}
           self.reads = {}
           self.hits = 0
           self.misses = 0

       def put(self, key, value):
           if key not in self.data and self.max_items is not None and len(self.data) >= self.max_items:
               victim = min(self.data, key=lambda k: self.reads[k])  # dict order = insertion order
               del self.data[victim]
               del self.reads[victim]
           if key not in self.data:
               self.reads[key] = 0
           self.data[key] = value

       def get(self, key, default=None):
           if key in self.data:
               self.hits += 1
               self.reads[key] += 1
               return self.data[key]
           self.misses += 1
           return default

       def stats(self):
           return {"hits": self.hits, "misses": self.misses}
   ''')

# S10 paging: page numbers start at 0
mk("S10", "decision", "paging.py", "List paging helpers for an API.",
   '''
   """Paging helpers."""
   ''',
   '''
   from paging import clamp


   def test_clamp():
       assert clamp(5, 0, 3) == 3
   ''',
   [f"""
    Add clamp(n, lo, hi) to paging.py: n limited to the range lo..hi. Add tests.

    {DEC}page numbers in this project start at 0, so page 0 is the first page.
    """,
    """
    Add count_pages(n_items, size) to paging.py: how many pages of at most size items are needed for n_items items (0 items need 0 pages). Add tests.
    """,
    """
    Add page(items, number, size) to paging.py: it returns the list of items on page `number`, where each page holds size items; a page past the end is an empty list. Add tests.
    """],
   [g("Session 1 added clamp(n, lo, hi) with tests.", [("clamp", "done")],
      ["Page numbers start at 0: page 0 is the first page."]),
    g("Session 2 added count_pages(n_items, size) with tests.", [("count_pages", "done")])],
   '''
   from paging import clamp, count_pages, page


   def test_clamp_count():
       assert clamp(-1, 0, 3) == 0
       assert count_pages(5, 2) == 3 and count_pages(4, 2) == 2 and count_pages(0, 3) == 0


   def test_fact_zero_based_pages():
       items = [1, 2, 3, 4, 5]
       assert page(items, 0, 2) == [1, 2]
       assert page(items, 1, 2) == [3, 4]
       assert page(items, 2, 2) == [5]
       assert page(items, 3, 2) == []
   ''',
   '''
   def clamp(n, lo, hi):
       return max(lo, min(hi, n))


   def count_pages(n_items, size):
       return -(-n_items // size)


   def page(items, number, size):
       return list(items[number * size:(number + 1) * size])
   ''')

# S11 slug: "_" separator
mk("S11", "decision", "slug.py", "Text helpers for a blog engine.",
   '''
   """Text helpers."""
   ''',
   '''
   from slug import word_count


   def test_word_count():
       assert word_count("a b  c") == 3
   ''',
   [f"""
    Add word_count(text) to slug.py: the number of whitespace-separated words. Add tests.

    {DEC}URL slugs in this project join words with "_" (underscore).
    """,
    """
    Add clean(text) to slug.py: it lowercases text and removes every character that is not a letter, digit or space. Add tests.
    """,
    """
    Add slugify(title) to slug.py: it turns a post title into a URL slug made of the title's lowercase words, without punctuation. Add tests.
    """],
   [g("Session 1 added word_count(text) with tests.", [("word_count", "done")],
      ["URL slugs join words with \"_\" (underscore)."]),
    g("Session 2 added clean(text) with tests.", [("clean", "done")])],
   '''
   from slug import word_count, clean, slugify


   def test_count_clean():
       assert word_count(" x y ") == 2
       assert clean("Hi, You!") == "hi you"


   def test_fact_underscore_slug():
       assert slugify("Hello World") == "hello_world"
       assert slugify("  Hi, there   friend! ") == "hi_there_friend"
   ''',
   '''
   import re


   def word_count(text):
       return len(text.split())


   def clean(text):
       return re.sub(r"[^a-z0-9 ]", "", text.lower())


   def slugify(title):
       return "_".join(clean(title).split())
   ''')

# S12 report: ";" CSV delimiter with header
mk("S12", "decision", "report.py", "Sales report helpers.",
   '''
   """Sales report helpers. A row is a dict with "name", "qty" and "price"."""
   ''',
   '''
   from report import row_total


   def test_row_total():
       assert row_total({"name": "pen", "qty": 2, "price": 3}) == 6
   ''',
   [f"""
    Add row_total(row) to report.py: qty * price for one row. Add tests.

    {DEC}CSV files this project writes use ";" (semicolon) as the delimiter, and their first line is a header row.
    """,
    """
    Add totals(rows) to report.py: a dict mapping each name to the sum of row_total over that name's rows. Add tests.
    """,
    """
    Add export(rows, path) to report.py: it writes the rows to a CSV file with the columns name, qty, price, in that order. Add tests.
    """],
   [g("Session 1 added row_total(row) with tests.", [("row_total", "done")],
      ["CSV files use \";\" (semicolon) as the delimiter, and their first line is a header row."]),
    g("Session 2 added totals(rows) with tests.", [("totals", "done")])],
   '''
   from report import row_total, totals, export


   def test_totals():
       rows = [{"name": "pen", "qty": 2, "price": 3}, {"name": "pen", "qty": 1, "price": 3},
               {"name": "cup", "qty": 1, "price": 5}]
       assert totals(rows) == {"pen": 9, "cup": 5}


   def test_fact_semicolon_csv(tmp_path):
       p = tmp_path / "r.csv"
       export([{"name": "pen", "qty": 2, "price": 3}, {"name": "cup", "qty": 1, "price": 5}], str(p))
       lines = [l.strip() for l in p.read_text().splitlines() if l.strip()]
       assert lines == ["name;qty;price", "pen;2;3", "cup;1;5"]
   ''',
   '''
   import csv


   def row_total(row):
       return row["qty"] * row["price"]


   def totals(rows):
       out = {}
       for r in rows:
           out[r["name"]] = out.get(r["name"], 0) + row_total(r)
       return out


   def export(rows, path):
       with open(path, "w", newline="") as f:
           w = csv.writer(f, delimiter=";")
           w.writerow(["name", "qty", "price"])
           for r in rows:
               w.writerow([r["name"], r["qty"], r["price"]])
   ''')

# S13 log: UTC YYYY-MM-DDTHH:MM:SSZ
mk("S13", "decision", "log.py", "A small in-memory logger.",
   '''
   """In-memory logger."""


   class Logger:
       def __init__(self):
           self.entries = []
   ''',
   '''
   from log import Logger


   def test_new_logger_empty():
       assert Logger().count() == 0
   ''',
   [f"""
    Add count() to Logger in log.py: the number of stored entries. Add tests.

    {DEC}every timestamp this project writes is in UTC, in the form YYYY-MM-DDTHH:MM:SSZ: no microseconds, and "Z" rather than "+00:00".
    """,
    """
    Add lines() to Logger: it returns a copy of the stored entries as a list of strings, oldest first. Add tests.
    """,
    """
    Add log(msg, now) to Logger: now is a timezone-aware datetime.datetime; it stores one entry, the line "<timestamp> <msg>" (the timestamp of now, a space, then msg). Add tests.
    """],
   [g("Session 1 added Logger.count() with tests.", [("Logger.count", "done")],
      ["Every timestamp written is UTC in the form YYYY-MM-DDTHH:MM:SSZ: no microseconds, and \"Z\" rather than \"+00:00\"."]),
    g("Session 2 added Logger.lines() with tests.", [("Logger.lines", "done")])],
   '''
   from datetime import datetime, timedelta, timezone
   from log import Logger


   def test_count_lines():
       lg = Logger()
       lg.log("a", datetime(2026, 1, 5, tzinfo=timezone.utc))
       out = lg.lines()
       out.append("x")
       assert lg.count() == 1 and len(lg.lines()) == 1


   def test_fact_utc_z_timestamp():
       lg = Logger()
       lg.log("hello", datetime(2026, 1, 5, 12, 30, 0, 123456, tzinfo=timezone(timedelta(hours=2))))
       lg.log("bye", datetime(2026, 1, 5, 23, 0, 5, tzinfo=timezone.utc))
       assert lg.lines() == ["2026-01-05T10:30:00Z hello", "2026-01-05T23:00:05Z bye"]
   ''',
   '''
   from datetime import timezone


   class Logger:
       def __init__(self):
           self.entries = []

       def count(self):
           return len(self.entries)

       def lines(self):
           return list(self.entries)

       def log(self, msg, now):
           ts = now.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
           self.entries.append(f"{ts} {msg}")
   ''')

# S14 tickets: ids "T0001"
mk("S14", "decision", "tickets.py", "A ticket tracker.",
   '''
   """Ticket tracker. tickets maps a ticket id to {"title": str, "open": bool}."""


   class TicketBook:
       def __init__(self):
           self.tickets = {}
   ''',
   '''
   from tickets import TicketBook


   def test_empty():
       assert TicketBook().count() == 0
   ''',
   [f"""
    Add count() to TicketBook in tickets.py: the number of tickets. Add tests.

    {DEC}ticket ids are strings made of "T" and a 4-digit number, starting at "T0001", then "T0002", and so on.
    """,
    """
    Add close(ticket_id) and open_titles() to TicketBook: close marks that ticket as not open; open_titles returns the titles of the open tickets in insertion order. Add tests (they can fill self.tickets directly).
    """,
    """
    Add add(title) to TicketBook: it stores a new open ticket and returns its id. Add tests.
    """],
   [g("Session 1 added TicketBook.count() with tests.", [("TicketBook.count", "done")],
      ["Ticket ids are strings of \"T\" and a 4-digit number: \"T0001\", then \"T0002\", and so on."]),
    g("Session 2 added close(ticket_id) and open_titles() with tests.", [("close, open_titles", "done")])],
   '''
   from tickets import TicketBook


   def test_add_close():
       b = TicketBook()
       i = b.add("x")
       b.add("y")
       b.close(i)
       assert b.open_titles() == ["y"] and b.count() == 2


   def test_fact_ticket_ids():
       b = TicketBook()
       assert b.add("a") == "T0001"
       assert b.add("b") == "T0002"
       assert list(b.tickets) == ["T0001", "T0002"]
   ''',
   '''
   class TicketBook:
       def __init__(self):
           self.tickets = {}

       def count(self):
           return len(self.tickets)

       def close(self, ticket_id):
           self.tickets[ticket_id]["open"] = False

       def open_titles(self):
           return [t["title"] for t in self.tickets.values() if t["open"]]

       def add(self, title):
           tid = f"T{len(self.tickets) + 1:04d}"
           self.tickets[tid] = {"title": title, "open": True}
           return tid
   ''')

# S15 config: case-insensitive keys
mk("S15", "decision", "config.py", "Config file helpers.",
   '''
   """Config file helpers."""
   ''',
   '''
   from config import parse_bool


   def test_parse_bool():
       assert parse_bool("yes") is True
   ''',
   [f"""
    Add parse_bool(s) to config.py: True for "yes", "true", "1" or "on", False for anything else, ignoring case and surrounding spaces. Add tests.

    {DEC}looking up a config key ignores letter case, so "PORT", "Port" and "port" name the same key.
    """,
    """
    Add load(text) to config.py: it parses "key=value" lines into a dict of strings, stripping spaces around keys and values and skipping blank lines and lines starting with "#". Add tests.
    """,
    """
    Add get(cfg, key, default=None) to config.py: it returns the value stored for key in a dict made by load(), or default when there is none. Add tests.
    """],
   [g("Session 1 added parse_bool(s) with tests.", [("parse_bool", "done")],
      ["Config key lookup ignores letter case: \"PORT\", \"Port\" and \"port\" name the same key."]),
    g("Session 2 added load(text) with tests.", [("load", "done")])],
   '''
   from config import parse_bool, load, get


   def test_bool_load():
       assert parse_bool(" ON ") is True and parse_bool("no") is False
       assert load("a = 1\\n# c\\n\\nb=two") == {"a": "1", "b": "two"}


   def test_get_default():
       assert get(load("a=1"), "zzz", "d") == "d"


   def test_fact_case_insensitive_get():
       cfg = load("Port = 8080\\nhost=x")
       assert get(cfg, "PORT") == "8080"
       assert get(cfg, "port") == "8080"
       assert get(cfg, "HOST") == "x"
   ''',
   '''
   def parse_bool(s):
       return s.strip().lower() in ("yes", "true", "1", "on")


   def load(text):
       out = {}
       for line in text.splitlines():
           line = line.strip()
           if not line or line.startswith("#"):
               continue
           k, v = line.split("=", 1)
           out[k.strip()] = v.strip()
       return out


   def get(cfg, key, default=None):
       for k, v in cfg.items():
           if k.lower() == key.lower():
               return v
       return default
   ''')

# S16 scores: averages truncated to int
mk("S16", "decision", "scores.py", "Score helpers for a game.",
   '''
   """Score helpers. Scores are numbers from 0 to 100."""
   ''',
   '''
   from scores import clamp_score


   def test_clamp():
       assert clamp_score(120) == 100
   ''',
   [f"""
    Add clamp_score(s) to scores.py: s limited to the range 0..100. Add tests.

    {DEC}every average this project computes is truncated to an int (the fractional part dropped), never rounded and never returned as a float.
    """,
    """
    Add best(scores) to scores.py: the highest score in a non-empty list. Add tests.
    """,
    """
    Add average(scores) to scores.py: the average of a non-empty list of scores. Add tests.
    """],
   [g("Session 1 added clamp_score(s) with tests.", [("clamp_score", "done")],
      ["Every average is truncated to an int (fractional part dropped), never rounded and never a float."]),
    g("Session 2 added best(scores) with tests.", [("best", "done")])],
   '''
   from scores import clamp_score, best, average


   def test_clamp_best():
       assert clamp_score(-3) == 0 and best([3, 9, 4]) == 9


   def test_fact_truncated_average():
       r = average([1, 2])
       assert r == 1 and type(r) is int
       assert average([2, 3, 3]) == 2
       assert average([99, 100]) == 99
       assert type(average([4, 6])) is int
   ''',
   '''
   def clamp_score(s):
       return max(0, min(100, s))


   def best(scores):
       return max(scores)


   def average(scores):
       return int(sum(scores) / len(scores))
   ''')

print("decision ok")
