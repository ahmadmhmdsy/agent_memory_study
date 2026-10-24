"""R-014 scored projects L18-L20 (v3 form: 8 sessions, 12 facts)."""
from long_common import CHG, DEC, FINISH, RULE, g, later, mk

# ---------------------------------------------------------------- L18 URL shortener
mk("L18", {"code_7": "superseded", "expire_90": "superseded", "report_line": "superseded",
           "normalize_host": "unfinished", "stats_day": "unfinished", "strip_www": "unfinished",
           "scheme_check": "constraint", "same_url": "constraint", "alias_rules": "decision",
           "no_confusable": "decision", "report_order": "decision", "report_header": "decision"},
   "A small URL shortener.",
   {"urls.py": '"""URL helpers."""\n', "store.py": '"""The shortener."""\n',
    "report.py": '"""Link reports."""\n'},
   [f"""
    Add normalize(url) to urls.py: a URL without a scheme gets "https://" in front ("example.com/a" becomes "https://example.com/a"); other URLs are returned unchanged. Add tests.

    {later("normalize", 'the host is made lower case and a trailing "/" is removed ("https://Example.COM/a/" becomes "https://example.com/a").')}

    {RULE}only http and https URLs are allowed: any function given a URL with another scheme (such as "ftp://") raises ValueError.

    {DEC}short codes are 6 characters long, letters and digits chosen at random.
    """,
    f"""
    Add a Shortener class to store.py: shorten(url, today) stores normalize(url) under a new short code and returns the code, and expand(code, today) returns the stored URL and records one click on that day, or returns None (recording no click) when the code is unknown or expired. Days are datetime.date. Add tests.

    {RULE}shortening a URL that is already stored returns its existing code instead of a new one.

    {DEC}a link expires 30 days after the day it was shortened: from that day on, expand returns None.

    {DEC}each line of a link report has the form abc123 https://example.com/a 3 (the code, the URL, the clicks).
    """,
    f"""
    Add Shortener.delete(code) to store.py: afterwards expand returns None for that code. Add tests.

    {CHG}a link expires 90 days after the day it was shortened, not 30.

    {DEC}shorten takes an optional alias that is used as the code; an alias must be 3 to 20 letters, digits or hyphens, and an alias that is invalid or already used raises ValueError.

    {DEC}generated codes never contain the characters 0, O, 1, l or I.
    """,
    f"""
    Add Shortener.stats(code) to store.py: the total number of clicks on that code. Add tests.

    {later("Shortener.stats", "it takes an optional day and then counts only the clicks on that day.")}

    {CHG}short codes are 7 characters long, not 6.
    """,
    f"""
    Add domain_of(url) to urls.py: the host of the URL ("https://example.com/a" gives "example.com"). Add tests.

    {later("domain_of", 'a leading "www." is removed ("https://www.example.com" gives "example.com").')}
    """,
    f"""
    Add Shortener.count(today) to store.py: the number of links that are neither expired nor deleted on that day. Add tests.

    {CHG}each line of a link report has the form abc1234 | 3 clicks | https://example.com/a, not abc123 https://example.com/a 3.

    {DEC}a link report lists the links by clicks, most first.

    {DEC}the first line of a link report is the number of links, in the form Links: 3.
    """,
    """
    Add Shortener.by_domain() to store.py: a dict from each domain (as given by domain_of) to the number of stored links for it. Add tests.
    """,
    f"""
    Add write_report(shortener, path) to report.py: it writes a text report with one line per stored link. Add tests. {FINISH}
    """],
   [g("Session 1 added normalize(url) with tests. Its last step is left for later: lower-case host and no trailing \"/\".",
      [("normalize", "done"), ("normalize: lower-case host, drop trailing /", "todo")],
      ["Only http and https URLs are allowed; another scheme raises ValueError in any function.",
       "Short codes are 6 random letters and digits."]),
    g("Session 2 added Shortener.shorten and expand with tests.", [("Shortener.shorten / expand", "done")],
      ["Shortening a URL that is already stored returns its existing code.",
       "A link expires 30 days after it was shortened; from then expand returns None.",
       "A report line has the form abc123 https://example.com/a 3."]),
    g("Session 3 added Shortener.delete with tests.", [("Shortener.delete", "done")],
      ["Supersedes 30 days: a link expires 90 days after it was shortened.",
       "shorten takes an optional alias: 3-20 letters, digits or hyphens; invalid or used raises ValueError.",
       "Generated codes never contain 0, O, 1, l or I."]),
    g("Session 4 added Shortener.stats(code) with tests. Its last step is left for later: an optional day.",
      [("Shortener.stats", "done"), ("Shortener.stats: optional day", "todo")],
      ["Supersedes 6: short codes are 7 characters long."]),
    g("Session 5 added domain_of(url) with tests. Its last step is left for later: remove a leading www.",
      [("domain_of", "done"), ("domain_of: remove www.", "todo")]),
    g("Session 6 added Shortener.count(today) with tests.", [("Shortener.count", "done")],
      ["Supersedes abc123 https://example.com/a 3: a report line has the form abc1234 | 3 clicks | https://example.com/a.",
       "A report lists links by clicks, most first.",
       "The first report line is Links: 3."]),
    g("Session 7 added Shortener.by_domain() with tests.", [("Shortener.by_domain", "done")])],
   '''
   import re
   from datetime import date, timedelta
   import pytest
   from urls import domain_of, normalize
   from store import Shortener
   from report import write_report

   D0 = date(2026, 6, 1)


   def test_short_basic():
       s = Shortener()
       c = s.shorten("example.com/a", D0)
       assert s.expand(c, D0) == "https://example.com/a" and s.stats(c) == 1
       assert s.expand("nope", D0) is None and s.count(D0) == 1
       assert s.by_domain() == {"example.com": 1} and domain_of("https://example.com/a") == "example.com"
       s.delete(c)
       assert s.expand(c, D0) is None and s.count(D0) == 0


   def test_fact_code_7():
       s = Shortener()
       codes = [s.shorten(f"https://e.com/{i}", D0) for i in range(30)]
       assert all(len(c) == 7 for c in codes) and len(set(codes)) == 30


   def test_stale_code_6():
       s = Shortener()
       assert all(len(s.shorten(f"https://e.com/{i}", D0)) == 6 for i in range(30))


   def test_fact_expire_90():
       s = Shortener()
       c = s.shorten("https://e.com/a", D0)
       assert s.expand(c, D0 + timedelta(days=60)) == "https://e.com/a"
       assert s.expand(c, D0 + timedelta(days=90)) is None


   def test_stale_expire_30():
       s = Shortener()
       c = s.shorten("https://e.com/a", D0)
       assert s.expand(c, D0 + timedelta(days=60)) is None


   def _rep(tmp_path, s):
       p = tmp_path / "r.txt"
       write_report(s, str(p))
       return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def _docs():
       s = Shortener()
       s.shorten("https://example.com/docs", D0, alias="docs")
       for _ in range(3):
           s.expand("docs", D0)
       return s


   def test_fact_report_line(tmp_path):
       assert "docs | 3 clicks | https://example.com/docs" in _rep(tmp_path, _docs())


   def test_stale_report_plain(tmp_path):
       assert "docs https://example.com/docs 3" in _rep(tmp_path, _docs())


   def _three():
       s = Shortener()
       for a, n in (("aaa", 1), ("bbb", 3), ("ccc", 2)):
           s.shorten(f"https://x.com/{n}", D0, alias=a)
           for _ in range(n):
               s.expand(a, D0)
       return s


   def test_fact_report_order(tmp_path):
       found = [re.search(r"\\b(aaa|bbb|ccc)\\b", x) for x in _rep(tmp_path, _three())]
       assert [m.group(1) for m in found if m] == ["bbb", "ccc", "aaa"]


   def test_fact_report_header(tmp_path):
       assert _rep(tmp_path, _three())[0] == "Links: 3"


   def test_fact_normalize_host():
       assert normalize("https://Example.COM/a/") == "https://example.com/a"
       assert normalize("Example.com/Path/") == "https://example.com/Path"


   def test_fact_stats_day():
       s = Shortener()
       c = s.shorten("https://e.com/a", D0)
       for d in (0, 1, 1):
           s.expand(c, D0 + timedelta(days=d))
       assert s.stats(c, D0 + timedelta(days=1)) == 2 and s.stats(c) == 3


   def test_fact_strip_www():
       assert domain_of("https://www.example.com/a") == "example.com"
       assert domain_of("http://shop.example.com") == "shop.example.com"


   def test_fact_scheme_check():
       with pytest.raises(ValueError):
           normalize("ftp://x.com/a")
       with pytest.raises(ValueError):
           Shortener().shorten("ftp://x.com/a", D0)
       assert normalize("http://x.com") == "http://x.com"


   def test_fact_same_url():
       s = Shortener()
       a = s.shorten("https://e.com/a", D0)
       b = s.shorten("https://e.com/a", D0)
       assert a == b and s.count(D0) == 1


   def test_fact_alias_rules():
       s = Shortener()
       s.shorten("https://e.com/1", D0, alias="docs")
       for bad in ("docs", "ab", "a!b"):
           with pytest.raises(ValueError):
               s.shorten("https://e.com/2", D0, alias=bad)
       assert s.expand("docs", D0) == "https://e.com/1"


   def test_fact_no_confusable():
       s = Shortener()
       codes = [s.shorten(f"https://e.com/{i}", D0) for i in range(200)]
       assert not any(ch in "0O1lI" for c in codes for ch in c)
   ''',
   {"urls.py": '''
    def normalize(url):
        u = url.strip()
        if "://" not in u:
            u = "https://" + u
        scheme, rest = u.split("://", 1)
        scheme = scheme.lower()
        if scheme not in ("http", "https"):
            raise ValueError("only http and https")
        host, _, path = rest.partition("/")
        out = f"{scheme}://{host.lower()}"
        if path:
            out += "/" + path
        return out.rstrip("/")


    def domain_of(url):
        host = normalize(url).split("://", 1)[1].split("/")[0]
        return host[4:] if host.startswith("www.") else host
    ''',
    "store.py": '''
    import random
    import re
    import string
    from urls import domain_of, normalize

    ALPHA = "".join(c for c in string.ascii_letters + string.digits if c not in "0O1lI")


    class Shortener:
        def __init__(self):
            self.links = {}
            self.clicks = {}

        def _new_code(self):
            while True:
                c = "".join(random.choice(ALPHA) for _ in range(7))
                if c not in self.links:
                    return c

        def shorten(self, url, today, alias=None):
            u = normalize(url)
            if alias is None:
                for c, (lu, cr) in self.links.items():
                    if lu == u:
                        return c
                c = self._new_code()
            else:
                if not re.fullmatch(r"[A-Za-z0-9-]{3,20}", alias) or alias in self.links:
                    raise ValueError("bad alias")
                c = alias
            self.links[c] = (u, today)
            self.clicks[c] = []
            return c

        def _live(self, code, today):
            return code in self.links and (today - self.links[code][1]).days < 90

        def expand(self, code, today):
            if not self._live(code, today):
                return None
            self.clicks[code].append(today)
            return self.links[code][0]

        def delete(self, code):
            self.links.pop(code, None)

        def stats(self, code, day=None):
            cl = self.clicks[code]
            return len(cl) if day is None else cl.count(day)

        def count(self, today):
            return sum(1 for c in self.links if self._live(c, today))

        def by_domain(self):
            out = {}
            for u, cr in self.links.values():
                d = domain_of(u)
                out[d] = out.get(d, 0) + 1
            return out
    ''',
    "report.py": '''
    def write_report(s, path):
        codes = sorted(s.links, key=lambda c: (-s.stats(c), c))
        with open(path, "w", encoding="utf8") as f:
            f.write(f"Links: {len(codes)}\\n")
            for c in codes:
                f.write(f"{c} | {s.stats(c)} clicks | {s.links[c][0]}\\n")
    '''})

# ---------------------------------------------------------------- L19 address book
mk("L19", {"first_name": "superseded", "country_49": "superseded", "csv_header": "superseded",
           "phone_marks": "unfinished", "search_email": "unfinished", "initials_hyphen": "unfinished",
           "email_valid": "constraint", "name_title": "constraint", "dup_name": "decision",
           "contact_needs": "decision", "export_empty": "decision", "export_count": "decision"},
   "A small address book.",
   {"phones.py": '"""Phone and email helpers."""\n', "names.py": '"""Name helpers."""\n',
    "book.py": '"""The address book."""\n', "export.py": '"""CSV export."""\n'},
   [f"""
    Add normalize_phone(s) to phones.py: spaces are removed ("+31 6 1234 5678" becomes "+31612345678"). Add tests.

    {later("normalize_phone", 'dashes, dots and brackets are removed too ("+31 (6) 12-34.56" becomes "+316123456").')}

    {RULE}an email address must have exactly one "@", some text before it, and a dot in the text after it: any function given another email raises ValueError.

    {DEC}a phone number that starts with 0 is a local number: normalize_phone replaces the 0 with the default country code +31.
    """,
    f"""
    Add an AddressBook class to book.py: add(name, phone=None, email=None) adds a contact, get(name) returns a dict with the keys name, phone and email (None when missing; the phone is normalized), and names() returns the contact names. Add tests.

    {RULE}names are stored with each word capitalized ("ann van zed" becomes "Ann Van Zed"), in every function.

    {DEC}names() is sorted by last name.

    {DEC}the header line of a CSV export is name,phone,email.
    """,
    f"""
    Add AddressBook.remove(name) to book.py. Add tests.

    {CHG}names() is sorted by first name, not last name.

    {DEC}adding a contact whose name is already in the book raises ValueError; names ignore case in that check.

    {DEC}a contact needs a phone or an email: adding one with neither raises ValueError.
    """,
    f"""
    Add AddressBook.search(text) to book.py: the sorted names that contain text, ignoring case. Add tests.

    {later("AddressBook.search", "it also matches contacts whose email contains text.")}

    {CHG}the default country code for local numbers is +49, not +31.
    """,
    f"""
    Add initials(name) to names.py: the first letter of each word ("Ann Lee" gives "AL"). Add tests.

    {later("initials", 'each part of a hyphenated name counts as a word ("Mary-Jane Lee" gives "MJL").')}
    """,
    f"""
    Add AddressBook.count() to book.py. Add tests.

    {CHG}the header line of a CSV export is name,email,phone, not name,phone,email.

    {DEC}in a CSV export a missing phone or email is an empty field.

    {DEC}the last line of a CSV export is the number of contacts, in the form # 3 contacts.
    """,
    """
    Add AddressBook.update(name, phone=None, email=None) to book.py: it changes the phone and/or email that are given and keeps the rest. Add tests.
    """,
    f"""
    Add write_csv(book, path) to export.py: it writes a CSV export with one row per contact, in names() order. Add tests. {FINISH}
    """],
   [g("Session 1 added normalize_phone(s) with tests. Its last step is left for later: remove dashes, dots and brackets.",
      [("normalize_phone", "done"), ("normalize_phone: remove - . ( )", "todo")],
      ["An email needs exactly one @, text before it and a dot after it; another raises ValueError in any function.",
       "A phone number starting with 0 gets the default country code +31 in place of the 0."]),
    g("Session 2 added AddressBook.add, get and names with tests.", [("AddressBook.add / get / names", "done")],
      ["Names are stored with each word capitalized, in every function.",
       "names() is sorted by last name.",
       "The CSV export header is name,phone,email."]),
    g("Session 3 added AddressBook.remove with tests.", [("AddressBook.remove", "done")],
      ["Supersedes last name: names() is sorted by first name.",
       "Adding a name already in the book raises ValueError (ignoring case).",
       "A contact needs a phone or an email; neither raises ValueError."]),
    g("Session 4 added AddressBook.search(text) with tests. Its last step is left for later: also match emails.",
      [("AddressBook.search", "done"), ("AddressBook.search: match emails", "todo")],
      ["Supersedes +31: the default country code for local numbers is +49."]),
    g("Session 5 added initials(name) with tests. Its last step is left for later: hyphenated parts count as words.",
      [("initials", "done"), ("initials: hyphenated names", "todo")]),
    g("Session 6 added AddressBook.count() with tests.", [("AddressBook.count", "done")],
      ["Supersedes name,phone,email: the CSV export header is name,email,phone.",
       "In a CSV export a missing phone or email is an empty field.",
       "The last CSV export line is # 3 contacts."]),
    g("Session 7 added AddressBook.update with tests.", [("AddressBook.update", "done")])],
   '''
   import csv
   import pytest
   from phones import normalize_phone
   from names import initials
   from book import AddressBook
   from export import write_csv


   def _b():
       b = AddressBook()
       b.add("Cy Abbot", phone="+44 20 7946 0000")
       b.add("Ann Zed", email="ann@zed.org")
       b.add("Bo Lee", phone="+31 6 1111 2222", email="bo@lee.nl")
       return b


   def test_book_basic():
       b = _b()
       g = b.get("Bo Lee")
       assert g["name"] == "Bo Lee" and g["phone"] == "+31611112222" and g["email"] == "bo@lee.nl"
       assert b.get("Ann Zed")["phone"] is None
       b.update("Bo Lee", email="bo@new.nl")
       assert b.get("Bo Lee")["email"] == "bo@new.nl" and b.get("Bo Lee")["phone"] == "+31611112222"
       assert b.count() == 3 and b.search("lee") == ["Bo Lee"] and initials("Ann Zed") == "AZ"
       b.remove("Cy Abbot")
       assert b.count() == 2 and normalize_phone("+31 6 12") == "+31612"


   def test_fact_first_name():
       assert _b().names() == ["Ann Zed", "Bo Lee", "Cy Abbot"]


   def test_stale_last_name():
       assert _b().names() == ["Cy Abbot", "Bo Lee", "Ann Zed"]


   def test_fact_country_49():
       assert normalize_phone("0612345678") == "+49612345678"


   def test_stale_country_31():
       assert normalize_phone("0612345678") == "+31612345678"


   def _csv(tmp_path):
       p = tmp_path / "c.csv"
       write_csv(_b(), str(p))
       return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def test_fact_csv_header(tmp_path):
       assert _csv(tmp_path)[0] == "name,email,phone"


   def test_stale_csv_header(tmp_path):
       assert _csv(tmp_path)[0] == "name,phone,email"


   def test_fact_export_empty(tmp_path):
       rows = [r for r in csv.DictReader(_csv(tmp_path)) if not r["name"].startswith("#")]
       ann = next(r for r in rows if r["name"] == "Ann Zed")
       assert ann["phone"] == "" and ann["email"] == "ann@zed.org"


   def test_fact_export_count(tmp_path):
       assert _csv(tmp_path)[-1] == "# 3 contacts"


   def test_fact_phone_marks():
       assert normalize_phone("+31 (6) 12-34.56") == "+316123456"


   def test_fact_search_email():
       b = _b()
       assert b.search("zed.org") == ["Ann Zed"] and b.search("abbot") == ["Cy Abbot"]


   def test_fact_initials_hyphen():
       assert initials("Mary-Jane Lee") == "MJL" and initials("Ann Zed") == "AZ"


   def test_fact_email_valid():
       b = AddressBook()
       for bad in ("ann", "ann@@x.org", "@x.org", "ann@xorg"):
           with pytest.raises(ValueError):
               b.add("Ann Zed", email=bad)
       assert b.count() == 0
       b.add("Ann Zed", email="ann@zed.org")
       with pytest.raises(ValueError):
           b.update("Ann Zed", email="nope")
       assert b.get("Ann Zed")["email"] == "ann@zed.org"


   def test_fact_name_title():
       b = AddressBook()
       b.add("ann van zed", email="a@b.nl")
       assert b.names() == ["Ann Van Zed"]


   def test_fact_dup_name():
       b = AddressBook()
       b.add("Ann Zed", email="ann@zed.org")
       with pytest.raises(ValueError):
           b.add("ann zed", phone="+3161")
       assert b.count() == 1


   def test_fact_contact_needs():
       b = AddressBook()
       with pytest.raises(ValueError):
           b.add("Ann Zed")
       assert b.count() == 0
   ''',
   {"phones.py": '''
    import re


    def normalize_phone(s):
        p = re.sub(r"[\\s().-]", "", s)
        if p.startswith("0"):
            p = "+49" + p[1:]
        return p


    def check_email(e):
        if e is None:
            return None
        if e.count("@") != 1:
            raise ValueError("bad email")
        user, dom = e.split("@")
        if not user or "." not in dom:
            raise ValueError("bad email")
        return e
    ''',
    "names.py": '''
    import re


    def title_name(name):
        return " ".join("-".join(p.capitalize() for p in w.split("-")) for w in name.split())


    def initials(name):
        return "".join(p[0].upper() for p in re.split(r"[\\s-]+", name.strip()) if p)
    ''',
    "book.py": '''
    from phones import check_email, normalize_phone
    from names import title_name


    class AddressBook:
        def __init__(self):
            self.c = {}

        def add(self, name, phone=None, email=None):
            n = title_name(name)
            if not n:
                raise ValueError("name required")
            if any(k.lower() == n.lower() for k in self.c):
                raise ValueError("duplicate name")
            if phone is None and email is None:
                raise ValueError("phone or email required")
            check_email(email)
            self.c[n] = {"name": n, "phone": normalize_phone(phone) if phone else None, "email": email}

        def get(self, name):
            return dict(self.c[title_name(name)])

        def names(self):
            return sorted(self.c)

        def remove(self, name):
            del self.c[title_name(name)]

        def search(self, text):
            t = text.lower()
            return sorted(n for n, v in self.c.items()
                          if t in n.lower() or (v["email"] and t in v["email"].lower()))

        def count(self):
            return len(self.c)

        def update(self, name, phone=None, email=None):
            v = self.c[title_name(name)]
            if email is not None:
                check_email(email)
                v["email"] = email
            if phone is not None:
                v["phone"] = normalize_phone(phone)
    ''',
    "export.py": '''
    import csv


    def write_csv(book, path):
        with open(path, "w", encoding="utf8", newline="") as f:
            w = csv.writer(f, lineterminator="\\n")
            w.writerow(["name", "email", "phone"])
            for n in book.names():
                v = book.get(n)
                w.writerow([n, v["email"] or "", v["phone"] or ""])
            f.write(f"# {book.count()} contacts\\n")
    '''})

# ---------------------------------------------------------------- L20 log analyser
mk("L20", {"slow_300": "superseded", "errors_400": "superseded", "report_line": "superseded",
           "seconds": "unfinished", "query_strip": "unfinished", "hour_fill": "unfinished",
           "bad_lines": "constraint", "method_upper": "constraint", "health_ignored": "decision",
           "error_round": "decision", "report_order": "decision", "report_header": "decision"},
   "A small web server log analyser.",
   {"parse.py": '"""Log parsing."""\n', "stats.py": '"""Log statistics."""\n',
    "report.py": '"""Log reports."""\n'},
   [f"""
    Add parse_line(line) to parse.py. A log line looks like 2026-06-01 12:00:05 INFO GET /home 200 35ms (date, time, level, method, path, status, duration). parse_line returns a dict with the keys date, time, hour, level, method, path, status (int) and ms (int). Add tests.

    {later("parse_line", 'the duration may also be in seconds ("1.2s" is 1200 ms).')}

    {RULE}parse_line raises ValueError for a malformed line, and any function that takes many lines skips the malformed ones.

    {DEC}a slow request is one that takes more than 500 ms.
    """,
    f"""
    Add parse_lines(lines) to parse.py: the records of all lines. Add count_levels(records) to stats.py: a dict from level to number of records. Add tests.

    {RULE}methods ignore case and are stored in upper case ("get" becomes "GET").

    {DEC}an error is a request with status 500 or above.

    {DEC}each path line of a report has the form /home 12.
    """,
    f"""
    Add error_rate(records) to stats.py: the percent of requests that are errors. Add tests.

    {CHG}an error is a request with status 400 or above, not 500.

    {DEC}requests to /health are ignored by every statistic and by the report.

    {DEC}error_rate is rounded to one decimal (1 error in 3 requests is 33.3).
    """,
    f"""
    Add top_paths(records, n) to stats.py: the n most requested paths as (path, count) pairs, most first. Add tests.

    {later("top_paths", 'a query string is removed before counting ("/a?x=1" counts as "/a").')}

    {CHG}a slow request is one that takes more than 300 ms, not 500.
    """,
    f"""
    Add by_hour(records) to stats.py: a dict from hour (int) to number of requests. Add tests.

    {later("by_hour", "every hour between the first and the last hour with requests is included, with 0 when it has none.")}
    """,
    f"""
    Add slow_requests(records) to stats.py: the slow requests, in log order. Add tests.

    {CHG}each path line of a report has the form /home: 12 requests, not /home 12.

    {DEC}a report lists the paths by count, most first.

    {DEC}the first line of a report is the date of the first record, in the form Log report 2026-06-01.
    """,
    """
    Add summary(records) to stats.py: a dict with the keys requests, errors and slow (counts). Add tests.
    """,
    f"""
    Add write_report(lines, path) to report.py: it reads log lines and writes a text report with one line per path. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_line(line) with tests. Its last step is left for later: durations in seconds.",
      [("parse_line", "done"), ("parse_line: durations in seconds", "todo")],
      ["parse_line raises ValueError for a malformed line; functions that take many lines skip malformed ones.",
       "A slow request takes more than 500 ms."]),
    g("Session 2 added parse_lines and count_levels with tests.", [("parse_lines / count_levels", "done")],
      ["Methods ignore case and are stored upper case.",
       "An error is a request with status 500 or above.",
       "A report path line has the form /home 12."]),
    g("Session 3 added error_rate(records) with tests.", [("error_rate", "done")],
      ["Supersedes 500: an error is a request with status 400 or above.",
       "Requests to /health are ignored by every statistic and by the report.",
       "error_rate is rounded to one decimal."]),
    g("Session 4 added top_paths(records, n) with tests. Its last step is left for later: strip query strings.",
      [("top_paths", "done"), ("top_paths: strip query strings", "todo")],
      ["Supersedes 500 ms: a slow request takes more than 300 ms."]),
    g("Session 5 added by_hour(records) with tests. Its last step is left for later: include empty hours between first and last with 0.",
      [("by_hour", "done"), ("by_hour: fill empty hours", "todo")]),
    g("Session 6 added slow_requests(records) with tests.", [("slow_requests", "done")],
      ["Supersedes /home 12: a report path line has the form /home: 12 requests.",
       "A report lists paths by count, most first.",
       "The first report line is Log report 2026-06-01."]),
    g("Session 7 added summary(records) with tests.", [("summary", "done")])],
   '''
   import re
   import pytest
   from parse import parse_line, parse_lines
   from stats import by_hour, count_levels, error_rate, slow_requests, summary, top_paths
   from report import write_report


   def _line(t="12:00:05", level="INFO", method="GET", path="/home", status=200, ms="35ms"):
       return f"2026-06-01 {t} {level} {method} {path} {status} {ms}"


   def test_log_basic():
       r = parse_lines([_line(), _line(path="/about", status=404, ms="20ms"), "garbage"])
       assert len(r) == 2 and r[0]["path"] == "/home" and r[0]["status"] == 200 and r[0]["ms"] == 35
       assert count_levels(r) == {"INFO": 2} and top_paths(r, 1)[0][1] == 1
       assert by_hour(r) == {12: 2} and summary(r)["requests"] == 2


   def test_fact_slow_300():
       r = parse_lines([_line(ms="400ms"), _line(ms="200ms"), _line(ms="600ms")])
       assert [x["ms"] for x in slow_requests(r)] == [400, 600]


   def test_stale_slow_500():
       r = parse_lines([_line(ms="400ms"), _line(ms="200ms"), _line(ms="600ms")])
       assert [x["ms"] for x in slow_requests(r)] == [600]


   def _errs():
       return parse_lines([_line(status=s) for s in (200, 404, 500, 200)])


   def test_fact_errors_400():
       assert error_rate(_errs()) == 50.0


   def test_stale_errors_500():
       assert error_rate(_errs()) == 25.0


   def _rep(tmp_path, paths):
       p = tmp_path / "r.txt"
       write_report([_line(path=x) for x in paths], str(p))
       return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def test_fact_report_line(tmp_path):
       assert "/home: 2 requests" in _rep(tmp_path, ["/home", "/about", "/home"])


   def test_stale_report_plain(tmp_path):
       assert "/home 2" in _rep(tmp_path, ["/home", "/about", "/home"])


   def test_fact_report_order(tmp_path):
       found = [re.match(r"(/[abc])\\b", x) for x in _rep(tmp_path, ["/a", "/b", "/c", "/b", "/c", "/b"])]
       assert [m.group(1) for m in found if m] == ["/b", "/c", "/a"]


   def test_fact_report_header(tmp_path):
       assert _rep(tmp_path, ["/home"])[0] == "Log report 2026-06-01"


   def test_fact_seconds():
       assert parse_line(_line(ms="1.2s"))["ms"] == 1200 and parse_line(_line(ms="35ms"))["ms"] == 35


   def test_fact_query_strip():
       r = parse_lines([_line(path="/a?x=1"), _line(path="/a?y=2"), _line(path="/b")])
       assert top_paths(r, 1) == [("/a", 2)]


   def test_fact_hour_fill():
       r = parse_lines([_line(t="09:10:00"), _line(t="12:00:00"), _line(t="12:30:00")])
       assert by_hour(r) == {9: 1, 10: 0, 11: 0, 12: 2}


   def test_fact_bad_lines():
       with pytest.raises(ValueError):
           parse_line("nonsense")
       with pytest.raises(ValueError):
           parse_line(_line(status="abc"))
       assert len(parse_lines(["x", _line()])) == 1


   def test_fact_method_upper():
       assert parse_line(_line(method="get"))["method"] == "GET"


   def test_fact_health_ignored():
       r = parse_lines([_line(path="/health", status=500), _line(), _line(path="/health")])
       assert error_rate(r) == 0.0 and top_paths(r, 5) == [("/home", 1)]


   def test_fact_error_round():
       assert error_rate(parse_lines([_line(status=s) for s in (404, 200, 200)])) == 33.3
   ''',
   {"parse.py": '''
    import re

    PAT = re.compile(r"(\\d{4}-\\d\\d-\\d\\d) (\\d\\d):(\\d\\d):(\\d\\d) (\\w+) (\\w+) (\\S+) (\\d{3}) (\\d+(?:\\.\\d+)?)(ms|s)")


    def parse_line(line):
        m = PAT.fullmatch(line.strip())
        if not m:
            raise ValueError("malformed line")
        d, h, mi, s, level, method, path, status, num, unit = m.groups()
        return {"date": d, "time": f"{h}:{mi}:{s}", "hour": int(h), "level": level,
                "method": method.upper(), "path": path, "status": int(status),
                "ms": int(round(float(num) * (1000 if unit == "s" else 1)))}


    def parse_lines(lines):
        out = []
        for l in lines:
            try:
                out.append(parse_line(l))
            except ValueError:
                pass
        return out
    ''',
    "stats.py": '''
    def _path(r):
        return r["path"].split("?")[0]


    def _live(records):
        return [r for r in records if _path(r) != "/health"]


    def count_levels(records):
        out = {}
        for r in _live(records):
            out[r["level"]] = out.get(r["level"], 0) + 1
        return out


    def error_rate(records):
        r = _live(records)
        if not r:
            return 0.0
        return round(sum(x["status"] >= 400 for x in r) * 100 / len(r), 1)


    def top_paths(records, n):
        c = {}
        for r in _live(records):
            c[_path(r)] = c.get(_path(r), 0) + 1
        return sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


    def by_hour(records):
        hours = [r["hour"] for r in _live(records)]
        if not hours:
            return {}
        return {h: hours.count(h) for h in range(min(hours), max(hours) + 1)}


    def slow_requests(records):
        return [r for r in _live(records) if r["ms"] > 300]


    def summary(records):
        r = _live(records)
        return {"requests": len(r), "errors": sum(x["status"] >= 400 for x in r),
                "slow": len(slow_requests(records))}
    ''',
    "report.py": '''
    from parse import parse_lines
    from stats import top_paths


    def write_report(lines, path):
        recs = parse_lines(lines)
        with open(path, "w", encoding="utf8") as f:
            if recs:
                f.write(f"Log report {recs[0]['date']}\\n")
            for p, c in top_paths(recs, len(recs)):
                f.write(f"{p}: {c} requests\\n")
    '''})
