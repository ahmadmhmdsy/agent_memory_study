"""Unfinished tasks S17-S24: session 2 plans (a), (b), (c), does (a) and (b) and defers (c).
Session 3 says only "finish the remaining planned work", so only memory carries (c)'s spec."""
from scored_common import mk, g

LATER = "Do (a) and (b) now, with tests. Leave (c) for a later session; do not start it now."
FINISH = "Finish the remaining planned work for this project, with tests. Then"


def plan(intro, a, b, c):
    return f"""
    {intro}
    (a) {a}
    (b) {b}
    (c) {c}

    {LATER}
    """


def given2(a, b, c):
    return g(f"Session 2 did (a) and (b). (c) is not started: {c}",
             [(f"(a) {a}", "done"), (f"(b) {b}", "done"), (f"(c) {c}", "todo")])


# S17 stack: peek() returns None when empty
A, B = "is_empty(): True when the stack has no items.", "clear(): removes every item."
C = "peek(): returns the top item without removing it; on an empty stack it returns None (it does not raise)."
mk("S17", "unfinished", "stack.py", "A stack for an undo feature.",
   '''
   """Stack for an undo feature."""


   class Stack:
       def __init__(self):
           self.items = []

       def push(self, x):
           self.items.append(x)
   ''',
   '''
   from stack import Stack


   def test_push():
       s = Stack()
       s.push(1)
       assert s.items == [1]
   ''',
   ["""
    Add pop() and __len__() to Stack in stack.py. pop() removes and returns the top item and raises IndexError when the stack is empty. Add tests.
    """,
    plan("Planned work for Stack:", A, B, C),
    f"""
    {FINISH} add to_list() to Stack: the items from bottom to top, as a new list. Add tests.
    """],
   [g("Session 1 added pop() and __len__() with tests.", [("pop, __len__", "done")]), given2(A, B, C)],
   '''
   import pytest
   from stack import Stack


   def test_basics():
       s = Stack()
       with pytest.raises(IndexError):
           s.pop()
       s.push(1)
       s.push(2)
       assert len(s) == 2 and s.pop() == 2 and not s.is_empty()
       s.clear()
       assert s.is_empty() and s.to_list() == []


   def test_fact_peek():
       s = Stack()
       assert s.peek() is None
       s.push(1)
       s.push(2)
       assert s.peek() == 2 and len(s) == 2
   ''',
   '''
   class Stack:
       def __init__(self):
           self.items = []

       def push(self, x):
           self.items.append(x)

       def pop(self):
           return self.items.pop()

       def __len__(self):
           return len(self.items)

       def is_empty(self):
           return not self.items

       def clear(self):
           self.items.clear()

       def peek(self):
           return self.items[-1] if self.items else None

       def to_list(self):
           return list(self.items)
   ''')

# S18 strings: truncate with a single "…"
A, B = "capitalize_words(s): each word's first letter upper case.", "reverse_words(s): the words in reverse order, joined by one space."
C = ('truncate(s, n): when len(s) > n, the first n-1 characters followed by "…" (the single character U+2026), '
     'so the result is exactly n characters long; otherwise s unchanged.')
mk("S18", "unfinished", "strings.py", "String helpers for a chat app.",
   '''
   """String helpers."""
   ''',
   '''
   from strings import shout


   def test_shout():
       assert shout("hi") == "HI!"
   ''',
   ["""
    Add shout(s) to strings.py: s in upper case followed by "!". Add tests.
    """,
    plan("Planned string helpers for strings.py:", A, B, C),
    f"""
    {FINISH} add count_vowels(s) to strings.py: the number of a, e, i, o, u letters in s, ignoring case. Add tests.
    """],
   [g("Session 1 added shout(s) with tests.", [("shout", "done")]), given2(A, B, C)],
   '''
   from strings import shout, capitalize_words, reverse_words, truncate, count_vowels


   def test_basics():
       assert shout("a") == "A!"
       assert capitalize_words("hello big world") == "Hello Big World"
       assert reverse_words("a b c") == "c b a"
       assert count_vowels("AbE") == 2


   def test_fact_truncate():
       assert truncate("abcdef", 4) == "abc\\u2026"
       assert len(truncate("hello world", 5)) == 5
       assert truncate("abc", 4) == "abc"
       assert truncate("abcd", 4) == "abcd"
   ''',
   '''
   def shout(s):
       return s.upper() + "!"


   def capitalize_words(s):
       return " ".join(w[:1].upper() + w[1:] for w in s.split())


   def reverse_words(s):
       return " ".join(reversed(s.split()))


   def truncate(s, n):
       return s if len(s) <= n else s[:n - 1] + "\\u2026"


   def count_vowels(s):
       return sum(ch in "aeiou" for ch in s.lower())
   ''')

# S19 grades: A>=85, B>=70, C>=55, else F
A, B = "mean(scores): the arithmetic mean of a non-empty list.", "highest(scores): the largest score."
C = 'letter(score): "A" for 85 and above, "B" for 70 to 84, "C" for 55 to 69, "F" below 55 (there is no D).'
mk("S19", "unfinished", "grades.py", "Grade helpers for a school.",
   '''
   """Grade helpers. Scores are numbers from 0 to 100."""
   ''',
   '''
   from grades import clamp


   def test_clamp():
       assert clamp(101) == 100
   ''',
   ["""
    Add clamp(score) to grades.py: score limited to the range 0..100. Add tests.
    """,
    plan("Planned grade helpers for grades.py:", A, B, C),
    f"""
    {FINISH} add spread(scores) to grades.py: the highest score minus the lowest. Add tests.
    """],
   [g("Session 1 added clamp(score) with tests.", [("clamp", "done")]), given2(A, B, C)],
   '''
   from grades import clamp, mean, highest, letter, spread


   def test_basics():
       assert clamp(-1) == 0 and mean([2, 4]) == 3 and highest([1, 7, 3]) == 7
       assert spread([4, 9, 1]) == 8


   def test_fact_letter_bands():
       got = [letter(s) for s in (100, 85, 84, 70, 69, 55, 54, 0)]
       assert got == ["A", "A", "B", "B", "C", "C", "F", "F"]
   ''',
   '''
   def clamp(score):
       return max(0, min(100, score))


   def mean(scores):
       return sum(scores) / len(scores)


   def highest(scores):
       return max(scores)


   def letter(score):
       return "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "F"


   def spread(scores):
       return max(scores) - min(scores)
   ''')

# S20 inventory2: low_stock(threshold=5), strictly below, sorted A-Z
A, B = "qty(name): the quantity of name, 0 when unknown.", "names(): every stored name, sorted A to Z."
C = "low_stock(threshold=5): the names whose quantity is strictly below threshold, sorted A to Z."
mk("S20", "unfinished", "inventory2.py", "Stock levels for a warehouse.",
   '''
   """Stock levels."""


   class Store:
       def __init__(self):
           self.stock = {}
   ''',
   '''
   from inventory2 import Store


   def test_add():
       s = Store()
       s.add("pen", 2)
       assert s.stock == {"pen": 2}
   ''',
   ["""
    Add add(name, qty) to Store in inventory2.py: it adds qty to the stored quantity of name. Add tests.
    """,
    plan("Planned work for Store:", A, B, C),
    f"""
    {FINISH} add total() to Store: the sum of all quantities. Add tests.
    """],
   [g("Session 1 added Store.add(name, qty) with tests.", [("Store.add", "done")]), given2(A, B, C)],
   '''
   from inventory2 import Store


   def make():
       s = Store()
       for n, q in [("pen", 2), ("cup", 5), ("bag", 1), ("ink", 9)]:
           s.add(n, q)
       return s


   def test_basics():
       s = make()
       assert s.qty("pen") == 2 and s.qty("zzz") == 0
       assert s.names() == ["bag", "cup", "ink", "pen"] and s.total() == 17


   def test_fact_low_stock():
       s = make()
       assert s.low_stock() == ["bag", "pen"]
       assert s.low_stock(6) == ["bag", "cup", "pen"]
   ''',
   '''
   class Store:
       def __init__(self):
           self.stock = {}

       def add(self, name, qty):
           self.stock[name] = self.stock.get(name, 0) + qty

       def qty(self, name):
           return self.stock.get(name, 0)

       def names(self):
           return sorted(self.stock)

       def low_stock(self, threshold=5):
           return sorted(n for n, q in self.stock.items() if q < threshold)

       def total(self):
           return sum(self.stock.values())
   ''')

# S21 timeparse: to_seconds with "MM:SS" for two parts
A, B = 'format_hms(seconds): the string "H:MM:SS", e.g. 3723 gives "1:02:03".', "parts(seconds): the tuple (hours, minutes, seconds)."
C = 'to_seconds(s): parses "H:MM:SS" into an int number of seconds; a string with only two parts, like "02:03", means minutes and seconds.'
mk("S21", "unfinished", "timeparse.py", "Duration helpers for a video player.",
   '''
   """Duration helpers."""
   ''',
   '''
   from timeparse import pad2


   def test_pad2():
       assert pad2(5) == "05"
   ''',
   ["""
    Add pad2(n) to timeparse.py: the int n as a string of at least two digits, padded with a leading zero. Add tests.
    """,
    plan("Planned duration helpers for timeparse.py:", A, B, C),
    f"""
    {FINISH} add is_long(seconds) to timeparse.py: True when seconds is more than one hour. Add tests.
    """],
   [g("Session 1 added pad2(n) with tests.", [("pad2", "done")]), given2(A, B, C)],
   '''
   from timeparse import pad2, format_hms, parts, to_seconds, is_long


   def test_basics():
       assert pad2(12) == "12" and format_hms(3723) == "1:02:03" and parts(3723) == (1, 2, 3)
       assert is_long(3601) and not is_long(3600)


   def test_fact_to_seconds():
       assert to_seconds("1:02:03") == 3723
       assert to_seconds("02:03") == 123
       assert to_seconds("0:00:05") == 5
       assert type(to_seconds("10:00")) is int
   ''',
   '''
   def pad2(n):
       return f"{n:02d}"


   def parts(seconds):
       return (seconds // 3600, seconds % 3600 // 60, seconds % 60)


   def format_hms(seconds):
       h, m, s = parts(seconds)
       return f"{h}:{pad2(m)}:{pad2(s)}"


   def to_seconds(s):
       nums = [int(x) for x in s.split(":")]
       if len(nums) == 2:
           nums = [0] + nums
       h, m, sec = nums
       return h * 3600 + m * 60 + sec


   def is_long(seconds):
       return seconds > 3600
   ''')

# S22 urltools: query_params, last value wins
A, B = "host(url): the host name, e.g. \"example.com\".", "path(url): the path, \"/\" when the URL has none."
C = ("query_params(url): a dict of the query parameters with string values; when a key repeats, the last value wins; "
     "a URL with no query gives {}.")
mk("S22", "unfinished", "urltools.py", "URL helpers for a crawler.",
   '''
   """URL helpers."""
   ''',
   '''
   from urltools import scheme


   def test_scheme():
       assert scheme("https://a.com/x") == "https"
   ''',
   ["""
    Add scheme(url) to urltools.py: the part before "://", in lower case. Add tests.
    """,
    plan("Planned URL helpers for urltools.py:", A, B, C),
    f"""
    {FINISH} add is_secure(url) to urltools.py: True when the scheme is https. Add tests.
    """],
   [g("Session 1 added scheme(url) with tests.", [("scheme", "done")]), given2(A, B, C)],
   '''
   from urltools import scheme, host, path, query_params, is_secure


   def test_basics():
       u = "HTTPS://example.com/a/b?x=1"
       assert scheme(u) == "https" and host(u) == "example.com" and path(u) == "/a/b"
       assert path("http://e.com") == "/" and is_secure(u) and not is_secure("http://e.com")


   def test_fact_query_params():
       assert query_params("http://e.com/p?a=1&b=x&a=2") == {"a": "2", "b": "x"}
       assert query_params("http://e.com/p") == {}
   ''',
   '''
   from urllib.parse import urlsplit, parse_qsl


   def scheme(url):
       return url.split("://", 1)[0].lower()


   def host(url):
       return urlsplit(url).hostname


   def path(url):
       return urlsplit(url).path or "/"


   def query_params(url):
       return dict(parse_qsl(urlsplit(url).query))


   def is_secure(url):
       return scheme(url) == "https"
   ''')

# S23 bank: statement lines "+100"/"-30", oldest first
A, B = "withdraw(amount): takes amount off the balance; raises ValueError when the balance is too small.", "transaction_count(): how many deposits and withdrawals were made."
C = ('statement(): a list of strings, one per deposit or withdrawal, oldest first: "+100" for a deposit of 100, '
     '"-30" for a withdrawal of 30.')
mk("S23", "unfinished", "bank.py", "A bank account model. Amounts are whole numbers.",
   '''
   """Bank account model. Amounts are ints."""


   class Account:
       def __init__(self):
           self.balance = 0
   ''',
   '''
   from bank import Account


   def test_new():
       assert Account().balance == 0
   ''',
   ["""
    Add deposit(amount) to Account in bank.py: it adds amount to the balance. Add tests.
    """,
    plan("Planned work for Account:", A, B, C),
    f"""
    {FINISH} add largest_deposit() to Account: the largest single deposit, or 0 when there is none. Add tests.
    """],
   [g("Session 1 added Account.deposit(amount) with tests.", [("deposit", "done")]), given2(A, B, C)],
   '''
   import pytest
   from bank import Account


   def test_basics():
       a = Account()
       a.deposit(100)
       a.withdraw(30)
       with pytest.raises(ValueError):
           a.withdraw(1000)
       assert a.balance == 70 and a.transaction_count() == 2 and a.largest_deposit() == 100


   def test_fact_statement():
       a = Account()
       a.deposit(100)
       a.withdraw(30)
       a.deposit(5)
       assert a.statement() == ["+100", "-30", "+5"]
   ''',
   '''
   class Account:
       def __init__(self):
           self.balance = 0
           self.moves = []

       def deposit(self, amount):
           self.balance += amount
           self.moves.append(amount)

       def withdraw(self, amount):
           if amount > self.balance:
               raise ValueError("insufficient funds")
           self.balance -= amount
           self.moves.append(-amount)

       def transaction_count(self):
           return len(self.moves)

       def statement(self):
           return [f"{m:+d}" for m in self.moves]

       def largest_deposit(self):
           return max([m for m in self.moves if m > 0], default=0)
   ''')

# S24 wordfreq: rare_words, stopwords excluded, sorted A-Z
A, B = "counts(text): a dict mapping each word of words(text) to how often it appears.", "top_words(text, n): the n most frequent words, most frequent first, ties A to Z."
C = ('rare_words(text, max_count=1): the words appearing at most max_count times, excluding the stopwords '
     '"the", "a", "an", "and", "of", "to", "in", sorted A to Z.')
mk("S24", "unfinished", "wordfreq.py", "Word statistics for a text tool.",
   '''
   """Word statistics."""
   ''',
   '''
   from wordfreq import words


   def test_words():
       assert words("Hi, hi!") == ["hi", "hi"]
   ''',
   ["""
    Add words(text) to wordfreq.py: the list of words in text, in lower case, where a word is a run of letters. Add tests.
    """,
    plan("Planned word statistics for wordfreq.py:", A, B, C),
    f"""
    {FINISH} add unique_count(text) to wordfreq.py: the number of distinct words. Add tests.
    """],
   [g("Session 1 added words(text) with tests.", [("words", "done")]), given2(A, B, C)],
   '''
   from wordfreq import words, counts, top_words, rare_words, unique_count

   TEXT = "the cat and the dog and a cat bird"


   def test_basics():
       assert counts("b a b") == {"b": 2, "a": 1}
       assert top_words("b a b c c", 2) == ["b", "c"]
       assert unique_count(TEXT) == 6


   def test_fact_rare_words():
       assert rare_words(TEXT) == ["bird", "dog"]
       assert rare_words(TEXT, 2) == ["bird", "cat", "dog"]
   ''',
   '''
   import re
   from collections import Counter

   STOP = {"the", "a", "an", "and", "of", "to", "in"}


   def words(text):
       return re.findall(r"[a-z]+", text.lower())


   def counts(text):
       return dict(Counter(words(text)))


   def top_words(text, n):
       return [w for w, _ in sorted(counts(text).items(), key=lambda kv: (-kv[1], kv[0]))[:n]]


   def rare_words(text, max_count=1):
       return sorted(w for w, c in counts(text).items() if c <= max_count and w not in STOP)


   def unique_count(text):
       return len(counts(text))
   ''')

print("unfinished ok")
