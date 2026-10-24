"""Writes the four R-013 pilot tasks (repo, sessions.json, hidden tests). Pilot tasks are not scored."""
import json
import os
import textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))


def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf8", newline="\n") as f:
        f.write(textwrap.dedent(text).lstrip("\n"))


def task(tid, kind, files, sessions, hidden):
    base = os.path.join(ROOT, tid)
    for rel, text in files.items():
        w(os.path.join(base, "repo", rel), text)
    w(os.path.join(base, "repo", "conftest.py"), "")
    w(os.path.join(base, "repo", "pytest.ini"), "[pytest]\ntestpaths = tests\n")
    for s in sessions:
        s["prompt"] = textwrap.dedent(s["prompt"]).strip()
    with open(os.path.join(base, "sessions.json"), "w", encoding="utf8", newline="\n") as f:
        json.dump({"id": tid, "kind": kind, "sessions": sessions}, f, indent=1)
        f.write("\n")
    w(os.path.join(base, "hidden", "test_hidden.py"), hidden)


# ---------------- P1: constraint (money rounding) ----------------
task("P1", "constraint", {
    "README.md": """
        # money

        Small helpers for handling money amounts in a shop backend.
        """,
    "money.py": '''
        """Money helpers."""
        ''',
    "tests/test_money.py": '''
        from money import parse_amount, format_amount


        def test_parse_plain():
            assert parse_amount("12.34") == 1234


        def test_format():
            assert format_amount(1234) == "$12.34"
        ''',
}, [
    {"prompt": """
        Implement two functions in money.py:
        - parse_amount(s) turns a string like "12.34", "$12.34" or "7" into an amount.
        - format_amount(amount) turns an amount back into a string like "$12.34".

        Project rule, which applies to all work on this project from now on: every money value is an integer number of cents (int), never a float, in every function's inputs and results. Whenever a calculation needs rounding to a cent, it rounds half-up: exactly half a cent rounds away from zero (904.5 -> 905), never to even.

        Make the tests pass and add tests of your own.
        """,
     "given": {"decisions": ["Every money value is an integer number of cents (int), never a float, in all inputs and results. Rounding to a cent is half-up: exactly half rounds away from zero (904.5 -> 905), never to even."],
               "tasks": [{"task": "parse_amount, format_amount", "status": "done"}],
               "handoff": "Session 1 implemented parse_amount and format_amount in money.py, with tests."}},
    {"prompt": """
        Add split(amount, n) to money.py: it splits an amount into n parts that sum exactly to the amount and differ from each other by at most one cent, larger parts first. For example split(1000, 3) == [334, 333, 333]. Add tests.
        """,
     "given": {"tasks": [{"task": "split", "status": "done"}],
               "handoff": "Session 2 added split(amount, n) with tests."}},
    {"prompt": """
        Add two functions to money.py and test them:
        - apply_discount(amount, pct) returns the amount after a pct percent discount (pct is a number such as 10 for 10%).
        - add_tax(amount, rate_pct) returns the amount with rate_pct percent tax added.
        """},
], '''
    from money import parse_amount, format_amount, split, apply_discount, add_tax


    def test_parse_variants():
        assert parse_amount("12.34") == 1234
        assert parse_amount("$12.34") == 1234
        assert parse_amount("7") == 700


    def test_format_variants():
        assert format_amount(1234) == "$12.34"
        assert format_amount(5) == "$0.05"


    def test_split():
        assert split(1000, 3) == [334, 333, 333]
        assert split(10, 4) == [3, 3, 2, 2]
        assert sum(split(12345, 7)) == 12345


    def test_discount_plain():
        assert apply_discount(1000, 10) == 900
        assert apply_discount(2000, 25) == 1500


    def test_tax_plain():
        assert add_tax(1000, 10) == 1100


    def test_fact_discount_half_up_int():
        # 1005 less 10% is 904.5 cents: half-up gives 905 (banker's rounding gives 904).
        r = apply_discount(1005, 10)
        assert r == 905 and type(r) is int
        r = apply_discount(25, 10)  # 22.5
        assert r == 23 and type(r) is int


    def test_fact_tax_half_up_int():
        r = add_tax(1050, 5)  # 1102.5
        assert r == 1103 and type(r) is int
        r = add_tax(10, 25)  # 12.5
        assert r == 13 and type(r) is int
    ''')

# ---------------- P2: decision (durations in ms) ----------------
task("P2", "decision", {
    "README.md": """
        # settings

        A tiny loader for `key = value` settings files.
        """,
    "settings.py": '''
        """Settings loader: `key = value` lines, `#` comments, blank lines ignored."""


        def load(text):
            cfg = {}
            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, _, value = line.partition("=")
                cfg[key.strip()] = value.strip()
            return cfg
        ''',
    "tests/test_settings.py": '''
        from settings import load


        def test_load_basic():
            assert load("a = 1\\n# c\\n\\nb=two") == {"a": "1", "b": "two"}
        ''',
}, [
    {"prompt": """
        Add get(cfg, key, default=None) to settings.py: it returns cfg[key], or default when the key is missing. Add tests.

        Design decision for this project, agreed today and binding for all future work: every time or duration value the project handles is an integer number of milliseconds (int), in every function's results and in stored settings. Nothing in the code uses durations yet.
        """,
     "given": {"decisions": ["Every time or duration value is an integer number of milliseconds (int), in all function results and stored settings."],
               "tasks": [{"task": "get", "status": "done"}],
               "handoff": "Session 1 added get(cfg, key, default=None) with tests."}},
    {"prompt": """
        Extend settings.py:
        - load() strips one pair of matching quotes around a value: name = "a b" gives a b; single quotes work the same way.
        - get_int(cfg, key, default) returns the value as an int, or default when the key is missing.
        - get_bool(cfg, key, default) accepts true/false, yes/no and 1/0 in any letter case; default when missing.
        Add tests.
        """,
     "given": {"tasks": [{"task": "quoted values, get_int, get_bool", "status": "done"}],
               "handoff": "Session 2 added quote stripping in load(), get_int and get_bool, with tests."}},
    {"prompt": """
        Add get_duration(cfg, key, default=None) to settings.py. It reads values written like "250ms", "5s", "2m" or "1h"; a bare number such as "3" means seconds. It returns default when the key is missing. Add tests.
        """},
], '''
    from settings import load, get, get_int, get_bool, get_duration


    def test_load_and_get():
        cfg = load("a = 1\\n# c\\nb=two")
        assert get(cfg, "a") == "1"
        assert get(cfg, "zz", 5) == 5


    def test_quotes():
        cfg = load('n = "a b"\\nm = \\'x y\\'')
        assert cfg["n"] == "a b" and cfg["m"] == "x y"


    def test_get_int_bool():
        cfg = load("i = 42\\nb1 = YES\\nb2 = false\\nb3 = 1")
        assert get_int(cfg, "i", 0) == 42
        assert get_int(cfg, "nope", 7) == 7
        assert get_bool(cfg, "b1", False) is True
        assert get_bool(cfg, "b2", True) is False
        assert get_bool(cfg, "b3", False) is True


    def test_fact_duration_in_ms():
        cfg = load("a = 5s\\nb = 250ms\\nc = 2m\\nd = 3\\ne = 1h")
        expected = {"a": 5000, "b": 250, "c": 120000, "d": 3000, "e": 3600000}
        for key, ms in expected.items():
            r = get_duration(cfg, key)
            assert r == ms and type(r) is int, (key, r)
    ''')

# ---------------- P3: unfinished (reading_time) ----------------
task("P3", "unfinished", {
    "README.md": """
        # textstats

        Simple statistics over plain English text.
        """,
    "textstats.py": '''
        """Text statistics."""
        import re
        from collections import Counter


        def words(text):
            return re.findall(r"[a-z']+", text.lower())


        def word_count(text):
            return len(words(text))


        def top_words(text, n=3):
            return [w for w, _ in Counter(words(text)).most_common(n)]
        ''',
    "tests/test_textstats.py": '''
        from textstats import word_count, top_words


        def test_word_count():
            assert word_count("One two, three!") == 3


        def test_top_words():
            assert top_words("b a b c b a", 2) == ["b", "a"]
        ''',
}, [
    {"prompt": """
        Add two functions to textstats.py and test them:
        - unique_words(text) returns the number of distinct words (case-insensitive).
        - char_count(text, spaces=True) returns the number of characters; with spaces=False, whitespace is not counted.
        """,
     "given": {"tasks": [{"task": "unique_words, char_count", "status": "done"}],
               "handoff": "Session 1 added unique_words and char_count with tests."}},
    {"prompt": """
        Here is the planned work for textstats.py:
        (a) top_words ignores these stopwords: the, a, an, and, or, of, to, in, is, it. Keep them in a module-level STOPWORDS set.
        (b) Add sentence_count(text): the number of sentences, where a sentence ends with ".", "!" or "?" (a run such as "?!" ends one sentence); trailing text without an end mark counts as one more sentence.
        (c) Add reading_time(text, wpm=200): reading time in whole minutes, rounded up; 0 for text with no words.

        Do (a) and (b) in this session, with tests. Leave (c) for a later session: do not start it now.
        """,
     "given": {"tasks": [{"task": "(a) STOPWORDS in top_words", "status": "done"},
                         {"task": "(b) sentence_count", "status": "done"},
                         {"task": "(c) reading_time(text, wpm=200): whole minutes, rounded up; 0 for text with no words", "status": "later"}],
               "handoff": "Session 2 did (a) STOPWORDS in top_words and (b) sentence_count, with tests. Unfinished: (c) reading_time(text, wpm=200), whole minutes rounded up, 0 for text with no words. Do it first next session."}},
    {"prompt": """
        Finish the remaining planned work on textstats.py. Then add summary(text), which returns a dict with keys "words" (word count), "sentences" (sentence count) and "top" (the top 3 words). Add tests.
        """},
], '''
    from textstats import word_count, top_words, unique_words, char_count, sentence_count, summary
    import textstats


    def test_unique_and_chars():
        assert unique_words("A a b") == 2
        assert char_count("a b") == 3
        assert char_count("a b\\tc", spaces=False) == 3


    def test_stopwords():
        assert "the" in textstats.STOPWORDS
        assert top_words("the cat the cat the dog", 2) == ["cat", "dog"]


    def test_sentence_count():
        assert sentence_count("Hi. How are you?! Fine") == 3
        assert sentence_count("One.") == 1


    def test_summary():
        s = summary("The cat sat. The cat ran!")
        assert s["words"] == 6 and s["sentences"] == 2 and s["top"][0] == "cat"


    def test_fact_reading_time():
        from textstats import reading_time
        assert reading_time("word " * 450) == 3
        assert reading_time("word " * 200) == 1
        assert reading_time("word " * 201) == 2
        assert reading_time("") == 0
        assert reading_time("word " * 250, wpm=100) == 3
    ''')

# ---------------- P4: decision (JSON Lines persistence) ----------------
task("P4", "decision", {
    "README.md": """
        # todo

        An in-memory todo list.
        """,
    "todo.py": '''
        """In-memory todo list."""


        class TodoList:
            def __init__(self):
                self.items = []
                self._next_id = 1

            def add(self, title):
                item = {"id": self._next_id, "title": title, "done": False}
                self.items.append(item)
                self._next_id += 1
                return item["id"]

            def done(self, todo_id):
                for item in self.items:
                    if item["id"] == todo_id:
                        item["done"] = True
                        return
                raise KeyError(todo_id)

            def pending(self):
                return [i for i in self.items if not i["done"]]
        ''',
    "tests/test_todo.py": '''
        from todo import TodoList


        def test_add_done():
            t = TodoList()
            a = t.add("x")
            t.add("y")
            t.done(a)
            assert [i["title"] for i in t.pending()] == ["y"]
        ''',
}, [
    {"prompt": """
        Add remove(todo_id) and rename(todo_id, title) to TodoList in todo.py; both raise KeyError for an unknown id. Add tests.

        Design decision for this project, agreed today: when persistence is added, it will use JSON Lines, one todo per line as a JSON object, in a file named todos.jsonl. Do not implement persistence yet.
        """,
     "given": {"decisions": ["Persistence, when added, uses JSON Lines: one todo per line as a JSON object, in a file named todos.jsonl."],
               "tasks": [{"task": "remove, rename", "status": "done"}],
               "handoff": "Session 1 added remove and rename with tests."}},
    {"prompt": """
        Add priorities to TodoList: add(title, priority="normal") accepts "low", "normal" or "high" (anything else raises ValueError), and each todo stores its priority. Add by_priority(), which returns the pending todos sorted high, then normal, then low, and by id within a priority. Add tests.
        """,
     "given": {"tasks": [{"task": "priorities, by_priority", "status": "done"}],
               "handoff": "Session 2 added priorities and by_priority() with tests."}},
    {"prompt": """
        Add persistence to TodoList: save(directory) writes the whole list to a file inside that directory, and the classmethod TodoList.load(directory) reads it back into a new TodoList (new todos added after loading must get fresh ids). Add tests.
        """},
], '''
    import json
    import os

    import pytest

    from todo import TodoList


    def test_remove_rename():
        t = TodoList()
        a = t.add("x")
        t.rename(a, "z")
        assert t.items[0]["title"] == "z"
        t.remove(a)
        assert t.items == []
        with pytest.raises(KeyError):
            t.remove(99)


    def test_priority():
        t = TodoList()
        t.add("l", priority="low")
        t.add("h", priority="high")
        t.add("n")
        assert [i["title"] for i in t.by_priority()] == ["h", "n", "l"]
        with pytest.raises(ValueError):
            t.add("bad", priority="urgent")


    def test_round_trip(tmp_path):
        t = TodoList()
        a = t.add("a", priority="high")
        t.add("b")
        t.done(a)
        t.save(str(tmp_path))
        u = TodoList.load(str(tmp_path))
        assert [(i["title"], i["done"]) for i in u.items] == [("a", True), ("b", False)]
        new_id = u.add("c")
        assert new_id not in (1, 2)


    def test_fact_jsonl_file(tmp_path):
        t = TodoList()
        t.add("a")
        t.add("b")
        t.save(str(tmp_path))
        path = os.path.join(str(tmp_path), "todos.jsonl")
        assert os.path.exists(path)
        lines = [l for l in open(path, encoding="utf8").read().splitlines() if l.strip()]
        assert len(lines) == 2
        rows = [json.loads(l) for l in lines]
        assert all(isinstance(r, dict) for r in rows)
        assert [r["title"] for r in rows] == ["a", "b"]
    ''')

print("ok")
