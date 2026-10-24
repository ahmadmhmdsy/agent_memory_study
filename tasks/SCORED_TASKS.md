# R-013 scored tasks (S01–S24)

Every task has 3 sessions. The fact is stated only in session 1 (constraint, decision) or session 2 (unfinished); the session-3 prompt never repeats it. Session 1–2 work never embodies the fact in code, so only memory carries it. Pilot lessons applied:
- Each fact goes against the default choice. Checked: a "default" version of each module (`check_scored.py`, `DEFAULTS`) passes every plain hidden test and fails every `test_fact*`.
- Each fact test checks the exact shape: value, type and format.

Generators: `make_scored_constraint.py`, `make_scored_decision.py`, `make_scored_unfinished.py` (shared `scored_common.py`). Check: `python check_scored.py` (reference passes visible + hidden; default fails only the fact tests). Result 2026-10-19: 24/24 ok.

## Constraint: a rule stated in S1 that S3's new function must follow

| id | module | S1 work + rule | S2 work | S3 work | fact test | default that fails |
|---|---|---|---|---|---|---|
| S01 | dates.py | `is_weekend`; returned dates are `DD/MM/YYYY` strings | `weekday_name` | `next_business_day(d)` | Fri 2026-01-02 → `"05/01/2026"` (str) | returns a `date` |
| S02 | ranking.py | `mean`; returned lists sorted descending | `median` | `unique_scores` | `[9, 5, 2]` | ascending |
| S03 | parsing.py | `strip_all`; bad input returns `None`, never raises | `split_fields` | `parse_date_iso` | `"2026-13-40"`, `"hello"`, `""` → `None` | raises ValueError |
| S04 | inventory.py | `add_stock`, `quantity`; every error is `InventoryError(Exception)`, not a built-in subclass | `total_items` | `remove_stock` over stock | raises `InventoryError`, not ValueError/KeyError; stock unchanged | `InventoryError(ValueError)` |
| S05 | rates.py | `total`; rates are fractions 0–1, 4 places | `count_items` | `discount_rate`, `growth` | `0.1`, `0.05`; `growth(3,4) == 0.3333` | 10 / 33.33 |
| S06 | export.py | `make_task`; booleans in files are `Y`/`N` | `pending` | `write_csv` | lines `title,done` / `a,Y` / `b,N` | `True`/`False` |
| S07 | users.py | `is_valid_email`; usernames stored stripped, lowercase, space runs → `.` | `domain` | `Users.add/names/has` | `["ann.lee", "bo.diaz"]` | stored as given |
| S08 | temps.py | `is_freezing`; returned temperatures in Kelvin, 2 places | `count_above` | `average` | `average([0,10]) == 278.15` | 5.0 (Celsius) |

## Decision: a design decision recorded in S1 that S3 implements (S3's prompt leaves the choice open)

| id | module | S1 work + decision | S2 work | S3 work | fact test | default that fails |
|---|---|---|---|---|---|---|
| S09 | cache.py | `Cache.put/get`; eviction is LFU by get() reads, ties → first added | `stats()` | `Cache(max_items)` | evicts the less-read key; tie → oldest, update is not a new key | FIFO / LRU |
| S10 | paging.py | `clamp`; pages start at 0 | `count_pages` | `page(items, number, size)` | `page(x,0,2) == [1,2]`, past end `[]` | 1-based |
| S11 | slug.py | `word_count`; slugs join words with `_` | `clean` | `slugify` | `"hi_there_friend"` | `-` |
| S12 | report.py | `row_total`; CSV uses `;` with a header row | `totals` | `export(rows, path)` | `name;qty;price` / `pen;2;3` | `,` |
| S13 | log.py | `Logger.count`; timestamps UTC `YYYY-MM-DDTHH:MM:SSZ` | `Logger.lines` | `Logger.log(msg, now)` | `"2026-01-05T10:30:00Z hello"` from a +02:00 time with µs | `isoformat()` |
| S14 | tickets.py | `TicketBook.count`; ids `T0001`, `T0002`… | `close`, `open_titles` | `TicketBook.add(title)` | `"T0001"`, `"T0002"`, dict keys | int ids |
| S15 | config.py | `parse_bool`; key lookup ignores case | `load(text)` | `get(cfg, key, default)` | `get(load("Port = 8080"), "PORT") == "8080"` | `cfg.get` |
| S16 | scores.py | `clamp_score`; averages truncated to int | `best` | `average` | `average([1,2]) == 1` (int), `[99,100] → 99` | float |

## Unfinished: S2 plans (a), (b), (c), does (a) and (b), defers (c); S3 says "Finish the remaining planned work, with tests. Then add …"

| id | module | S1 work | S2 (a), (b) | deferred (c) | S3 new work | fact test | default that fails |
|---|---|---|---|---|---|---|---|
| S17 | stack.py | `pop`, `__len__` | `is_empty`, `clear` | `peek()`: `None` when empty | `to_list` | `Stack().peek() is None` | raises IndexError |
| S18 | strings.py | `shout` | `capitalize_words`, `reverse_words` | `truncate(s, n)`: n chars, ends in `…` (U+2026) | `count_vowels` | `"abcdef",4 → "abc…"` | `s[:n] + "..."` |
| S19 | grades.py | `clamp` | `mean`, `highest` | `letter`: A≥85, B≥70, C≥55, else F (no D) | `spread` | 85 A, 84 B, 69 C, 54 F | 90/80/70/60 with D |
| S20 | inventory2.py | `Store.add` | `qty`, `names` | `low_stock(threshold=5)`: qty < threshold, A–Z | `total` | `["bag","pen"]`, `(6) → ["bag","cup","pen"]` | `<= 10`, unsorted |
| S21 | timeparse.py | `pad2` | `format_hms`, `parts` | `to_seconds`: `H:MM:SS`; two parts = `MM:SS` | `is_long` | 3723, `"02:03" → 123` (int) | two parts = H:MM |
| S22 | urltools.py | `scheme` | `host`, `path` | `query_params`: str values, last repeat wins | `is_secure` | `{"a": "2", "b": "x"}`, no query `{}` | `parse_qs` lists |
| S23 | bank.py | `deposit` | `withdraw`, `transaction_count` | `statement()`: `"+100"`, `"-30"`, oldest first | `largest_deposit` | `["+100", "-30", "+5"]` | `"Deposit: 100"` |
| S24 | wordfreq.py | `words` | `counts`, `top_words` | `rare_words(text, max_count=1)`: stopwords out, A–Z | `unique_count` | `["bird", "dog"]` | stopwords kept, unsorted |

## C2g facts

Sessions 1 and 2 each carry a `given` block. After that session ends, the harness writes its task rows and handoff into the pack. For constraint and decision tasks, session 1's block also holds the rule or decision as a decisions.md line. For unfinished tasks, session 2's block lists (a) and (b) as done and (c) as todo with its full spec.
