"""R-014 scored projects L15-L17 (v3 form: 8 sessions, 12 facts)."""
from long_common import CHG, DEC, FINISH, RULE, g, later, mk

# ---------------------------------------------------------------- L15 hotel booking
mk("L15", {"min_two": "superseded", "weekend_25": "superseded", "stay_line": "superseded",
           "parse_dmy": "unfinished", "free_kind": "unfinished", "guest_sorted": "unfinished",
           "room_number": "constraint", "name_case": "constraint", "no_overlap": "decision",
           "lowest_room": "decision", "long_stay": "decision", "conf_header": "decision"},
   "Room bookings for a small hotel. Prices are int cents.",
   {"dates.py": '"""Date helpers."""\n', "hotel.py": '"""The hotel."""\n',
    "price.py": '"""Stay prices."""\n', "confirm.py": '"""Booking confirmations."""\n'},
   [f"""
    Add parse_date(s) to dates.py: an ISO date string such as "2026-06-05" becomes a datetime.date. Add tests.

    {later("parse_date", 'it also accepts day/month/year dates ("05/06/2026" is 5 June 2026).')}

    {RULE}room numbers are positive whole numbers: adding a room with another number, or with a number the hotel already has, raises ValueError.

    {DEC}a stay is at least 1 night: a booking whose end date is not after its start date raises ValueError.
    """,
    f"""
    Add a Hotel class to hotel.py: add_room(number, kind, price) adds a room of kind "single" or "double" with a nightly price in int cents, book(guest, kind, start, end) books a free room of that kind for the nights from start up to end (dates) and returns a booking id (1, 2, 3 and so on), and room_of(booking_id) returns the booked room number. When no room of that kind is free, book raises ValueError. Add tests.

    {RULE}guest names ignore case in every function: "Ann" and "ANN" are the same guest.

    {DEC}Friday and Saturday nights cost 20% more than the room's nightly price.

    {DEC}the stay line of a confirmation has the form Room 12, 3 nights.
    """,
    f"""
    Add Hotel.cancel(booking_id) to hotel.py. Add tests.

    {CHG}Friday and Saturday nights cost 25% more, not 20%.

    {DEC}two bookings of the same room may not overlap; a stay that ends on the day another starts does not overlap it.

    {DEC}book gives the free room of that kind with the lowest number.
    """,
    f"""
    Add Hotel.free_rooms(start, end) to hotel.py: the sorted numbers of the rooms that are free for all nights from start up to end. Add tests.

    {later("Hotel.free_rooms", "it takes an optional kind and then returns only rooms of that kind.")}

    {CHG}a stay is at least 2 nights: a booking of fewer nights raises ValueError.
    """,
    f"""
    Add Hotel.guest_bookings(name) to hotel.py: the booking ids of that guest, in the order they were booked. Add tests.

    {later("Hotel.guest_bookings", "the ids are sorted by the stay's start date instead.")}
    """,
    f"""
    Add Hotel.occupancy(day) to hotel.py: the number of rooms booked for the night that starts on that day. Add tests.

    {CHG}the stay line of a confirmation has the form 3 nights in room 12, not Room 12, 3 nights.

    {DEC}a stay of 7 nights or more gets 10% off its total price, rounded down to a whole cent.

    {DEC}the first line of a confirmation is the booking id, in the form Booking #1.
    """,
    """
    Add stay_price(hotel, booking_id) to price.py: the total price in cents (an int) of that booking's stay. Add tests.
    """,
    f"""
    Add write_confirmation(hotel, booking_id, path) to confirm.py: it writes a text confirmation with the booking id, the guest, the stay and the total price. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_date(s) with tests. Its last step is left for later: accept day/month/year dates.",
      [("parse_date", "done"), ("parse_date: accept dd/mm/yyyy", "todo")],
      ["Room numbers are positive whole numbers; another number or a duplicate raises ValueError.",
       "A stay is at least 1 night: an end date not after the start raises ValueError."]),
    g("Session 2 added Hotel.add_room, book and room_of with tests.", [("Hotel.add_room / book / room_of", "done")],
      ["Guest names ignore case in every function.",
       "Friday and Saturday nights cost 20% more than the nightly price.",
       "A confirmation stay line has the form Room 12, 3 nights."]),
    g("Session 3 added Hotel.cancel with tests.", [("Hotel.cancel", "done")],
      ["Supersedes 20%: Friday and Saturday nights cost 25% more.",
       "Bookings of the same room may not overlap; ending on the day another starts is not an overlap.",
       "book gives the free room of that kind with the lowest number."]),
    g("Session 4 added Hotel.free_rooms(start, end) with tests. Its last step is left for later: an optional kind.",
      [("Hotel.free_rooms", "done"), ("Hotel.free_rooms: optional kind", "todo")],
      ["Supersedes 1 night: a stay is at least 2 nights; fewer raises ValueError."]),
    g("Session 5 added Hotel.guest_bookings(name) with tests. Its last step is left for later: sort the ids by start date.",
      [("Hotel.guest_bookings", "done"), ("Hotel.guest_bookings: sort by start date", "todo")]),
    g("Session 6 added Hotel.occupancy(day) with tests.", [("Hotel.occupancy", "done")],
      ["Supersedes Room 12, 3 nights: a confirmation stay line has the form 3 nights in room 12.",
       "A stay of 7 nights or more gets 10% off its total, rounded down.",
       "The first confirmation line is Booking #1."]),
    g("Session 7 added stay_price(hotel, booking_id) with tests.", [("stay_price", "done")])],
   '''
   from datetime import date
   import pytest
   from dates import parse_date
   from hotel import Hotel
   from price import stay_price
   from confirm import write_confirmation


   def D(d):
       return date(2026, 6, d)


   def _h():
       h = Hotel()
       h.add_room(1, "single", 10000)
       h.add_room(2, "double", 15000)
       h.add_room(3, "double", 15000)
       return h


   def test_hotel_basic():
       h = _h()
       assert h.book("ann", "double", D(1), D(3)) == 1 and h.room_of(1) == 2
       assert h.free_rooms(D(1), D(3)) == [1, 3] and h.occupancy(D(2)) == 1 and h.occupancy(D(3)) == 0
       assert stay_price(h, 1) == 30000
       h.cancel(1)
       assert h.free_rooms(D(1), D(3)) == [1, 2, 3] and parse_date("2026-06-05") == D(5)


   def test_fact_min_two():
       h = _h()
       with pytest.raises(ValueError):
           h.book("ann", "single", D(1), D(2))
       assert h.free_rooms(D(1), D(2)) == [1, 2, 3]


   def test_stale_min_one():
       assert isinstance(_h().book("ann", "single", D(1), D(2)), int)


   def test_fact_weekend_25():
       h = _h()
       h.book("ann", "single", D(4), D(6))
       assert stay_price(h, 1) == 22500


   def test_stale_weekend_20():
       h = _h()
       h.book("ann", "single", D(4), D(6))
       assert stay_price(h, 1) == 22000


   def _conf(tmp_path):
       h = _h()
       h.book("ann", "double", D(1), D(4))
       p = tmp_path / "c.txt"
       write_confirmation(h, 1, str(p))
       return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def test_fact_stay_line(tmp_path):
       assert "3 nights in room 2" in _conf(tmp_path)


   def test_stale_room_first(tmp_path):
       assert "Room 2, 3 nights" in _conf(tmp_path)


   def test_fact_conf_header(tmp_path):
       assert _conf(tmp_path)[0] == "Booking #1"


   def test_fact_parse_dmy():
       assert parse_date("05/06/2026") == D(5) and parse_date("2026-06-05") == D(5)


   def test_fact_free_kind():
       h = _h()
       h.book("ann", "double", D(1), D(3))
       assert h.free_rooms(D(1), D(3), "double") == [3] and h.free_rooms(D(1), D(3), "single") == [1]


   def test_fact_guest_sorted():
       h = _h()
       h.book("ann", "single", D(10), D(12))
       h.book("ann", "double", D(1), D(3))
       assert h.guest_bookings("ann") == [2, 1]


   def test_fact_room_number():
       h = _h()
       for bad in (0, -4, 1):
           with pytest.raises(ValueError):
               h.add_room(bad, "single", 10000)
       assert h.free_rooms(D(1), D(3)) == [1, 2, 3]


   def test_fact_name_case():
       h = _h()
       h.book("Ann", "single", D(1), D(3))
       assert h.guest_bookings("ANN") == [1]


   def test_fact_no_overlap():
       h = Hotel()
       h.add_room(1, "single", 10000)
       h.book("ann", "single", D(1), D(3))
       with pytest.raises(ValueError):
           h.book("bo", "single", D(2), D(4))
       assert h.book("bo", "single", D(3), D(5)) == 2


   def test_fact_lowest_room():
       h = Hotel()
       for n in (5, 2, 9):
           h.add_room(n, "double", 15000)
       a = h.book("ann", "double", D(1), D(3))
       b = h.book("bo", "double", D(1), D(3))
       assert h.room_of(a) == 2 and h.room_of(b) == 5


   def test_fact_long_stay():
       h = Hotel()
       h.add_room(1, "single", 10000)
       h.add_room(2, "single", 10000)
       six = h.book("ann", "single", D(1), D(7))
       seven = h.book("bo", "single", D(1), D(8))
       assert stay_price(h, six) >= 60000
       assert stay_price(h, seven) == (stay_price(h, six) + 10000) * 90 // 100
   ''',
   {"dates.py": '''
    from datetime import date


    def parse_date(s):
        s = s.strip()
        if "/" in s:
            d, m, y = s.split("/")
            return date(int(y), int(m), int(d))
        return date.fromisoformat(s)
    ''',
    "hotel.py": '''
    class Hotel:
        def __init__(self):
            self.rooms = {}
            self.bookings = {}
            self.n = 0

        def add_room(self, number, kind, price):
            if not isinstance(number, int) or number <= 0 or number in self.rooms:
                raise ValueError("bad room number")
            self.rooms[number] = (kind, price)

        def _free(self, room, start, end):
            return all(not (s < end and start < e) for g, r, s, e in self.bookings.values() if r == room)

        def book(self, guest, kind, start, end):
            if (end - start).days < 2:
                raise ValueError("at least 2 nights")
            for num in sorted(self.rooms):
                if self.rooms[num][0] == kind and self._free(num, start, end):
                    self.n += 1
                    self.bookings[self.n] = (guest.lower(), num, start, end)
                    return self.n
            raise ValueError("no room free")

        def room_of(self, bid):
            return self.bookings[bid][1]

        def cancel(self, bid):
            del self.bookings[bid]

        def free_rooms(self, start, end, kind=None):
            return [n for n in sorted(self.rooms)
                    if (kind is None or self.rooms[n][0] == kind) and self._free(n, start, end)]

        def guest_bookings(self, name):
            return sorted((b for b, v in self.bookings.items() if v[0] == name.lower()),
                          key=lambda b: (self.bookings[b][2], b))

        def occupancy(self, day):
            return sum(1 for g, r, s, e in self.bookings.values() if s <= day < e)
    ''',
    "price.py": '''
    from datetime import timedelta


    def stay_price(hotel, bid):
        g, r, s, e = hotel.bookings[bid]
        price = hotel.rooms[r][1]
        total = 0
        d = s
        while d < e:
            total += (price + price * 25 // 100) if d.weekday() in (4, 5) else price
            d += timedelta(days=1)
        if (e - s).days >= 7:
            total = total * 90 // 100
        return total
    ''',
    "confirm.py": '''
    from price import stay_price


    def write_confirmation(hotel, bid, path):
        g, r, s, e = hotel.bookings[bid]
        with open(path, "w", encoding="utf8") as f:
            f.write(f"Booking #{bid}\\n")
            f.write(f"Guest: {g.title()}\\n")
            f.write(f"{(e - s).days} nights in room {r}\\n")
            f.write(f"Total: {stay_price(hotel, bid) / 100:.2f}\\n")
    '''})

# ---------------------------------------------------------------- L16 workout log
mk("L16", {"week_sunday": "superseded", "run_70": "superseded", "summary_line": "superseded",
           "duration_forms": "unfinished", "kinds_sorted": "unfinished", "rest_day": "unfinished",
           "minutes_range": "constraint", "kind_known": "constraint", "merge_same_day": "decision",
           "swim_minutes": "decision", "summary_order": "decision", "total_line": "decision"},
   "A small workout log.",
   {"units.py": '"""Unit parsing."""\n', "log.py": '"""The workout log."""\n',
    "stats.py": '"""Workout statistics."""\n', "summary.py": '"""Log summaries."""\n'},
   [f"""
    Add parse_duration(s) to units.py: a duration in minutes such as "30m" becomes an int (30). Add tests.

    {later("parse_duration", 'it also accepts hours and minutes ("1h15m") and clock form ("1:15"); both are 75.')}

    {RULE}a workout lasts a whole number of minutes from 1 to 300: any function given another duration raises ValueError.

    {DEC}running burns 60 calories per km.
    """,
    f"""
    Add a Log class to log.py: add(day, kind, minutes, km=0) records a workout on a datetime.date, entries(day) returns that day's workouts as (kind, minutes, km) tuples in the order they were added, and total(kind=None) returns the total minutes, of one kind or of all. Add tests.

    {RULE}the kinds are "run", "bike" and "swim"; kinds ignore case and are stored in lower case, and any other kind raises ValueError in any function.

    {DEC}weeks start on Monday.

    {DEC}each line of a summary has the form 2026-06-01 run 30m.
    """,
    f"""
    Add Log.days() to log.py: the sorted list of days with workouts. Add tests.

    {CHG}weeks start on Sunday, not Monday.

    {DEC}a second workout of the same kind on the same day is merged into the first: its minutes and km are added.

    {DEC}swimming burns 10 calories per minute, whatever the distance.
    """,
    f"""
    Add Log.kinds() to log.py: the kinds that have workouts, in the order they first appeared. Add tests.

    {later("Log.kinds", "they are sorted by total minutes, most first.")}

    {CHG}running burns 70 calories per km, not 60.
    """,
    f"""
    Add streak(log, today) to stats.py: the number of days in the unbroken run of workout days that ends today (0 when today has no workout). Add tests.

    {later("streak", "a single rest day between two workout days does not break the streak; the rest day itself is not counted.")}
    """,
    f"""
    Add week_total(log, day) to stats.py: the total minutes in the week that contains day. Add tests.

    {CHG}each line of a summary has the form 2026-06-01 Run: 30 min, not 2026-06-01 run 30m.

    {DEC}a summary lists the days newest first.

    {DEC}the last line of a summary is the total, in the form Total: 95 min.
    """,
    """
    Add calories(kind, minutes, km) to stats.py: the calories (an int) burned in one workout. Cycling burns 30 calories per km. Add tests.
    """,
    f"""
    Add write_summary(log, path) to summary.py: it writes a text summary with one line per workout and the total. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_duration(s) with tests. Its last step is left for later: accept 1h15m and 1:15.",
      [("parse_duration", "done"), ("parse_duration: accept 1h15m and 1:15", "todo")],
      ["A workout lasts a whole number of minutes from 1 to 300; another duration raises ValueError in any function.",
       "Running burns 60 calories per km."]),
    g("Session 2 added Log.add, entries and total with tests.", [("Log.add / entries / total", "done")],
      ["Kinds are run, bike, swim; they ignore case, are stored lower case, and any other kind raises ValueError.",
       "Weeks start on Monday.",
       "A summary line has the form 2026-06-01 run 30m."]),
    g("Session 3 added Log.days() with tests.", [("Log.days", "done")],
      ["Supersedes Monday: weeks start on Sunday.",
       "A second workout of the same kind on the same day is merged: minutes and km are added.",
       "Swimming burns 10 calories per minute, whatever the distance."]),
    g("Session 4 added Log.kinds() with tests. Its last step is left for later: sort by total minutes, most first.",
      [("Log.kinds", "done"), ("Log.kinds: sort by total minutes", "todo")],
      ["Supersedes 60: running burns 70 calories per km."]),
    g("Session 5 added streak(log, today) with tests. Its last step is left for later: a single rest day does not break the streak and is not counted.",
      [("streak", "done"), ("streak: single rest day allowed", "todo")]),
    g("Session 6 added week_total(log, day) with tests.", [("week_total", "done")],
      ["Supersedes 2026-06-01 run 30m: a summary line has the form 2026-06-01 Run: 30 min.",
       "A summary lists the days newest first.",
       "The last summary line is the total: Total: 95 min."]),
    g("Session 7 added calories(kind, minutes, km) with tests; cycling is 30 calories per km.", [("calories", "done")])],
   '''
   import re
   from datetime import date
   import pytest
   from units import parse_duration
   from log import Log
   from stats import calories, streak, week_total
   from summary import write_summary


   def D(d):
       return date(2026, 6, d)


   def test_log_basic():
       l = Log()
       l.add(D(1), "run", 30, 5)
       l.add(D(2), "bike", 60, 20)
       assert l.entries(D(1)) == [("run", 30, 5)] and l.total() == 90 and l.total("bike") == 60
       assert l.days() == [D(1), D(2)] and sorted(l.kinds()) == ["bike", "run"]
       assert parse_duration("30m") == 30 and calories("bike", 60, 20) == 600
       assert streak(l, D(2)) == 2 and week_total(l, D(2)) == 90


   def test_fact_week_sunday():
       l = Log()
       l.add(D(6), "run", 40)
       l.add(D(7), "run", 30)
       assert week_total(l, D(7)) == 30 and week_total(l, D(6)) == 40


   def test_stale_week_monday():
       l = Log()
       l.add(D(6), "run", 40)
       l.add(D(7), "run", 30)
       assert week_total(l, D(7)) == 70


   def test_fact_run_70():
       assert calories("run", 30, 5) == 350


   def test_stale_run_60():
       assert calories("run", 30, 5) == 300


   def _sum(tmp_path, l):
       p = tmp_path / "s.txt"
       write_summary(l, str(p))
       return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def test_fact_summary_line(tmp_path):
       l = Log()
       l.add(D(1), "run", 30, 5)
       assert "2026-06-01 Run: 30 min" in _sum(tmp_path, l)


   def test_stale_summary_short(tmp_path):
       l = Log()
       l.add(D(1), "run", 30, 5)
       assert "2026-06-01 run 30m" in _sum(tmp_path, l)


   def test_fact_summary_order(tmp_path):
       l = Log()
       l.add(D(1), "run", 30, 5)
       l.add(D(3), "bike", 40, 10)
       l.add(D(2), "swim", 20, 1)
       found = [re.search(r"\\d{4}-\\d\\d-\\d\\d", x) for x in _sum(tmp_path, l)]
       assert [m.group() for m in found if m] == ["2026-06-03", "2026-06-02", "2026-06-01"]


   def test_fact_total_line(tmp_path):
       l = Log()
       l.add(D(1), "run", 30, 5)
       l.add(D(2), "bike", 65, 20)
       assert re.fullmatch(r"Total: 95 min", _sum(tmp_path, l)[-1])


   def test_fact_duration_forms():
       assert parse_duration("1h15m") == 75 and parse_duration("1:15") == 75 and parse_duration("30m") == 30


   def test_fact_kinds_sorted():
       l = Log()
       l.add(D(1), "run", 30)
       l.add(D(2), "bike", 60)
       l.add(D(3), "swim", 20)
       l.add(D(4), "run", 10)
       assert l.kinds() == ["bike", "run", "swim"]


   def test_fact_rest_day():
       l = Log()
       for d in (1, 2, 4, 5):
           l.add(D(d), "run", 30)
       assert streak(l, D(5)) == 4
       l2 = Log()
       for d in (1, 4, 5):
           l2.add(D(d), "run", 30)
       assert streak(l2, D(5)) == 2


   def test_fact_minutes_range():
       l = Log()
       for bad in (0, 301):
           with pytest.raises(ValueError):
               l.add(D(1), "run", bad)
       with pytest.raises(ValueError):
           calories("swim", 0, 0)
       assert l.days() == []


   def test_fact_kind_known():
       l = Log()
       l.add(D(1), "Run", 30, 5)
       assert l.entries(D(1)) == [("run", 30, 5)]
       with pytest.raises(ValueError):
           l.add(D(1), "yoga", 30)
       with pytest.raises(ValueError):
           calories("rowing", 30, 0)


   def test_fact_merge_same_day():
       l = Log()
       l.add(D(1), "run", 30, 5)
       l.add(D(1), "run", 20, 3)
       assert l.entries(D(1)) == [("run", 50, 8)]


   def test_fact_swim_minutes():
       assert calories("swim", 30, 1) == 300 and calories("swim", 30, 2) == 300
   ''',
   {"units.py": '''
    import re


    def parse_duration(s):
        s = s.strip().lower()
        if ":" in s:
            h, m = s.split(":")
            v = int(h) * 60 + int(m)
        else:
            m = re.fullmatch(r"(?:(\\d+)h)?(?:(\\d+)m)?", s)
            if not s or not m:
                raise ValueError("bad duration")
            v = int(m.group(1) or 0) * 60 + int(m.group(2) or 0)
        if not 1 <= v <= 300:
            raise ValueError("bad duration")
        return v
    ''',
    "log.py": '''
    KINDS = ("run", "bike", "swim")


    def check_minutes(m):
        if not isinstance(m, int) or not 1 <= m <= 300:
            raise ValueError("bad duration")


    def check_kind(kind):
        k = kind.strip().lower()
        if k not in KINDS:
            raise ValueError("unknown kind")
        return k


    class Log:
        def __init__(self):
            self.data = {}

        def add(self, day, kind, minutes, km=0):
            k = check_kind(kind)
            check_minutes(minutes)
            e = self.data.setdefault(day, {}).setdefault(k, [0, 0])
            e[0] += minutes
            e[1] += km

        def entries(self, day):
            return [(k, m, km) for k, (m, km) in self.data.get(day, {}).items()]

        def total(self, kind=None):
            return sum(m for d in self.data.values() for k, (m, km) in d.items() if kind is None or k == kind)

        def days(self):
            return sorted(self.data)

        def kinds(self):
            t = {}
            for d in self.data.values():
                for k, (m, km) in d.items():
                    t[k] = t.get(k, 0) + m
            return sorted(t, key=lambda k: -t[k])
    ''',
    "stats.py": '''
    from datetime import timedelta
    from log import check_kind, check_minutes


    def streak(log, today):
        days = set(log.days())
        n = gap = 0
        d = today
        while True:
            if d in days:
                n += 1
                gap = 0
            else:
                gap += 1
                if gap > 1 or n == 0:
                    break
            d -= timedelta(days=1)
        return n


    def week_total(log, day):
        start = day - timedelta(days=(day.weekday() + 1) % 7)
        return sum(m for i in range(7) for k, m, km in log.entries(start + timedelta(days=i)))


    def calories(kind, minutes, km):
        k = check_kind(kind)
        check_minutes(minutes)
        return {"run": 70 * km, "bike": 30 * km, "swim": 10 * minutes}[k]
    ''',
    "summary.py": '''
    def write_summary(log, path):
        with open(path, "w", encoding="utf8") as f:
            for d in reversed(log.days()):
                for k, m, km in log.entries(d):
                    f.write(f"{d.isoformat()} {k.title()}: {m} min\\n")
            f.write(f"Total: {log.total()} min\\n")
    '''})

# ---------------------------------------------------------------- L17 quiz scoring
mk("L17", {"wrong_2": "superseded", "pass_60": "superseded", "result_line": "superseded",
           "parse_forms": "unfinished", "ranking_ties": "unfinished", "half_up": "unfinished",
           "answer_letters": "constraint", "once_only": "constraint", "unanswered_wrong": "decision",
           "floor_zero": "decision", "results_order": "decision", "results_header": "decision"},
   "Scoring for a small multiple-choice quiz.",
   {"questions.py": '"""Question helpers."""\n', "quiz.py": '"""The quiz."""\n',
    "grading.py": '"""Grades."""\n', "results.py": '"""Results files."""\n'},
   [f"""
    Add parse_answer(s) to questions.py: an answer letter such as "b" becomes upper case ("B"). Add tests.

    {later("parse_answer", 'it also accepts a number from 1 to 4 ("2" is "B") and a letter in brackets ("(c)" is "C").')}

    {RULE}answers are the letters A to D: any function given another answer raises ValueError.

    {DEC}a wrong answer costs 1 point.
    """,
    f"""
    Add a Quiz class to quiz.py: Quiz(title), add_question(text, correct) adds a question with its correct letter and returns its number (1, 2, 3 and so on), answer(name, number, letter) records a player's answer, and score(name) returns the player's points: 4 for each correct answer. Add tests.

    {RULE}a player answers each question at most once: a second answer to the same question raises ValueError and keeps the first.

    {DEC}the pass mark is 50%.

    {DEC}each line of a results file has the form ann 75%.
    """,
    f"""
    Add Quiz.percent(name) to quiz.py: the player's score as a percent of the maximum (4 points per question). Add tests.

    {CHG}the pass mark is 60%, not 50%.

    {DEC}a question the player did not answer counts as a wrong answer.

    {DEC}a negative score counts as 0%.
    """,
    f"""
    Add Quiz.ranking() to quiz.py: the player names, highest score first. Add tests.

    {later("Quiz.ranking", "players with the same score are sorted by name.")}

    {CHG}a wrong answer costs 2 points, not 1.
    """,
    f"""
    Add grade(percent) to grading.py: "A" from 90%, "B" from 75%, "C" from the pass mark, and "F" below the pass mark. Add tests.

    {later("grade", "the percent is first rounded half up to a whole number (89.5 is an A).")}
    """,
    f"""
    Add Quiz.players() to quiz.py: the sorted player names. Add tests.

    {CHG}each line of a results file has the form 75% - ann, not ann 75%.

    {DEC}a results file lists the players by name.

    {DEC}the first line of a results file is the title and question count, in the form Quiz: Capitals (4 questions).
    """,
    """
    Add Quiz.passed(name) to quiz.py: True when the player's percent reaches the pass mark. Add tests.
    """,
    f"""
    Add write_results(quiz, path) to results.py: it writes a text results file with one line per player. Add tests. {FINISH}
    """],
   [g("Session 1 added parse_answer(s) with tests. Its last step is left for later: accept 1-4 and a letter in brackets.",
      [("parse_answer", "done"), ("parse_answer: accept 1-4 and (c)", "todo")],
      ["Answers are the letters A to D; another answer raises ValueError in any function.",
       "A wrong answer costs 1 point."]),
    g("Session 2 added Quiz, add_question, answer and score with tests; a correct answer is 4 points.",
      [("Quiz / add_question / answer / score", "done")],
      ["A player answers each question at most once; a second answer raises ValueError and keeps the first.",
       "The pass mark is 50%.",
       "A results line has the form ann 75%."]),
    g("Session 3 added Quiz.percent(name) with tests.", [("Quiz.percent", "done")],
      ["Supersedes 50%: the pass mark is 60%.",
       "An unanswered question counts as a wrong answer.",
       "A negative score counts as 0%."]),
    g("Session 4 added Quiz.ranking() with tests. Its last step is left for later: ties sorted by name.",
      [("Quiz.ranking", "done"), ("Quiz.ranking: ties by name", "todo")],
      ["Supersedes 1 point: a wrong answer costs 2 points."]),
    g("Session 5 added grade(percent) with tests. Its last step is left for later: round the percent half up first.",
      [("grade", "done"), ("grade: round half up first", "todo")]),
    g("Session 6 added Quiz.players() with tests.", [("Quiz.players", "done")],
      ["Supersedes ann 75%: a results line has the form 75% - ann.",
       "A results file lists the players by name.",
       "The first results line is Quiz: Capitals (4 questions)."]),
    g("Session 7 added Quiz.passed(name) with tests.", [("Quiz.passed", "done")])],
   '''
   import re
   import pytest
   from questions import parse_answer
   from quiz import Quiz
   from grading import grade
   from results import write_results


   def _q():
       q = Quiz("Capitals")
       for t, c in (("Paris?", "A"), ("Rome?", "B"), ("Oslo?", "C"), ("Bern?", "D")):
           q.add_question(t, c)
       return q


   def _play(q, name, letters):
       for i, l in enumerate(letters, 1):
           q.answer(name, i, l)


   def test_quiz_basic():
       q = _q()
       _play(q, "ann", "ABCD")
       assert q.score("ann") == 16 and q.percent("ann") == 100 and q.passed("ann")
       assert q.players() == ["ann"] and q.ranking() == ["ann"]
       assert grade(95) == "A" and parse_answer("b") == "B"


   def test_fact_wrong_2():
       q = _q()
       _play(q, "ann", "AACD")
       assert q.score("ann") == 10


   def test_stale_wrong_1():
       q = _q()
       _play(q, "ann", "AACD")
       assert q.score("ann") == 11


   def test_fact_pass_60():
       assert grade(55) == "F" and grade(65) == "C"


   def test_stale_pass_50():
       assert grade(55) == "C"


   def _res(tmp_path, q):
       p = tmp_path / "r.txt"
       write_results(q, str(p))
       return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


   def test_fact_result_line(tmp_path):
       q = _q()
       _play(q, "ann", "ABCD")
       assert "100% - ann" in _res(tmp_path, q)


   def test_stale_name_first(tmp_path):
       q = _q()
       _play(q, "ann", "ABCD")
       assert "ann 100%" in _res(tmp_path, q)


   def test_fact_results_order(tmp_path):
       q = _q()
       for n in ("cy", "ann", "bo"):
           _play(q, n, "ABCD")
       found = [re.search(r"\\b(ann|bo|cy)\\b", x) for x in _res(tmp_path, q)]
       assert [m.group(1) for m in found if m] == ["ann", "bo", "cy"]


   def test_fact_results_header(tmp_path):
       q = _q()
       _play(q, "ann", "ABCD")
       assert _res(tmp_path, q)[0] == "Quiz: Capitals (4 questions)"


   def test_fact_parse_forms():
       assert parse_answer("2") == "B" and parse_answer("(c)") == "C" and parse_answer("d") == "D"


   def test_fact_ranking_ties():
       q = _q()
       _play(q, "cy", "ABCD")
       _play(q, "bo", "AACD")
       _play(q, "ann", "ABCD")
       assert q.ranking() == ["ann", "cy", "bo"]


   def test_fact_half_up():
       assert grade(89.5) == "A" and grade(74.5) == "B" and grade(74.4) == "C"


   def test_fact_answer_letters():
       q = _q()
       with pytest.raises(ValueError):
           q.answer("ann", 1, "E")
       with pytest.raises(ValueError):
           parse_answer("e")
       with pytest.raises(ValueError):
           q.add_question("Lima?", "Z")
       assert q.players() == []


   def test_fact_once_only():
       q = _q()
       _play(q, "ann", ["B"])
       with pytest.raises(ValueError):
           q.answer("ann", 1, "A")
       _play(q, "bo", ["B"])
       assert q.score("ann") == q.score("bo")


   def test_fact_unanswered_wrong():
       q = _q()
       _play(q, "ann", "ADAB")
       _play(q, "bo", ["A"])
       assert q.score("ann") == q.score("bo")


   def test_fact_floor_zero():
       q = _q()
       _play(q, "bo", ["B"])
       assert q.score("bo") < 0 and q.percent("bo") == 0
   ''',
   {"questions.py": '''
    def parse_answer(s):
        s = s.strip().strip("()").upper()
        if s in ("1", "2", "3", "4"):
            s = "ABCD"[int(s) - 1]
        if s not in ("A", "B", "C", "D"):
            raise ValueError("answer must be A-D")
        return s
    ''',
    "grading.py": '''
    from decimal import Decimal, ROUND_HALF_UP


    def grade(percent):
        p = int(Decimal(str(percent)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        return "A" if p >= 90 else "B" if p >= 75 else "C" if p >= 60 else "F"
    ''',
    "quiz.py": '''
    from questions import parse_answer
    from grading import grade


    class Quiz:
        def __init__(self, title):
            self.title = title
            self.qs = []
            self.ans = {}

        def add_question(self, text, correct):
            self.qs.append(parse_answer(correct))
            return len(self.qs)

        def answer(self, name, number, letter):
            l = parse_answer(letter)
            a = self.ans.setdefault(name, {})
            if number in a:
                raise ValueError("already answered")
            a[number] = l

        def score(self, name):
            a = self.ans[name]
            r = sum(1 for i, c in enumerate(self.qs, 1) if a.get(i) == c)
            return 4 * r - 2 * (len(self.qs) - r)

        def percent(self, name):
            return max(0, self.score(name)) * 100 / (4 * len(self.qs))

        def ranking(self):
            return sorted(self.ans, key=lambda n: (-self.score(n), n))

        def players(self):
            return sorted(self.ans)

        def passed(self, name):
            return grade(self.percent(name)) != "F"
    ''',
    "results.py": '''
    def write_results(quiz, path):
        with open(path, "w", encoding="utf8") as f:
            f.write(f"Quiz: {quiz.title} ({len(quiz.qs)} questions)\\n")
            for n in quiz.players():
                f.write(f"{round(quiz.percent(n))}% - {n}\\n")
    '''})
