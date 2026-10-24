"""R-014 scored projects L12-L14 (v3 form: 8 sessions, 12 facts)."""
from long_common import CHG, DEC, FINISH, RULE, g, later, mk

# ---------------------------------------------------------------- L12 bank ledger
mk("L12", {"no_overdraft": "superseded", "fee_25": "superseded", "closing_line": "superseded",
           "parse_dollar": "unfinished", "history_last": "unfinished", "money_commas": "unfinished",
           "positive_amount": "constraint", "name_case": "constraint", "dup_open": "decision",
           "transfer_self": "decision", "interest_tier": "decision", "statement_header": "decision"},
   "A small bank ledger. Amounts are int cents.",
   {"money.py": '"""Money parsing."""\n', "ledger.py": '"""Ledger."""\n',
    "interest.py": '"""Interest."""\n', "statement.py": '"""Statements."""\n'},
   [f"""
    Add parse_amount(s) to money.py: an amount string such as "12.50" becomes int cents (1250). Add tests.

    {later("parse_amount", 'it also accepts a leading "$" and thousands commas ("$1,234.50" becomes 123450).')}

    {RULE}an amount must be positive: any function given an amount of zero or less raises ValueError and changes nothing.

    {DEC}an account may be overdrawn: its balance may go down to -5000 cents.
    """,
    f"""
    Add a Ledger class to ledger.py with open(account), deposit(account, cents), withdraw(account, cents) and balance(account). Add tests.

    {RULE}account names ignore case: "Ann" and "ANN" are the same account, in every function.

    {DEC}each withdrawal costs a fee of 100 cents, taken from the balance.

    {DEC}the last line of a statement is the balance in the form BALANCE: 12.50.
    """,
    f"""
    Add Ledger.transfer(src, dst, cents) to ledger.py: it moves cents from one account to another. Transfers have no fee. Add tests.

    {CHG}the withdrawal fee is 25 cents, not 100.

    {DEC}opening an account that already exists raises ValueError.

    {DEC}a transfer from an account to itself raises ValueError.
    """,
    f"""
    Add Ledger.history(account) to ledger.py: the account's balance changes in order, as signed cents (a deposit of 500 is 500, a withdrawal of 200 is -200, and a fee is its own entry). Add tests.

    {later("Ledger.history", "it takes an optional n and then returns only the last n entries.")}

    {CHG}no account may be overdrawn: a withdrawal (with its fee) or a transfer that would take a balance below 0 raises ValueError and changes nothing.
    """,
    f"""
    Add fmt_money(cents) to statement.py: 123450 becomes "1234.50". Add tests.

    {later("fmt_money", 'thousands are separated by commas ("1,234.50").')}
    """,
    f"""
    Add Ledger.accounts() to ledger.py: the sorted list of account names, in lower case. Add tests.

    {CHG}the last line of a statement has the form Closing balance: $12.50, not BALANCE: 12.50.

    {DEC}monthly interest is 1% of the balance up to 100000 cents plus 2% of the part above, rounded down to a whole cent.

    {DEC}the first line of a statement is the account name in upper case, in the form ACCOUNT ANN.
    """,
    """
    Add monthly_interest(balance) to interest.py: the interest in cents (an int) for one month on that balance. Add tests.
    """,
    f"""
    Add write_statement(ledger, account, path) to statement.py: it writes a text statement with one line per history entry and the balance. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_amount(s) with tests. Its last step is left for later: accept a leading \"$\" and thousands commas.",
      [("parse_amount", "done"), ("parse_amount: accept $ and commas", "todo")],
      ["An amount must be positive: zero or less raises ValueError and changes nothing, in any function.",
       "An account may be overdrawn down to -5000 cents."]),
    g("Session 2 added Ledger.open, deposit, withdraw and balance with tests.", [("Ledger.open / deposit / withdraw / balance", "done")],
      ["Account names ignore case in every function.",
       "Each withdrawal costs a fee of 100 cents, taken from the balance.",
       "The last statement line is the balance: BALANCE: 12.50."]),
    g("Session 3 added Ledger.transfer with tests.", [("Ledger.transfer", "done")],
      ["Supersedes 100 cents: the withdrawal fee is 25 cents.",
       "Opening an account that already exists raises ValueError.",
       "A transfer from an account to itself raises ValueError."]),
    g("Session 4 added Ledger.history(account) with tests. Its last step is left for later: an optional n returns only the last n entries.",
      [("Ledger.history", "done"), ("Ledger.history: optional last n", "todo")],
      ["Supersedes the -5000 overdraft: a withdrawal (with fee) or transfer taking a balance below 0 raises ValueError and changes nothing."]),
    g("Session 5 added fmt_money(cents) with tests. Its last step is left for later: thousands commas.",
      [("fmt_money", "done"), ("fmt_money: thousands commas", "todo")]),
    g("Session 6 added Ledger.accounts() with tests.", [("Ledger.accounts", "done")],
      ["Supersedes BALANCE: 12.50: the last statement line is Closing balance: $12.50.",
       "Monthly interest is 1% up to 100000 cents plus 2% of the part above, rounded down.",
       "The first statement line is the account name in upper case: ACCOUNT ANN."]),
    g("Session 7 added monthly_interest(balance) with tests.", [("monthly_interest", "done")])],
   '''
   import re
   import pytest
   from money import parse_amount
   from ledger import Ledger
   from interest import monthly_interest
   from statement import fmt_money, write_statement


   def _l(*accts):
       l = Ledger()
       for a in accts:
           l.open(a)
       return l


   def test_ledger_basic():
       l = _l("ann", "bo")
       l.deposit("ann", 5000)
       l.transfer("ann", "bo", 1000)
       assert l.balance("ann") == 4000 and l.balance("bo") == 1000 and l.history("bo") == [1000]
       assert l.accounts() == ["ann", "bo"]
       assert parse_amount("12.50") == 1250 and fmt_money(1250) == "12.50" and monthly_interest(10000) == 100


   def test_fact_no_overdraft():
       l = _l("ann")
       l.deposit("ann", 1000)
       with pytest.raises(ValueError):
           l.withdraw("ann", 3000)
       assert l.balance("ann") == 1000


   def test_stale_overdraft():
       l = _l("ann")
       l.deposit("ann", 1000)
       l.withdraw("ann", 3000)
       assert l.balance("ann") < 0


   def test_fact_fee_25():
       l = _l("ann")
       l.deposit("ann", 10000)
       l.withdraw("ann", 1000)
       assert l.balance("ann") == 8975


   def test_stale_fee_100():
       l = _l("ann")
       l.deposit("ann", 10000)
       l.withdraw("ann", 1000)
       assert l.balance("ann") == 8900


   def _stmt(tmp_path):
       l = _l("ann")
       l.deposit("ann", 2000)
       l.withdraw("ann", 500)
       p = tmp_path / "s.txt"
       write_statement(l, "ann", str(p))
       return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def test_fact_closing_line(tmp_path):
       assert re.fullmatch(r"Closing balance: \\$[\\d,]+\\.\\d\\d", _stmt(tmp_path)[-1])


   def test_stale_balance_upper(tmp_path):
       assert re.fullmatch(r"BALANCE: \\$?[\\d,]+\\.\\d\\d", _stmt(tmp_path)[-1])


   def test_fact_statement_header(tmp_path):
       assert _stmt(tmp_path)[0] == "ACCOUNT ANN"


   def test_fact_parse_dollar():
       assert parse_amount("$1,234.50") == 123450 and parse_amount("12.50") == 1250


   def test_fact_history_last():
       l = _l("ann")
       for c in (1000, 2000, 3000):
           l.deposit("ann", c)
       assert l.history("ann", 2) == [2000, 3000] and l.history("ann") == [1000, 2000, 3000]


   def test_fact_money_commas():
       assert fmt_money(123450) == "1,234.50" and fmt_money(5) == "0.05"


   def test_fact_positive_amount():
       l = _l("ann", "bo")
       l.deposit("ann", 1000)
       with pytest.raises(ValueError):
           l.deposit("ann", 0)
       with pytest.raises(ValueError):
           l.withdraw("ann", -5)
       with pytest.raises(ValueError):
           l.transfer("ann", "bo", 0)
       assert l.balance("ann") == 1000 and l.balance("bo") == 0


   def test_fact_name_case():
       l = _l("Ann")
       l.deposit("ANN", 500)
       assert l.balance("ann") == 500


   def test_fact_dup_open():
       l = _l("ann")
       l.deposit("ann", 500)
       with pytest.raises(ValueError):
           l.open("ann")
       assert l.balance("ann") == 500


   def test_fact_transfer_self():
       l = _l("ann")
       l.deposit("ann", 500)
       with pytest.raises(ValueError):
           l.transfer("ann", "ann", 100)
       assert l.balance("ann") == 500


   def test_fact_interest_tier():
       assert monthly_interest(150000) == 2000 and monthly_interest(50000) == 500 and monthly_interest(12345) == 123
   ''',
   {"money.py": '''
    from decimal import Decimal


    def parse_amount(s):
        v = int(Decimal(s.strip().replace("$", "").replace(",", "")) * 100)
        if v <= 0:
            raise ValueError("amount must be positive")
        return v
    ''',
    "ledger.py": '''
    class Ledger:
        def __init__(self):
            self.bal = {}
            self.hist = {}

        def open(self, account):
            a = account.lower()
            if a in self.bal:
                raise ValueError("account exists")
            self.bal[a] = 0
            self.hist[a] = []

        def _chg(self, a, c):
            self.bal[a] += c
            self.hist[a].append(c)

        def deposit(self, account, cents):
            if cents <= 0:
                raise ValueError("amount must be positive")
            self._chg(account.lower(), cents)

        def withdraw(self, account, cents):
            if cents <= 0:
                raise ValueError("amount must be positive")
            a = account.lower()
            if self.bal[a] - cents - 25 < 0:
                raise ValueError("no overdraft")
            self._chg(a, -cents)
            self._chg(a, -25)

        def balance(self, account):
            return self.bal[account.lower()]

        def transfer(self, src, dst, cents):
            if cents <= 0:
                raise ValueError("amount must be positive")
            a, b = src.lower(), dst.lower()
            if a == b:
                raise ValueError("same account")
            if self.bal[a] - cents < 0:
                raise ValueError("no overdraft")
            self._chg(a, -cents)
            self._chg(b, cents)

        def history(self, account, n=None):
            h = list(self.hist[account.lower()])
            return h[-n:] if n else h

        def accounts(self):
            return sorted(self.bal)
    ''',
    "interest.py": '''
    def monthly_interest(balance):
        return min(balance, 100000) // 100 + max(0, balance - 100000) * 2 // 100
    ''',
    "statement.py": '''
    def fmt_money(cents):
        return f"{cents // 100:,}.{cents % 100:02d}"


    def write_statement(ledger, account, path):
        with open(path, "w", encoding="utf8") as f:
            f.write(f"ACCOUNT {account.upper()}\\n")
            for c in ledger.history(account):
                f.write(f"{'+' if c > 0 else '-'}{fmt_money(abs(c))}\\n")
            f.write(f"Closing balance: ${fmt_money(ledger.balance(account))}\\n")
    '''})

# ---------------------------------------------------------------- L13 kanban board
mk("L13", {"wip_2": "superseded", "backlog_start": "superseded", "export_line": "superseded",
           "tags_clean": "unfinished", "find_case": "unfinished", "weekdays": "unfinished",
           "title_required": "constraint", "unknown_column": "constraint", "done_locked": "decision",
           "same_column": "decision", "export_order": "decision", "count_open": "decision"},
   "A small kanban board.",
   {"cards.py": '"""Card helpers."""\n', "board.py": '"""The board."""\n',
    "search.py": '"""Card search."""\n', "export.py": '"""Board export."""\n'},
   [f"""
    Add parse_tags(s) to cards.py: a comma-separated tag string becomes a list of tags with spaces removed ("bug, ui" becomes ["bug", "ui"]). Add tests.

    {later("parse_tags", 'tags are lower case and duplicates are removed, keeping the first-seen order ("Bug, ui, BUG" becomes ["bug", "ui"]).')}

    {RULE}card titles are stored with leading and trailing spaces removed, and an empty or blank title raises ValueError in any function.

    {DEC}the "doing" column holds at most 3 cards; moving a card into a full "doing" column raises ValueError.
    """,
    f"""
    Add a Board class to board.py: add(title) adds a card and returns its id (1, 2, 3 and so on), move(card_id, column) moves a card, column(name) returns the ids in that column in the order they entered it, and title(card_id) returns the title. The columns are "todo", "doing" and "done". Add tests.

    {RULE}moving a card to a column the board does not have raises ValueError and changes nothing.

    {DEC}a new card starts in the "todo" column.

    {DEC}each line of a board export has the form [todo] Fix bug (the column in brackets, then the title).
    """,
    f"""
    Add Board.rename(card_id, title) to board.py. Add tests.

    {CHG}a new card starts in a "backlog" column, not "todo"; the columns are now "backlog", "todo", "doing" and "done".

    {DEC}a card in "done" cannot move to another column: move raises ValueError.

    {DEC}moving a card to the column it is already in does nothing and keeps its place in that column.
    """,
    f"""
    Add find(board, text) to search.py: the ids, in ascending order, of the cards whose title contains text. Add tests.

    {later("find", "the match ignores case.")}

    {CHG}the "doing" column holds at most 2 cards, not 3.
    """,
    f"""
    Add days_left(due, today) to cards.py: the number of days from today until the due date (both datetime.date). Add tests.

    {later("days_left", "only Monday to Friday count: from a Friday to the next Monday is 1 day.")}
    """,
    f"""
    Add Board.count() to board.py. Add tests.

    {CHG}each line of a board export has the form Fix bug (todo) (the title, then the column in brackets), not [todo] Fix bug.

    {DEC}Board.count() counts only open cards: cards in "done" are not counted.

    {DEC}a board export lists the cards by column, in board column order, and by card id within a column.
    """,
    """
    Add tags to cards: Board.tag(card_id, s) stores the tags from parse_tags(s) for that card, and Board.tags(card_id) returns them. Add tests.
    """,
    f"""
    Add write_export(board, path) to export.py: it writes a text export of the board with one line per card. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_tags(s) with tests. Its last step is left for later: lower case and remove duplicates, first-seen order.",
      [("parse_tags", "done"), ("parse_tags: lower case, no duplicates", "todo")],
      ["Card titles are stored without outer spaces; an empty or blank title raises ValueError in any function.",
       "The \"doing\" column holds at most 3 cards; moving into a full one raises ValueError."]),
    g("Session 2 added Board.add, move, column and title with tests. Columns are \"todo\", \"doing\", \"done\".",
      [("Board.add / move / column / title", "done")],
      ["Moving a card to a column the board does not have raises ValueError and changes nothing.",
       "A new card starts in the \"todo\" column.",
       "A board export line has the form [todo] Fix bug."]),
    g("Session 3 added Board.rename with tests.", [("Board.rename", "done")],
      ["Supersedes \"todo\": a new card starts in a \"backlog\" column; columns are backlog, todo, doing, done.",
       "A card in \"done\" cannot move to another column: move raises ValueError.",
       "Moving a card to the column it is already in does nothing and keeps its place."]),
    g("Session 4 added find(board, text) with tests. Its last step is left for later: the match ignores case.",
      [("find", "done"), ("find: ignore case", "todo")],
      ["Supersedes 3: the \"doing\" column holds at most 2 cards."]),
    g("Session 5 added days_left(due, today) with tests. Its last step is left for later: only Monday to Friday count.",
      [("days_left", "done"), ("days_left: weekdays only", "todo")]),
    g("Session 6 added Board.count() with tests.", [("Board.count", "done")],
      ["Supersedes [todo] Fix bug: a board export line has the form Fix bug (todo).",
       "Board.count() counts only open cards, not cards in \"done\".",
       "A board export lists cards by column in board order, then by card id."]),
    g("Session 7 added Board.tag and Board.tags with tests.", [("Board.tag / Board.tags", "done")])],
   '''
   import re
   from datetime import date
   import pytest
   from cards import days_left, parse_tags
   from board import Board
   from search import find
   from export import write_export


   def _board(*titles):
       b = Board()
       for t in titles:
           b.add(t)
       return b


   def test_board_basic():
       b = _board("Fix bug", "Docs")
       b.move(1, "doing")
       b.rename(2, "Write docs")
       b.tag(1, "bug, ui")
       assert b.column("doing") == [1] and b.title(2) == "Write docs" and b.tags(1) == ["bug", "ui"]
       assert find(b, "docs") == [2] and parse_tags("bug, ui") == ["bug", "ui"]
       assert days_left(date(2026, 6, 10), date(2026, 6, 8)) == 2


   def test_fact_wip_2():
       b = _board("a", "b", "c")
       b.move(1, "doing")
       b.move(2, "doing")
       with pytest.raises(ValueError):
           b.move(3, "doing")
       assert b.column("doing") == [1, 2]


   def test_stale_wip_3():
       b = _board("a", "b", "c")
       for i in (1, 2, 3):
           b.move(i, "doing")
       assert b.column("doing") == [1, 2, 3]


   def test_fact_backlog_start():
       b = _board("a")
       assert b.column("backlog") == [1] and b.column("todo") == []


   def test_stale_todo_start():
       assert _board("a").column("todo") == [1]


   def _export(tmp_path, b):
       p = tmp_path / "e.txt"
       write_export(b, str(p))
       return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def test_fact_export_line(tmp_path):
       b = _board("Fix bug")
       b.move(1, "doing")
       assert "Fix bug (doing)" in _export(tmp_path, b)


   def test_stale_export_brackets_first(tmp_path):
       b = _board("Fix bug")
       b.move(1, "doing")
       assert "[doing] Fix bug" in _export(tmp_path, b)


   def test_fact_export_order(tmp_path):
       b = _board("Alpha", "Beta", "Gamma", "Delta")
       b.move(1, "done")
       b.move(4, "todo")
       b.move(2, "todo")
       b.move(3, "doing")
       names = [re.search(r"Alpha|Beta|Gamma|Delta", x).group() for x in _export(tmp_path, b)
                if re.search(r"Alpha|Beta|Gamma|Delta", x)]
       assert names == ["Beta", "Delta", "Gamma", "Alpha"]


   def test_fact_tags_clean():
       assert parse_tags("Bug, ui, BUG") == ["bug", "ui"]


   def test_fact_find_case():
       b = _board("Fix bug", "Bug report", "Docs")
       assert find(b, "BUG") == [1, 2]


   def test_fact_weekdays():
       assert days_left(date(2026, 6, 8), date(2026, 6, 5)) == 1
       assert days_left(date(2026, 6, 15), date(2026, 6, 8)) == 5


   def test_fact_title_required():
       b = _board(" Fix ")
       assert b.title(1) == "Fix"
       with pytest.raises(ValueError):
           b.add("   ")
       with pytest.raises(ValueError):
           b.rename(1, "")
       assert b.title(1) == "Fix"


   def test_fact_unknown_column():
       b = _board("a")
       b.move(1, "todo")
       with pytest.raises(ValueError):
           b.move(1, "later")
       assert b.column("todo") == [1]


   def test_fact_done_locked():
       b = _board("a")
       b.move(1, "done")
       with pytest.raises(ValueError):
           b.move(1, "todo")
       assert b.column("done") == [1]


   def test_fact_same_column():
       b = _board("a", "b", "c")
       for i in (1, 2, 3):
           b.move(i, "todo")
       b.move(1, "todo")
       assert b.column("todo") == [1, 2, 3]


   def test_fact_count_open():
       b = _board("a", "b", "c")
       b.move(2, "done")
       assert b.count() == 2
   ''',
   {"cards.py": '''
    from datetime import timedelta


    def parse_tags(s):
        out = []
        for t in s.split(","):
            t = t.strip().lower()
            if t and t not in out:
                out.append(t)
        return out


    def days_left(due, today):
        n = 0
        d = today
        while d < due:
            d += timedelta(days=1)
            if d.weekday() < 5:
                n += 1
        return n
    ''',
    "board.py": '''
    from cards import parse_tags

    COLS = ["backlog", "todo", "doing", "done"]


    class Board:
        def __init__(self):
            self.cols = {c: [] for c in COLS}
            self.titles = {}
            self._tags = {}
            self.n = 0

        @staticmethod
        def _clean(title):
            t = title.strip()
            if not t:
                raise ValueError("title required")
            return t

        def add(self, title):
            t = self._clean(title)
            self.n += 1
            self.titles[self.n] = t
            self.cols["backlog"].append(self.n)
            return self.n

        def where(self, cid):
            return next(c for c in COLS if cid in self.cols[c])

        def move(self, cid, column):
            if column not in self.cols:
                raise ValueError("unknown column")
            cur = self.where(cid)
            if cur == column:
                return
            if cur == "done":
                raise ValueError("card is done")
            if column == "doing" and len(self.cols["doing"]) >= 2:
                raise ValueError("doing is full")
            self.cols[cur].remove(cid)
            self.cols[column].append(cid)

        def column(self, name):
            return list(self.cols[name])

        def title(self, cid):
            return self.titles[cid]

        def rename(self, cid, title):
            self.titles[cid] = self._clean(title)

        def count(self):
            return sum(len(self.cols[c]) for c in COLS if c != "done")

        def tag(self, cid, s):
            self._tags[cid] = parse_tags(s)

        def tags(self, cid):
            return list(self._tags.get(cid, []))
    ''',
    "search.py": '''
    def find(board, text):
        t = text.lower()
        return sorted(i for i, title in board.titles.items() if t in title.lower())
    ''',
    "export.py": '''
    from board import COLS


    def write_export(board, path):
        with open(path, "w", encoding="utf8") as f:
            for c in COLS:
                for i in sorted(board.column(c)):
                    f.write(f"{board.title(i)} ({c})\\n")
    '''})

# ---------------------------------------------------------------- L14 shipping cost
mk("L14", {"vol_4000": "superseded", "per_kg_150": "superseded", "weight_kg": "superseded",
           "parse_units": "unfinished", "split_equal": "unfinished", "check_digit": "unfinished",
           "weight_range": "constraint", "country_code": "constraint", "charged_max": "decision",
           "blocked": "decision", "world_double": "decision", "label_code": "decision"},
   "Shipping cost helpers for a small web shop. Weights are int grams, prices int cents.",
   {"parcels.py": '"""Parcels."""\n', "zones.py": '"""Shipping zones."""\n',
    "rates.py": '"""Shipping rates."""\n', "label.py": '"""Shipping labels."""\n'},
   [f"""
    Add parse_weight(s) to parcels.py: a weight in kilograms such as "1.5kg" becomes int grams (1500). Add tests.

    {later("parse_weight", 'it also accepts grams ("750g" becomes 750) and pounds ("2lb" becomes 908; 1 lb is 454 g).')}

    {RULE}a parcel weighs more than 0 and at most 30 kg: any function given a parcel weight outside that range raises ValueError.

    {DEC}volumetric weight uses 5000 cm³ per kg: a box of l x w x h cm weighs l*w*h/5000 kg.
    """,
    f"""
    Add zone(country) to zones.py: 1 for "NL", 2 for "BE", "DE", "FR" and "LU", and 3 for any other country code. Add tests.

    {RULE}country codes ignore case and must be exactly two letters; any function given another code raises ValueError.

    {DEC}shipping costs 200 cents for each started kilogram of the charged weight, on top of the zone's base price.

    {DEC}the weight line of a label has the form Weight: 1500 g.
    """,
    f"""
    Add vol_weight(l, w, h) to rates.py: the volumetric weight in grams of a box with sides in cm. Add tests.

    {CHG}shipping costs 150 cents for each started kilogram, not 200.

    {DEC}the charged weight of a parcel is the larger of its real weight and its volumetric weight.

    {DEC}"KP" and "IR" are blocked: any function given one of them raises ValueError.
    """,
    f"""
    Add split_parcels(grams) to parcels.py: the parcel weights when a shipment of that many grams is split into as few parcels of at most 30 kg as possible (70000 becomes [30000, 30000, 10000]). Add tests.

    {later("split_parcels", "the parcels are as equal as possible, heaviest first (70000 becomes [23334, 23333, 23333]).")}

    {CHG}volumetric weight uses 4000 cm³ per kg, not 5000.
    """,
    f"""
    Add tracking_code(n) to label.py: "TR" followed by n as 6 digits (42 becomes "TR000042"). Add tests.

    {later("tracking_code", 'a check digit is added at the end: the sum of the 6 digits modulo 10 (42 becomes "TR0000426").')}
    """,
    f"""
    Add zone_name(country) to zones.py: "home", "eu" or "world" for zones 1, 2 and 3. Add tests.

    {CHG}the weight line of a label has the form Weight: 1.5 kg (kilograms), not Weight: 1500 g.

    {DEC}in zone 3 the price per started kilogram is doubled.

    {DEC}the first line of a label is the tracking code.
    """,
    """
    Add cost(country, grams, dims=None) to rates.py: the shipping cost in cents (an int) of one parcel, where dims is an optional (l, w, h) box size in cm. The base price is 500 cents in zone 1, 900 in zone 2 and 1500 in zone 3, plus the price per started kilogram of the charged weight. Add tests.
    """,
    f"""
    Add write_label(n, country, grams, path) to label.py: it writes a text label with the tracking code for n, the country and the weight. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_weight(s) with tests. Its last step is left for later: accept grams and pounds (1 lb is 454 g).",
      [("parse_weight", "done"), ("parse_weight: accept g and lb", "todo")],
      ["A parcel weighs more than 0 and at most 30 kg; outside that range raises ValueError in any function.",
       "Volumetric weight uses 5000 cm³ per kg."]),
    g("Session 2 added zone(country) with tests.", [("zone", "done")],
      ["Country codes ignore case and must be two letters; another code raises ValueError in any function.",
       "Shipping costs 200 cents per started kilogram of charged weight, on top of the zone base price.",
       "A label weight line has the form Weight: 1500 g."]),
    g("Session 3 added vol_weight(l, w, h) with tests.", [("vol_weight", "done")],
      ["Supersedes 200 cents: shipping costs 150 cents per started kilogram.",
       "The charged weight is the larger of real and volumetric weight.",
       "\"KP\" and \"IR\" are blocked: any function given one raises ValueError."]),
    g("Session 4 added split_parcels(grams) with tests. Its last step is left for later: parcels as equal as possible, heaviest first.",
      [("split_parcels", "done"), ("split_parcels: as equal as possible", "todo")],
      ["Supersedes 5000: volumetric weight uses 4000 cm³ per kg."]),
    g("Session 5 added tracking_code(n) with tests. Its last step is left for later: a check digit, the digit sum modulo 10.",
      [("tracking_code", "done"), ("tracking_code: check digit", "todo")]),
    g("Session 6 added zone_name(country) with tests.", [("zone_name", "done")],
      ["Supersedes Weight: 1500 g: a label weight line has the form Weight: 1.5 kg.",
       "In zone 3 the price per started kilogram is doubled.",
       "The first label line is the tracking code."]),
    g("Session 7 added cost(country, grams, dims=None) with tests.", [("cost", "done")])],
   '''
   import re
   import pytest
   from parcels import parse_weight, split_parcels
   from zones import zone, zone_name
   from rates import cost, vol_weight
   from label import tracking_code, write_label


   def test_ship_basic():
       assert parse_weight("1.5kg") == 1500 and split_parcels(20000) == [20000]
       assert [zone(c) for c in ("NL", "FR", "US")] == [1, 2, 3] and zone_name("FR") == "eu"
       assert tracking_code(42).startswith("TR000042")
       assert cost("NL", 1000) < cost("DE", 1000) < cost("US", 1000)


   def test_fact_vol_4000():
       assert vol_weight(40, 30, 20) == 6000


   def test_stale_vol_5000():
       assert vol_weight(40, 30, 20) == 4800


   def test_fact_per_kg_150():
       assert cost("NL", 3500) - cost("NL", 1500) == 300


   def test_stale_per_kg_200():
       assert cost("NL", 3500) - cost("NL", 1500) == 400


   def _label(tmp_path):
       p = tmp_path / "l.txt"
       write_label(42, "DE", 1500, str(p))
       return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def test_fact_weight_kg(tmp_path):
       assert any(re.fullmatch(r"Weight: 1\\.50*\\s*kg", x) for x in _label(tmp_path))


   def test_stale_weight_g(tmp_path):
       assert any(re.fullmatch(r"Weight: 1500\\s*g", x) for x in _label(tmp_path))


   def test_fact_label_code(tmp_path):
       assert _label(tmp_path)[0] == tracking_code(42)


   def test_fact_parse_units():
       assert parse_weight("750g") == 750 and parse_weight("2lb") == 908 and parse_weight("1.5kg") == 1500


   def test_fact_split_equal():
       assert split_parcels(70000) == [23334, 23333, 23333] and split_parcels(60000) == [30000, 30000]


   def test_fact_check_digit():
       assert tracking_code(42) == "TR0000426" and tracking_code(999999) == "TR9999994"


   def test_fact_weight_range():
       for bad in (0, 30001):
           with pytest.raises(ValueError):
               cost("NL", bad)
       cost("NL", 30000)


   def test_fact_country_code():
       assert zone("de") == 2
       for bad in ("DEU", "1", ""):
           with pytest.raises(ValueError):
               zone(bad)


   def test_fact_charged_max():
       assert cost("NL", 1000, (40, 30, 20)) == cost("NL", vol_weight(40, 30, 20))
       assert cost("NL", 8000, (10, 10, 10)) == cost("NL", 8000)


   def test_fact_blocked():
       with pytest.raises(ValueError):
           zone("KP")
       with pytest.raises(ValueError):
           cost("ir", 1000)


   def test_fact_world_double():
       assert cost("US", 2500) - cost("US", 1500) == 2 * (cost("NL", 2500) - cost("NL", 1500))
   ''',
   {"parcels.py": '''
    from decimal import Decimal


    def parse_weight(s):
        s = s.strip().lower()
        for suf, f in (("kg", 1000), ("lb", 454), ("g", 1)):
            if s.endswith(suf):
                return int(Decimal(s[:-len(suf)].strip()) * f)
        raise ValueError("unknown unit")


    def split_parcels(grams):
        k = -(-grams // 30000)
        q, r = divmod(grams, k)
        return [q + 1] * r + [q] * (k - r)
    ''',
    "zones.py": '''
    def zone(country):
        c = country.strip().upper()
        if len(c) != 2 or not c.isalpha():
            raise ValueError("bad country code")
        if c in ("KP", "IR"):
            raise ValueError("blocked country")
        if c == "NL":
            return 1
        return 2 if c in ("BE", "DE", "FR", "LU") else 3


    def zone_name(country):
        return {1: "home", 2: "eu", 3: "world"}[zone(country)]
    ''',
    "rates.py": '''
    from zones import zone

    BASE = {1: 500, 2: 900, 3: 1500}


    def vol_weight(l, w, h):
        return -(-(l * w * h) // 4)


    def cost(country, grams, dims=None):
        if not 0 < grams <= 30000:
            raise ValueError("bad weight")
        z = zone(country)
        charged = max(grams, vol_weight(*dims)) if dims else grams
        per = 150 * (2 if z == 3 else 1)
        return BASE[z] + per * -(-charged // 1000)
    ''',
    "label.py": '''
    def tracking_code(n):
        d = f"{n:06d}"
        return f"TR{d}{sum(int(c) for c in d) % 10}"


    def write_label(n, country, grams, path):
        with open(path, "w", encoding="utf8") as f:
            f.write(tracking_code(n) + "\\n")
            f.write(f"To: {country.upper()}\\n")
            f.write(f"Weight: {grams / 1000:g} kg\\n")
    '''})
