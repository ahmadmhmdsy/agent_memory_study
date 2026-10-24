"""R-015 advanced projects A03-A16 (confirm stage): 20+ sessions and 13-15 facts each, facts
superseded 1-3 times (2-4 values) with a stale test per old value, and deferred steps that the
last session finishes. Same style as r015_advanced.py (A01-A02), which stays frozen.

Test conventions, after the R-015 task audit (check_facts.py): every fact test checks only what
some prompt states, test_basic uses no fact value, and a fact test is kept apart from the other
facts where it can be (it compares two results, or uses inputs every value of another fact
accepts). Run: python r015_advanced2.py; then check_long.py and check_facts.py on A03-A16."""
from r015_common import CHG, DEC, FINISH, RULE, later, mk

# ---------------------------------------------------------------- A03 car rental (21 sessions)
mk("A03", {"day_rate": "superseded", "free_km": "superseded", "young_surcharge": "superseded",
           "min_age": "superseded", "delimiter": "superseded",
           "plate_groups": "unfinished", "receipt_km": "unfinished", "export_order": "unfinished",
           "no_overlap": "constraint", "km_positive": "constraint", "car_class": "constraint",
           "km_fee": "decision", "week_free": "decision", "export_header": "decision"},
   "Cars, rentals and charges for a small car rental firm. Money is in cents (ints); days are datetime.date; distances are whole km. A rental from its pickup day to its return day covers the days from pickup up to the day before return, so its length in days is return minus pickup.",
   {"fleet.py": '"""The cars."""\n', "rentals.py": '"""Rentals."""\n', "charges.py": '"""Rental charges."""\n',
    "export.py": '"""CSV export."""\n', "report.py": '"""Reports."""\n'},
   [f"""
    Add a Fleet class to fleet.py with add(plate, car_class), which adds a car, and car_class(plate), which returns the class of a car; an unknown plate raises KeyError. Add tests.

    {RULE}a car class is one of "economy", "compact" or "van"; any other class raises ValueError and adds nothing.

    {DEC}a rental costs 4000 cents per day.
    """,
    f"""
    Add Fleet.plates(): the sorted list of plates. Add tests.

    {later("Fleet.plates", "the plates are grouped by class: economy cars first, then compact, then van, and sorted by plate within each group.")}

    {DEC}each rental includes 200 free km per rental day; every km driven above that free allowance costs 30 cents.
    """,
    f"""
    Add a Rentals class to rentals.py. Rentals(fleet) works on a Fleet, kept as its attribute fleet. book(plate, driver, age, pickup, ret) books the car for a driver of the given age (an int) and returns a rental id: an int counter that starts at 1. An unknown plate raises KeyError, and a return day that is not after the pickup day raises ValueError; either way nothing is booked. Add tests.

    {RULE}a car is never rented twice for the same day: a booking that overlaps another rental of the same car raises ValueError and books nothing.
    """,
    f"""
    Add Rentals.get(rid), which returns the rental as a tuple (plate, driver, age, pickup, ret); an unknown id raises KeyError. Add tests.

    {RULE}a driver must be at least 21 years old; a younger driver raises ValueError and books nothing.
    """,
    f"""
    Add days(rentals, rid) to charges.py, the length of the rental in days, and price(rentals, rid), the day charge of the rental in cents. Add tests.

    {DEC}in a rental of 7 days or more every 7th day is free, so a 7-day rental pays for 6 days and a 14-day rental pays for 12 days.
    """,
    f"""
    Add Rentals.finish(rid, km), which records the km driven in the rental, and Rentals.km(rid), the km recorded for it (0 before finish). Add tests.

    {RULE}km driven is 0 or more; a negative km raises ValueError and changes nothing.
    """,
    f"""
    Add km_charge(rentals, rid) to charges.py: the charge for the km driven above the free allowance, in cents. Add tests.

    {CHG}each rental includes 150 free km per rental day, not 200.
    """,
    f"""
    Add total(rentals, rid) to charges.py: price(rentals, rid) plus km_charge(rentals, rid). Add tests.

    {DEC}drivers under 25 pay 10% more on the day charge: price is 10% higher for them, rounded to the nearest cent.
    """,
    f"""
    Add Rentals.of_driver(driver): the ids of the rentals of driver, in id order. Add tests.

    {CHG}a rental costs 4500 cents per day, not 4000.
    """,
    f"""
    Add export_rentals(rentals, path) to export.py: a CSV file with one row per rental in id order (id, plate, driver, pickup, ret), with ISO dates. Add tests.

    {later("export_rentals", "the rows are sorted by plate, and by id for the same plate.")}

    {DEC}an exported rentals file starts with a header line with the column names id, plate, driver, out, back, in that order, and uses "," as the delimiter.
    """,
    f"""
    Add receipt(rentals, rid) to charges.py: a list of text lines for the rental: first "days: <N>", the rental length (for example "days: 2"), then "total: <cents>", where <cents> is total(rentals, rid). Add tests.

    {later("receipt", 'between those two lines it has the line "extra km: <K>", where <K> is the number of km driven above the free allowance (for example "extra km: 0" when there are none).')}

    {CHG}drivers under 25 pay 15% more on the day charge, not 10%.
    """,
    f"""
    Add Rentals.cancel(rid), which removes the rental; an unknown id raises KeyError. Add tests.

    {CHG}a driver must be at least 23 years old, not 21.
    """,
    f"""
    Add Rentals.on_road(day): the sorted list of plates of the cars rented for day. Add tests.

    {CHG}exported files use ";" as the delimiter, not ",".
    """,
    """
    Add revenue(rentals) to report.py: the sum of total(rentals, rid) over all rentals. Add tests.
    """,
    f"""
    Add Rentals.is_free(plate, day): False when a rental of the car covers day, else True. Add tests.

    {CHG}each rental includes 250 free km per rental day, not 150.
    """,
    """
    Add Fleet.remove(plate), which removes a car; an unknown plate raises KeyError. Add tests.
    """,
    f"""
    Add Rentals.days_rented(plate): the total number of days over all rentals of the car. Add tests.

    {CHG}a rental costs 4200 cents per day, not 4500.
    """,
    f"""
    Add Rentals.extend(rid, ret), which moves the return day of a rental; the booking rules still apply, and a broken rule raises ValueError and changes nothing. Add tests.

    {CHG}drivers under 25 pay 12% more on the day charge, not 15%.
    """,
    f"""
    Add busiest_car(rentals) to report.py: the plate with the most days rented, the smallest plate on a tie, or None when there are no rentals. Add tests.

    {CHG}exported files use "|" as the delimiter, not ";".
    """,
    f"""
    Add Rentals.drivers(): the sorted list of distinct driver names. Add tests.

    {CHG}each rental includes 100 free km per rental day, not 250.
    """,
    f"""
    Add Rentals.ids(): all rental ids in order. Add tests. {FINISH}
    """],
   '''
    import datetime as dt
    import re
    import pytest
    from fleet import Fleet
    from rentals import Rentals
    from charges import days, price, km_charge, total, receipt
    from export import export_rentals

    D = dt.date
    MON = D(2026, 1, 5)


    def _r():
        f = Fleet()
        f.add("AA1", "economy")
        f.add("BB2", "van")
        return Rentals(f)


    def _book(r, n, age=30, plate="AA1", start=MON):
        return r.book(plate, "Ann", age, start, start + dt.timedelta(n))


    def test_basic():
        r = _r()
        assert r.fleet.car_class("BB2") == "van"
        i = _book(r, 3)
        assert i == 1 and r.get(i) == ("AA1", "Ann", 30, MON, D(2026, 1, 8)) and days(r, i) == 3
        with pytest.raises(KeyError):
            r.get(99)
        with pytest.raises(KeyError):
            _book(r, 1, plate="ZZ9")


    def _price(n, age=30):
        r = _r()
        return price(r, _book(r, n, age))


    def test_fact_day_rate():
        assert _price(1) == 4200


    def test_stale_rate_4500():
        assert _price(1) == 4500


    def test_stale_rate_4000():
        assert _price(1) == 4000


    def test_fact_week_free():
        p = _price(1)
        assert _price(6) == 6 * p and _price(7) == 6 * p and _price(14) == 12 * p


    def _young():
        return _price(1, 24), _price(1, 25), _price(1)


    def test_fact_young_surcharge():
        y, at25, p = _young()
        assert at25 == p and y == round(p * 112 / 100)


    def test_stale_young_15():
        y, _, p = _young()
        assert y == round(p * 115 / 100)


    def test_stale_young_10():
        y, _, p = _young()
        assert y == round(p * 110 / 100)


    def _age_ok(age):
        try:
            _book(_r(), 1, age)
            return True
        except ValueError:
            return False


    def test_fact_min_age():
        assert _age_ok(23) and not _age_ok(22)


    def test_stale_age_21():
        assert _age_ok(22)


    def _kc(km, n=2):
        r = _r()
        i = _book(r, n)
        r.finish(i, km)
        return km_charge(r, i)


    def test_fact_free_km():
        assert _kc(200) == 0 and _kc(201) > 0


    def test_stale_free_250():
        assert _kc(500) == 0


    def test_stale_free_150():
        assert _kc(300) == 0


    def test_stale_free_200():
        assert _kc(400) == 0


    def test_fact_km_fee():
        assert _kc(2010) - _kc(2000) == 300


    def test_fact_km_positive():
        r = _r()
        i = _book(r, 2)
        with pytest.raises(ValueError):
            r.finish(i, -1)
        assert r.km(i) == 0


    def test_fact_receipt_km():
        r = _r()
        i = _book(r, 2)
        r.finish(i, 0)
        assert [x.strip() for x in receipt(r, i)] == ["days: 2", "extra km: 0", f"total: {total(r, i)}"]
        j = _book(r, 1, plate="BB2")
        r.finish(j, 5000)
        assert re.fullmatch(r"extra km: [1-9][0-9]*", receipt(r, j)[1].strip())


    def _rows(r, tmp_path):
        p = tmp_path / "r.csv"
        export_rentals(r, str(p))
        return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        r = _r()
        _book(r, 1)
        assert re.split(r"[,;|]", _rows(r, tmp_path)[0]) == ["id", "plate", "driver", "out", "back"]


    def _row(tmp_path, plate, driver):
        r = _r()
        r.book(plate, driver, 30, MON, MON + dt.timedelta(1))
        return _rows(r, tmp_path)[1]


    def test_fact_delimiter(tmp_path):
        assert _row(tmp_path, "AA1", "Ann").split("|") == ["1", "AA1", "Ann", "2026-01-05", "2026-01-06"]


    def test_stale_delim_semicolon(tmp_path):
        assert _row(tmp_path, "AA1", "Ann").split(";") == ["1", "AA1", "Ann", "2026-01-05", "2026-01-06"]


    def test_stale_delim_comma(tmp_path):
        assert _row(tmp_path, "AA1", "Ann").split(",") == ["1", "AA1", "Ann", "2026-01-05", "2026-01-06"]


    def test_fact_export_order(tmp_path):
        r = _r()
        _book(r, 1, plate="BB2")
        _book(r, 1, plate="AA1")
        _book(r, 1, plate="AA1", start=D(2026, 1, 9))
        assert [re.split(r"[,;|]", x)[0] for x in _rows(r, tmp_path)[1:]] == ["2", "3", "1"]


    def test_fact_plate_groups():
        f = Fleet()
        f.add("AA9", "van")
        f.add("ZZ1", "economy")
        f.add("MM5", "compact")
        f.add("BB2", "economy")
        assert f.plates() == ["BB2", "ZZ1", "MM5", "AA9"]


    def test_fact_no_overlap():
        r = _r()
        _book(r, 3)
        with pytest.raises(ValueError):
            _book(r, 2, start=D(2026, 1, 7))
        assert r.is_free("AA1", D(2026, 1, 8)) and _book(r, 2, plate="BB2", start=D(2026, 1, 7)) == 2


    def test_fact_car_class():
        f = Fleet()
        with pytest.raises(ValueError):
            f.add("XX1", "truck")
        with pytest.raises(KeyError):
            f.car_class("XX1")
        assert f.plates() == []
    ''',
   {"fleet.py": '''
    """The cars."""

    CLASSES = ("economy", "compact", "van")


    class Fleet:
        def __init__(self):
            self._c = {}

        def add(self, plate, car_class):
            if car_class not in CLASSES:
                raise ValueError(f"bad class {car_class!r}")
            self._c[plate] = car_class

        def car_class(self, plate):
            return self._c[plate]

        def plates(self):
            return sorted(self._c, key=lambda p: (CLASSES.index(self._c[p]), p))

        def remove(self, plate):
            del self._c[plate]
    ''',
    "rentals.py": '''
    """Rentals."""

    MIN_AGE = 23


    class Rentals:
        def __init__(self, fleet):
            self.fleet = fleet
            self._r = {}
            self._km = {}
            self._n = 0

        def _check(self, plate, age, pickup, ret, skip=None):
            self.fleet.car_class(plate)
            if age < MIN_AGE:
                raise ValueError("driver too young")
            if ret <= pickup:
                raise ValueError("return must be after pickup")
            for k, (p, _, _, a, b) in self._r.items():
                if k != skip and p == plate and pickup < b and a < ret:
                    raise ValueError("car already rented")

        def book(self, plate, driver, age, pickup, ret):
            self._check(plate, age, pickup, ret)
            self._n += 1
            self._r[self._n] = (plate, driver, age, pickup, ret)
            return self._n

        def get(self, rid):
            return self._r[rid]

        def ids(self):
            return list(self._r)

        def finish(self, rid, km):
            self._r[rid]
            if km < 0:
                raise ValueError("km must be 0 or more")
            self._km[rid] = km

        def km(self, rid):
            self._r[rid]
            return self._km.get(rid, 0)

        def of_driver(self, driver):
            return [k for k, v in self._r.items() if v[1] == driver]

        def cancel(self, rid):
            del self._r[rid]
            self._km.pop(rid, None)

        def on_road(self, day):
            return sorted(p for p, _, _, a, b in self._r.values() if a <= day < b)

        def is_free(self, plate, day):
            return plate not in self.on_road(day)

        def days_rented(self, plate):
            return sum((b - a).days for p, _, _, a, b in self._r.values() if p == plate)

        def extend(self, rid, ret):
            p, d, age, a, _ = self._r[rid]
            self._check(p, age, a, ret, skip=rid)
            self._r[rid] = (p, d, age, a, ret)

        def drivers(self):
            return sorted({v[1] for v in self._r.values()})
    ''',
    "charges.py": '''
    """Rental charges."""

    RATE = 4200
    FREE_KM = 100
    KM_FEE = 30
    YOUNG = 12


    def days(rentals, rid):
        _, _, _, a, b = rentals.get(rid)
        return (b - a).days


    def price(rentals, rid):
        n = days(rentals, rid)
        p = (n - n // 7) * RATE
        if rentals.get(rid)[2] < 25:
            p = round(p * (100 + YOUNG) / 100)
        return p


    def extra_km(rentals, rid):
        return max(0, rentals.km(rid) - FREE_KM * days(rentals, rid))


    def km_charge(rentals, rid):
        return extra_km(rentals, rid) * KM_FEE


    def total(rentals, rid):
        return price(rentals, rid) + km_charge(rentals, rid)


    def receipt(rentals, rid):
        return [f"days: {days(rentals, rid)}", f"extra km: {extra_km(rentals, rid)}", f"total: {total(rentals, rid)}"]
    ''',
    "export.py": '''
    """CSV export."""
    import csv

    DELIM = "|"


    def export_rentals(rentals, path):
        ids = sorted(rentals.ids(), key=lambda i: (rentals.get(i)[0], i))
        with open(path, "w", newline="") as f:
            w = csv.writer(f, delimiter=DELIM)
            w.writerow(["id", "plate", "driver", "out", "back"])
            for i in ids:
                p, d, _, a, b = rentals.get(i)
                w.writerow([i, p, d, a.isoformat(), b.isoformat()])
    ''',
    "report.py": '''
    """Reports."""
    from collections import Counter

    from charges import days, total


    def revenue(rentals):
        return sum(total(rentals, i) for i in rentals.ids())


    def busiest_car(rentals):
        c = Counter()
        for i in rentals.ids():
            c[rentals.get(i)[0]] += days(rentals, i)
        return min(c, key=lambda p: (-c[p], p)) if c else None
    '''}, "advanced")

# ---------------------------------------------------------------- A04 dental clinic (21 sessions)
mk("A04", {"slot_len": "superseded", "last_start": "superseded", "filling_fee": "superseded",
           "kid_age": "superseded", "no_show_fee": "superseded",
           "name_spaces": "unfinished", "agenda_kind": "unfinished", "export_hhmm": "unfinished",
           "no_overlap": "constraint", "kind_valid": "constraint", "open_8": "constraint", "name_required": "constraint",
           "kid_noshow": "decision", "export_header": "decision"},
   "Patients, appointments and fees for a small dental clinic with one chair. Money is in cents (ints); days are datetime.date; times are int minutes after midnight (9:30 is 570).",
   {"patients.py": '"""Patients."""\n', "schedule.py": '"""Appointments."""\n', "fees.py": '"""Fees and bills."""\n',
    "export.py": '"""Agenda and CSV export."""\n'},
   [f"""
    Add a Patients class to patients.py with register(name, age), which registers a patient and returns a patient id (an int counter that starts at 1), name(pid) and age(pid); an unknown id raises KeyError. Add tests.

    {later("Patients.register", 'runs of spaces inside a name are collapsed to one space, so "Ann   Lee" is stored as "Ann Lee".')}

    {RULE}a patient name that is empty or only spaces raises ValueError and registers nothing; names are stored without surrounding spaces.
    """,
    f"""
    Add a Schedule class to schedule.py. Schedule(patients) works on a Patients, kept as its attribute patients. book(pid, day, start, kind) books an appointment and returns an appointment id: an int counter that starts at 1. An unknown patient raises KeyError and books nothing. Add tests.

    {RULE}an appointment kind is one of "checkup", "filling" or "cleaning"; any other kind raises ValueError and books nothing.

    {DEC}every appointment lasts 30 minutes.
    """,
    f"""
    Add Schedule.get(aid), which returns the appointment as a tuple (pid, day, start, kind), and Schedule.end(aid), the minute the appointment ends; an unknown id raises KeyError. Add tests.

    {RULE}an appointment starts at or after 8:00 (480) and before 17:00 (1020); any other start raises ValueError and books nothing.
    """,
    f"""
    Add Schedule.day(day): the ids of the appointments on day, sorted by start. Add tests.

    {RULE}the clinic has one chair, so two appointments on the same day never overlap: a booking that starts before another appointment ends and ends after it starts raises ValueError and books nothing.
    """,
    f"""
    Add fee(schedule, aid) to fees.py: the fee of the appointment in cents. Add tests.

    {DEC}a checkup costs 5000 cents, a filling 12000 cents and a cleaning 8000 cents.
    """,
    f"""
    Add Schedule.mark(aid, status), where status is "done" or "missed" (anything else raises ValueError), and Schedule.status(aid), which is "open" until the appointment is marked. From now on fee(schedule, aid) is the kind's fee for a done appointment, the no-show fee for a missed one, and 0 for an open one. Add tests.

    {DEC}the no-show fee is 2000 cents.
    """,
    f"""
    Add Patients.find(text): the ids of the patients whose name contains text, ignoring case, in id order. Add tests.

    {DEC}patients under 12 pay half the fee of a done appointment, rounded to the nearest cent; the no-show fee is the same for every patient.
    """,
    f"""
    Add agenda(schedule, day) to export.py: one text line per appointment on day, sorted by start: the start as HH:MM, a space and the patient name, for example "09:00 Ann Lee". Add tests.

    {later("agenda", 'each line ends with a space and the kind in brackets, for example "09:00 Ann Lee (checkup)".')}

    {CHG}every appointment lasts 20 minutes, not 30.
    """,
    f"""
    Add Schedule.cancel(aid), which removes the appointment; an unknown id raises KeyError. Add tests.

    {CHG}a filling costs 13500 cents, not 12000.
    """,
    f"""
    Add export_day(schedule, day, path) to export.py: a CSV file with one row per appointment on day, sorted by start (start, patient name, kind), with the start in minutes. Add tests.

    {later("export_day", "the start is written as HH:MM (for example 09:00) instead of minutes.")}

    {DEC}an exported day file starts with the header line start,patient,kind and uses "," as the delimiter.
    """,
    f"""
    Add bill(schedule, pid) to fees.py: the sum of the fees of the patient's appointments. Add tests.

    {CHG}an appointment starts before 16:00 (960), not 17:00.
    """,
    f"""
    Add Schedule.of_patient(pid): the ids of the patient's appointments in id order. Add tests.

    {CHG}patients under 16 pay half, not patients under 12.
    """,
    f"""
    Add Schedule.count(day): the number of appointments on day. Add tests.

    {CHG}the no-show fee is 2500 cents, not 2000.
    """,
    f"""
    Add Schedule.move(aid, day, start), which moves an appointment; the booking rules still apply, and a broken rule raises ValueError and changes nothing. Add tests.

    {CHG}every appointment lasts 45 minutes, not 20.
    """,
    """
    Add revenue(schedule, day) to fees.py: the sum of the fees of the appointments on day. Add tests.
    """,
    f"""
    Add Schedule.missed(pid): the number of missed appointments of the patient. Add tests.

    {CHG}a filling costs 12500 cents, not 13500.
    """,
    """
    Add Patients.rename(pid, name), which changes a patient's name; the name rules still apply. Add tests.
    """,
    f"""
    Add busiest_day(schedule) to fees.py: the day with the most appointments, the earliest one on a tie, or None when there are none. Add tests.

    {CHG}an appointment starts before 18:00 (1080), not 16:00.
    """,
    f"""
    Add Schedule.kinds(day): a dict that maps each kind to the number of appointments of that kind on day. Add tests.

    {CHG}patients under 14 pay half, not patients under 16.
    """,
    """
    Add Schedule.first(day): the id of the earliest appointment on day, or None when there is none. Add tests.
    """,
    f"""
    Add Schedule.open_ids(): the ids of the open appointments in id order. Add tests. {FINISH}
    """],
   '''
    import datetime as dt
    import pytest
    from patients import Patients
    from schedule import Schedule
    from fees import fee
    from export import agenda, export_day

    D = dt.date
    MON, TUE = D(2026, 1, 5), D(2026, 1, 6)


    def _s(age=30):
        p = Patients()
        p.register("Ann", age)
        return Schedule(p)


    def test_basic():
        s = _s()
        i = s.book(1, MON, 600, "checkup")
        assert i == 1 and s.get(i) == (1, MON, 600, "checkup") and s.day(MON) == [1] and s.day(TUE) == []
        assert s.patients.name(1) == "Ann" and s.patients.age(1) == 30 and s.status(i) == "open"
        with pytest.raises(KeyError):
            s.get(9)
        with pytest.raises(KeyError):
            s.book(7, TUE, 600, "checkup")


    def _end():
        s = _s()
        return s.end(s.book(1, MON, 600, "checkup"))


    def test_fact_slot_len():
        assert _end() == 645


    def test_stale_slot_20():
        assert _end() == 620


    def test_stale_slot_30():
        assert _end() == 630


    def _start_ok(start):
        try:
            _s().book(1, MON, start, "checkup")
            return True
        except ValueError:
            return False


    def test_fact_last_start():
        assert _start_ok(1079) and not _start_ok(1080)


    def test_stale_last_960():
        assert not _start_ok(1000)


    def test_stale_last_1020():
        assert not _start_ok(1050)


    def test_fact_open_8():
        assert _start_ok(480) and not _start_ok(479)


    def _fee(age, kind="filling", status="done"):
        s = _s(age)
        i = s.book(1, MON, 600, kind)
        s.mark(i, status)
        return fee(s, i)


    def test_fact_filling_fee():
        assert _fee(30) == 12500


    def test_stale_filling_13500():
        assert _fee(30) == 13500


    def test_stale_filling_12000():
        assert _fee(30) == 12000


    def test_fact_kid_age():
        full = _fee(30)
        assert _fee(13) == round(full / 2) and _fee(14) == full


    def test_stale_kid_16():
        assert _fee(15) == round(_fee(30) / 2)


    def test_stale_kid_12():
        assert _fee(12) == _fee(30)


    def test_fact_no_show_fee():
        assert _fee(30, status="missed") == 2500


    def test_stale_no_show_2000():
        assert _fee(30, status="missed") == 2000


    def test_fact_kid_noshow():
        assert _fee(5, status="missed") == _fee(30, status="missed")


    def test_fact_no_overlap():
        s = _s()
        s.book(1, MON, 600, "checkup")
        with pytest.raises(ValueError):
            s.book(1, MON, 610, "cleaning")
        assert s.day(MON) == [1] and s.book(1, TUE, 610, "cleaning") == 2


    def test_fact_kind_valid():
        s = _s()
        with pytest.raises(ValueError):
            s.book(1, MON, 600, "whitening")
        assert s.day(MON) == []


    def test_fact_name_required():
        p = Patients()
        for n in ("", "   "):
            with pytest.raises(ValueError):
                p.register(n, 30)
        i = p.register("  Bob ", 30)
        assert i == 1 and p.name(i) == "Bob"


    def test_fact_name_spaces():
        p = Patients()
        assert p.name(p.register("Ann   Lee", 30)) == "Ann Lee"


    def test_fact_agenda_kind():
        p = Patients()
        p.register("Ann Lee", 30)
        s = Schedule(p)
        s.book(1, MON, 540, "checkup")
        assert [x.strip() for x in agenda(s, MON)] == ["09:00 Ann Lee (checkup)"]


    def _rows(tmp_path):
        s = _s()
        s.book(1, MON, 540, "checkup")
        p = tmp_path / "d.csv"
        export_day(s, MON, str(p))
        return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        assert _rows(tmp_path)[0] == "start,patient,kind"


    def test_fact_export_hhmm(tmp_path):
        assert _rows(tmp_path)[1].split(",")[0] == "09:00"
    ''',
   {"patients.py": '''
    """Patients."""


    class Patients:
        def __init__(self):
            self._p = {}
            self._n = 0

        @staticmethod
        def _clean(name):
            name = " ".join(w for w in name.split(" ") if w)
            if not name:
                raise ValueError("name required")
            return name

        def register(self, name, age):
            name = self._clean(name)
            self._n += 1
            self._p[self._n] = [name, age]
            return self._n

        def name(self, pid):
            return self._p[pid][0]

        def age(self, pid):
            return self._p[pid][1]

        def find(self, text):
            return [k for k, v in self._p.items() if text.lower() in v[0].lower()]

        def rename(self, pid, name):
            self._p[pid][0] = self._clean(name)
    ''',
    "schedule.py": '''
    """Appointments."""
    from collections import Counter

    SLOT = 45
    OPEN = 480
    LAST = 1080
    KINDS = ("checkup", "filling", "cleaning")


    class Schedule:
        def __init__(self, patients):
            self.patients = patients
            self._a = {}
            self._st = {}
            self._n = 0

        def _check(self, pid, day, start, kind, skip=None):
            self.patients.name(pid)
            if kind not in KINDS:
                raise ValueError(f"bad kind {kind!r}")
            if not OPEN <= start < LAST:
                raise ValueError("clinic closed")
            for k, (_, d, s, _) in self._a.items():
                if k != skip and d == day and start < s + SLOT and s < start + SLOT:
                    raise ValueError("chair taken")

        def book(self, pid, day, start, kind):
            self._check(pid, day, start, kind)
            self._n += 1
            self._a[self._n] = (pid, day, start, kind)
            self._st[self._n] = "open"
            return self._n

        def get(self, aid):
            return self._a[aid]

        def end(self, aid):
            return self._a[aid][2] + SLOT

        def day(self, day):
            return sorted((k for k, v in self._a.items() if v[1] == day), key=lambda k: self._a[k][2])

        def mark(self, aid, status):
            self._a[aid]
            if status not in ("done", "missed"):
                raise ValueError(f"bad status {status!r}")
            self._st[aid] = status

        def status(self, aid):
            self._a[aid]
            return self._st[aid]

        def cancel(self, aid):
            del self._a[aid]
            del self._st[aid]

        def ids(self):
            return list(self._a)

        def of_patient(self, pid):
            return [k for k, v in self._a.items() if v[0] == pid]

        def count(self, day):
            return len(self.day(day))

        def move(self, aid, day, start):
            pid, _, _, kind = self._a[aid]
            self._check(pid, day, start, kind, skip=aid)
            self._a[aid] = (pid, day, start, kind)

        def missed(self, pid):
            return sum(self._st[k] == "missed" for k in self.of_patient(pid))

        def kinds(self, day):
            return dict(Counter(self._a[k][3] for k in self.day(day)))

        def first(self, day):
            d = self.day(day)
            return d[0] if d else None

        def open_ids(self):
            return [k for k in self._a if self._st[k] == "open"]
    ''',
    "fees.py": '''
    """Fees and bills."""
    from collections import Counter

    FEES = {"checkup": 5000, "filling": 12500, "cleaning": 8000}
    NO_SHOW = 2500
    KID_UNDER = 14


    def fee(schedule, aid):
        pid, _, _, kind = schedule.get(aid)
        st = schedule.status(aid)
        if st == "missed":
            return NO_SHOW
        if st == "open":
            return 0
        f = FEES[kind]
        if schedule.patients.age(pid) < KID_UNDER:
            f = round(f / 2)
        return f


    def bill(schedule, pid):
        return sum(fee(schedule, a) for a in schedule.of_patient(pid))


    def revenue(schedule, day):
        return sum(fee(schedule, a) for a in schedule.day(day))


    def busiest_day(schedule):
        c = Counter(schedule.get(a)[1] for a in schedule.ids())
        return min(c, key=lambda d: (-c[d], d)) if c else None
    ''',
    "export.py": '''
    """Agenda and CSV export."""
    import csv


    def hhmm(m):
        return f"{m // 60:02d}:{m % 60:02d}"


    def agenda(schedule, day):
        out = []
        for a in schedule.day(day):
            pid, _, start, kind = schedule.get(a)
            out.append(f"{hhmm(start)} {schedule.patients.name(pid)} ({kind})")
        return out


    def export_day(schedule, day, path):
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["start", "patient", "kind"])
            for a in schedule.day(day):
                pid, _, start, kind = schedule.get(a)
                w.writerow([hhmm(start), schedule.patients.name(pid), kind])
    '''}, "advanced")

# ---------------------------------------------------------------- A05 restaurant tabs (21 sessions)
mk("A05", {"service_pct": "superseded", "party_min": "superseded", "staff_pct": "superseded",
           "money_format": "superseded", "max_lines": "superseded",
           "menu_sorted": "unfinished", "split_fair": "unfinished", "receipt_merge": "unfinished",
           "qty_positive": "constraint", "unknown_dish": "constraint", "closed_tab": "constraint",
           "service_after_discount": "decision", "export_header": "decision"},
   "Menu, table tabs and bills for a small restaurant. Money is in cents (ints).",
   {"menu.py": '"""The menu."""\n', "tabs.py": '"""Table tabs."""\n', "bills.py": '"""Bills."""\n',
    "export.py": '"""CSV export."""\n'},
   [f"""
    Add a Menu class to menu.py with add(name, price), which adds a dish, and price(name), its price in cents; an unknown dish raises KeyError. Add Menu.items(): the dish names in the order they were added. Add tests.

    {later("Menu.items", "the names are sorted by price, and by name for the same price.")}

    {DEC}a staff tab gets 50% off its subtotal, rounded to the nearest cent.
    """,
    f"""
    Add a Tabs class to tabs.py. Tabs(menu) works on a Menu, kept as its attribute menu. open(table, guests, staff=False) opens a tab and returns a tab id (an int counter that starts at 1); order(tid, dish, qty) adds an order line; lines(tid) is the list of order lines as (dish, qty) tuples, in the order they were added. Add tests.

    {RULE}an order quantity is 1 or more; anything else raises ValueError and adds nothing.

    {RULE}ordering a dish that is not on the menu raises KeyError and adds nothing.
    """,
    f"""
    Add subtotal(tabs, tid) to bills.py: the sum of quantity times dish price over the tab's lines. Add tests.

    {DEC}a tab with 6 or more guests gets a 10% service charge, rounded to the nearest cent.
    """,
    f"""
    Add total(tabs, tid) to bills.py: what the table pays: the subtotal less any staff discount plus any service charge. Add tests.

    {DEC}the service charge is computed on the subtotal after the staff discount.
    """,
    f"""
    Add format_money(cents) to bills.py. Add tests.

    {DEC}money is shown as units, a dot and two-digit cents: format_money(1250) returns "12.50".
    """,
    f"""
    Add Tabs.close(tid) and Tabs.is_open(tid). Add tests.

    {RULE}a closed tab takes no orders: an order on it raises ValueError and adds nothing.
    """,
    f"""
    Add split(total, n) to bills.py: a list of n int shares of total, each total // n. Add tests.

    {later("split", "the shares add up to total: the first total % n shares get one cent more, so split(1000, 3) is [334, 333, 333].")}

    {RULE}a tab holds at most 30 order lines (each order call adds one line); one more raises ValueError and adds nothing.
    """,
    f"""
    Add receipt(tabs, tid) to bills.py: one text line per order line, "<qty> x <dish>", for example "2 x Soup", in order. Add tests.

    {later("receipt", 'lines for the same dish are merged into one line with the summed quantity, at the place where the dish was first ordered: lines "2 x Soup" and "1 x Soup" become "3 x Soup".')}

    {CHG}the service charge is 12%, not 10%.
    """,
    f"""
    Add Tabs.of_table(table): the ids of the tabs of table, in id order. Add tests.

    {CHG}money is shown with a dollar sign in front: format_money(1250) returns "$12.50", not "12.50".
    """,
    f"""
    Add export_tabs(tabs, path) to export.py: a CSV file with one row per tab in id order (id, table, guests, total). Add tests.

    {DEC}an exported tabs file starts with the header line id,table,guests,total and uses "," as the delimiter.
    """,
    f"""
    Add Tabs.open_ids(): the ids of the open tabs, in id order. Add tests.

    {CHG}the service charge applies to tabs with 8 or more guests, not 6.
    """,
    f"""
    Add Menu.remove(name), which takes a dish off the menu; an unknown dish raises KeyError. Add tests.

    {CHG}a staff tab gets 30% off its subtotal, not 50%.
    """,
    """
    Add Tabs.guests_total(): the number of guests over all open tabs. Add tests.
    """,
    f"""
    Add Tabs.move(tid, table), which moves a tab to another table. Add tests.

    {CHG}a tab holds at most 40 order lines, not 30.
    """,
    f"""
    Add revenue(tabs) to bills.py: the sum of the totals of the closed tabs. Add tests.

    {CHG}the service charge is 15%, not 12%.
    """,
    """
    Add best_dish(tabs) to bills.py: the dish with the most items ordered over all tabs, the smallest name on a tie, or None when nothing was ordered. Add tests.
    """,
    f"""
    Add Menu.set_price(name, price), which changes the price of a dish; an unknown dish raises KeyError. Add tests.

    {CHG}money is shown as units, a dot, two-digit cents, a space and "USD": format_money(1250) returns "12.50 USD", not "$12.50".
    """,
    f"""
    Add Tabs.void(tid, index), which removes the order line at index (0 is the first) from an open tab. Add tests.

    {CHG}the service charge applies to tabs with 5 or more guests, not 8.
    """,
    """
    Add Tabs.item_count(tid): the total quantity over the tab's lines. Add tests.
    """,
    f"""
    Add Tabs.guests(tid): the number of guests of the tab. Add tests.

    {CHG}a staff tab gets 40% off its subtotal, not 30%.
    """,
    f"""
    Add Tabs.reopen(tid), which opens a closed tab again. Add tests. {FINISH}
    """],
   '''
    import pytest
    from menu import Menu
    from tabs import Tabs
    from bills import subtotal, total, format_money, split, receipt
    from export import export_tabs


    def _t():
        m = Menu()
        m.add("Soup", 500)
        m.add("Tea", 200)
        m.add("Steak", 2500)
        return Tabs(m)


    def test_basic():
        t = _t()
        assert t.menu.price("Tea") == 200
        with pytest.raises(KeyError):
            t.menu.price("Cake")
        i = t.open(3, 2)
        t.order(i, "Soup", 2)
        t.order(i, "Tea", 1)
        assert i == 1 and t.lines(i) == [("Soup", 2), ("Tea", 1)] and subtotal(t, i) == 1200 and t.is_open(i)


    def _total(guests, staff=False):
        t = _t()
        i = t.open(1, guests, staff)
        t.order(i, "Steak", 4)
        return total(t, i)


    def test_fact_service_pct():
        assert _total(8) == 11500


    def test_stale_service_12():
        assert _total(8) == 11200


    def test_stale_service_10():
        assert _total(8) == 11000


    def test_fact_party_min():
        assert _total(5) > 10000 and _total(4) == 10000


    def test_stale_party_8():
        assert _total(7) == 10000


    def test_stale_party_6():
        assert _total(5) == 10000


    def test_fact_staff_pct():
        assert _total(2, True) == 6000


    def test_stale_staff_30():
        assert _total(2, True) == 7000


    def test_stale_staff_50():
        assert _total(2, True) == 5000


    def test_fact_service_after_discount():
        a = _total(2, True)
        b = _total(8) - 10000
        assert _total(8, True) == a + round(a * b / 10000)


    def test_fact_money_format():
        assert format_money(1250) == "12.50 USD"


    def test_stale_money_dollar():
        assert format_money(1250) == "$12.50"


    def test_stale_money_plain():
        assert format_money(1250) == "12.50"


    def _lines_ok(n):
        t = _t()
        i = t.open(1, 2)
        for _ in range(n - 1):
            t.order(i, "Tea", 1)
        try:
            t.order(i, "Tea", 1)
            return True
        except ValueError:
            assert len(t.lines(i)) == n - 1
            return False


    def test_fact_max_lines():
        assert _lines_ok(40) and not _lines_ok(41)


    def test_stale_lines_30():
        assert not _lines_ok(31)


    def test_fact_menu_sorted():
        m = Menu()
        m.add("Tea", 200)
        m.add("Steak", 2500)
        m.add("Juice", 200)
        m.add("Soup", 500)
        assert m.items() == ["Juice", "Tea", "Soup", "Steak"]


    def test_fact_split_fair():
        assert split(1000, 3) == [334, 333, 333] and split(1001, 4) == [251, 250, 250, 250]


    def test_fact_receipt_merge():
        t = _t()
        i = t.open(1, 2)
        t.order(i, "Soup", 2)
        t.order(i, "Tea", 1)
        t.order(i, "Soup", 1)
        r = [x.strip() for x in receipt(t, i)]
        assert len(r) == 2 and r[0] == "3 x Soup"


    def test_fact_qty_positive():
        t = _t()
        i = t.open(1, 2)
        for q in (0, -1):
            with pytest.raises(ValueError):
                t.order(i, "Tea", q)
        assert t.lines(i) == []


    def test_fact_unknown_dish():
        t = _t()
        i = t.open(1, 2)
        with pytest.raises(KeyError):
            t.order(i, "Cake", 1)
        assert t.lines(i) == []


    def test_fact_closed_tab():
        t = _t()
        i = t.open(1, 2)
        t.order(i, "Tea", 1)
        t.close(i)
        with pytest.raises(ValueError):
            t.order(i, "Tea", 1)
        assert not t.is_open(i) and t.lines(i) == [("Tea", 1)]


    def test_fact_export_header(tmp_path):
        t = _t()
        t.open(1, 2)
        p = tmp_path / "t.csv"
        export_tabs(t, str(p))
        rows = [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]
        assert rows[0] == "id,table,guests,total" and rows[1].split(",")[0] == "1"
    ''',
   {"menu.py": '''
    """The menu."""


    class Menu:
        def __init__(self):
            self._p = {}

        def add(self, name, price):
            self._p[name] = price

        def price(self, name):
            return self._p[name]

        def items(self):
            return sorted(self._p, key=lambda n: (self._p[n], n))

        def remove(self, name):
            del self._p[name]

        def set_price(self, name, price):
            self._p[name]
            self._p[name] = price
    ''',
    "tabs.py": '''
    """Table tabs."""

    MAX_LINES = 40


    class Tabs:
        def __init__(self, menu):
            self.menu = menu
            self._t = {}
            self._n = 0

        def open(self, table, guests, staff=False):
            self._n += 1
            self._t[self._n] = {"table": table, "guests": guests, "staff": staff, "lines": [], "open": True}
            return self._n

        def order(self, tid, dish, qty):
            t = self._t[tid]
            if not t["open"]:
                raise ValueError("tab is closed")
            if qty < 1:
                raise ValueError("quantity must be 1 or more")
            self.menu.price(dish)
            if len(t["lines"]) >= MAX_LINES:
                raise ValueError("tab is full")
            t["lines"].append((dish, qty))

        def lines(self, tid):
            return list(self._t[tid]["lines"])

        def table(self, tid):
            return self._t[tid]["table"]

        def guests(self, tid):
            return self._t[tid]["guests"]

        def is_staff(self, tid):
            return self._t[tid]["staff"]

        def close(self, tid):
            self._t[tid]["open"] = False

        def reopen(self, tid):
            self._t[tid]["open"] = True

        def is_open(self, tid):
            return self._t[tid]["open"]

        def ids(self):
            return list(self._t)

        def of_table(self, table):
            return [k for k, v in self._t.items() if v["table"] == table]

        def open_ids(self):
            return [k for k, v in self._t.items() if v["open"]]

        def guests_total(self):
            return sum(self._t[k]["guests"] for k in self.open_ids())

        def move(self, tid, table):
            self._t[tid]["table"] = table

        def void(self, tid, index):
            if not self._t[tid]["open"]:
                raise ValueError("tab is closed")
            del self._t[tid]["lines"][index]

        def item_count(self, tid):
            return sum(q for _, q in self._t[tid]["lines"])
    ''',
    "bills.py": '''
    """Bills."""
    from collections import Counter

    SERVICE = 15
    PARTY_MIN = 5
    STAFF_OFF = 40


    def subtotal(tabs, tid):
        return sum(q * tabs.menu.price(d) for d, q in tabs.lines(tid))


    def total(tabs, tid):
        s = subtotal(tabs, tid)
        if tabs.is_staff(tid):
            s -= round(s * STAFF_OFF / 100)
        if tabs.guests(tid) >= PARTY_MIN:
            s += round(s * SERVICE / 100)
        return s


    def format_money(cents):
        return f"{cents // 100}.{cents % 100:02d} USD"


    def split(total, n):
        q, r = divmod(total, n)
        return [q + (i < r) for i in range(n)]


    def receipt(tabs, tid):
        c = {}
        for d, q in tabs.lines(tid):
            c[d] = c.get(d, 0) + q
        return [f"{q} x {d}" for d, q in c.items()]


    def revenue(tabs):
        return sum(total(tabs, i) for i in tabs.ids() if not tabs.is_open(i))


    def best_dish(tabs):
        c = Counter()
        for i in tabs.ids():
            for d, q in tabs.lines(i):
                c[d] += q
        return min(c, key=lambda d: (-c[d], d)) if c else None
    ''',
    "export.py": '''
    """CSV export."""
    import csv

    from bills import total


    def export_tabs(tabs, path):
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "table", "guests", "total"])
            for i in tabs.ids():
                w.writerow([i, tabs.table(i), tabs.guests(i), total(tabs, i)])
    '''}, "advanced")

# ---------------------------------------------------------------- A06 electricity billing (21 sessions)
mk("A06", {"standing_charge": "superseded", "rate1": "superseded", "block": "superseded",
           "rate2": "superseded", "late_pct": "superseded",
           "meter_order": "unfinished", "kwh_line": "unfinished", "export_order": "unfinished",
           "meter_id": "constraint", "reading_order": "constraint", "monotonic": "constraint",
           "social": "decision", "export_header": "decision"},
   "Meters, meter readings and bills for a small electricity supplier. Money is in cents (ints); days are datetime.date; a meter reading is the meter's running total in whole kWh.",
   {"meters.py": '"""The meters."""\n', "readings.py": '"""Meter readings."""\n', "billing.py": '"""Bills."""\n',
    "export.py": '"""CSV export."""\n'},
   [f"""
    Add a Meters class to meters.py with add(mid, social=False), which adds a meter, is_social(mid), which tells whether it is a social-tariff meter (an unknown id raises KeyError), and ids(): the meter ids in the order they were added. Add tests.

    {RULE}a meter id is "M" followed by one or more digits, like "M7" or "M12"; any other id raises ValueError and adds nothing.

    {later("Meters.ids", 'the ids are sorted by the number after the M, so "M7" comes before "M12".')}
    """,
    f"""
    Add a Readings class to readings.py. Readings(meters) works on a Meters, kept as its attribute meters. record(mid, day, value) records a reading of the meter; history(mid) is the list of its readings as (day, value) tuples in the order recorded. An unknown meter raises KeyError and records nothing. Add tests.

    {RULE}each reading of a meter is on a later day than the meter's last reading; a reading on the same day or an earlier day raises ValueError and records nothing.
    """,
    f"""
    Add Readings.latest(mid): the last reading as a (day, value) tuple, or None when the meter has none. Add tests.

    {RULE}a reading value is never lower than the meter's last reading value; a lower value raises ValueError and records nothing (an equal value is fine).
    """,
    f"""
    Add cost(kwh) to billing.py: the energy cost of kwh kWh in cents. Add tests.

    {DEC}the first 300 kWh of a bill cost 15 cents per kWh, and every kWh above 300 costs 25 cents.
    """,
    f"""
    Add Readings.usage(mid, start, end): the reading value on day end minus the reading value on day start; when the meter has no reading on one of those days it raises KeyError. Add tests.

    {DEC}every bill includes a standing charge of 900 cents.
    """,
    f"""
    Add bill(readings, mid, start, end) to billing.py: cost of the usage from start to end plus the standing charge. Add tests.

    {DEC}a social-tariff meter pays no standing charge; its bill is the energy cost only.
    """,
    f"""
    Add late_total(readings, mid, start, end) to billing.py: what is owed when the bill is paid late: the bill plus a late fee. Add tests.

    {DEC}the late fee is 5% of the bill, rounded to the nearest cent.
    """,
    f"""
    Add statement(readings, mid, start, end) to billing.py: a list of text lines: "from: <start>", "to: <end>" (ISO days), then "bill: <cents>", where <cents> is the bill. Add tests.

    {later("statement", 'after the "to:" line it has the line "kWh: <N>", the usage (for example "kWh: 120").')}

    {CHG}the first block of kWh costs 18 cents per kWh, not 15.
    """,
    f"""
    Add Meters.remove(mid), which removes a meter; an unknown id raises KeyError. Add tests.

    {CHG}the cheaper first block is the first 250 kWh of a bill, not 300; every kWh above 250 costs the higher rate.
    """,
    f"""
    Add export_readings(readings, path) to export.py: a CSV file with one row per reading (meter, day, value), with ISO days, in the order recorded. Add tests.

    {later("export_readings", "the rows are sorted by the number after the M of the meter id, and by day for the same meter.")}

    {DEC}an exported readings file starts with the header line meter,day,kwh and uses "," as the delimiter.
    """,
    f"""
    Add Readings.count(mid): the number of readings of the meter. Add tests.

    {CHG}the standing charge is 1100 cents, not 900.
    """,
    f"""
    Add Meters.social_ids(): the ids of the social-tariff meters. Add tests.

    {CHG}the late fee is 8% of the bill, not 5%.
    """,
    f"""
    Add Readings.meters_read(day): the ids of the meters with a reading on day. Add tests.

    {CHG}every kWh above the first block costs 22 cents, not 25.
    """,
    f"""
    Add Readings.first(mid): the first reading as a (day, value) tuple, or None. Add tests.

    {CHG}the first block of kWh costs 16 cents per kWh, not 18.
    """,
    """
    Add average_daily(readings, mid, start, end) to billing.py: the usage divided by the number of days from start to end, rounded down. Add tests.
    """,
    f"""
    Add Meters.set_social(mid, flag), which turns the social tariff of a meter on or off. Add tests.

    {CHG}the cheaper first block is the first 400 kWh of a bill, not 250.
    """,
    """
    Add Readings.undo(mid), which removes the meter's last reading; a meter with no readings raises KeyError. Add tests.
    """,
    f"""
    Add Readings.days(mid): the days of the meter's readings, in order. Add tests.

    {CHG}the standing charge is 1000 cents, not 1100.
    """,
    f"""
    Add total_bills(readings, start, end) to billing.py: the sum of the bills of all meters that have a reading on both days. Add tests.

    {CHG}the late fee is 6% of the bill, not 8%.
    """,
    """
    Add Meters.count(): the number of meters. Add tests.
    """,
    f"""
    Add Readings.last_day(): the latest reading day over all meters, or None when there are no readings. Add tests. {FINISH}
    """],
   '''
    import datetime as dt
    import pytest
    from meters import Meters
    from readings import Readings
    from billing import bill, late_total, statement
    from export import export_readings

    D = dt.date
    D1, D2, D3 = D(2026, 1, 5), D(2026, 2, 5), D(2026, 3, 5)


    def _r():
        m = Meters()
        m.add("M1")
        m.add("M2", social=True)
        return Readings(m)


    def test_basic():
        r = _r()
        r.record("M1", D1, 1000)
        r.record("M1", D2, 1120)
        assert r.history("M1") == [(D1, 1000), (D2, 1120)] and r.latest("M1") == (D2, 1120)
        assert r.latest("M2") is None and r.usage("M1", D1, D2) == 120 and r.meters.is_social("M2")
        with pytest.raises(KeyError):
            r.record("M9", D1, 5)
        with pytest.raises(KeyError):
            r.usage("M1", D1, D3)


    def _bill(kwh, mid="M1", fn=None):
        r = _r()
        r.record(mid, D1, 1000)
        r.record(mid, D2, 1000 + kwh)
        return (fn or bill)(r, mid, D1, D2)


    def test_fact_standing_charge():
        assert _bill(0) == 1000


    def test_stale_standing_1100():
        assert _bill(0) == 1100


    def test_stale_standing_900():
        assert _bill(0) == 900


    def test_fact_rate1():
        assert _bill(100) - _bill(0) == 1600


    def test_stale_rate1_18():
        assert _bill(100) - _bill(0) == 1800


    def test_stale_rate1_15():
        assert _bill(100) - _bill(0) == 1500


    def test_fact_block():
        d = _bill(1) - _bill(0)
        assert _bill(400) - _bill(399) == d and _bill(401) - _bill(400) != d


    def test_stale_block_250():
        assert _bill(251) - _bill(250) != _bill(1) - _bill(0)


    def test_stale_block_300():
        assert _bill(301) - _bill(300) != _bill(1) - _bill(0)


    def test_fact_rate2():
        assert _bill(1001) - _bill(1000) == 22


    def test_stale_rate2_25():
        assert _bill(1001) - _bill(1000) == 25


    def test_fact_social():
        assert _bill(100, "M2") == _bill(100) - _bill(0)


    def _late():
        b = _bill(100)
        return _bill(100, fn=late_total) - b, b


    def test_fact_late_pct():
        x, b = _late()
        assert x == round(b * 6 / 100)


    def test_stale_late_8():
        x, b = _late()
        assert x == round(b * 8 / 100)


    def test_stale_late_5():
        x, b = _late()
        assert x == round(b * 5 / 100)


    def test_fact_meter_id():
        m = Meters()
        for bad in ("X1", "M", "M1a"):
            with pytest.raises(ValueError):
                m.add(bad)
        assert m.ids() == []


    def test_fact_meter_order():
        m = Meters()
        m.add("M12")
        m.add("M7")
        m.add("M100")
        assert m.ids() == ["M7", "M12", "M100"]


    def test_fact_reading_order():
        r = _r()
        r.record("M1", D2, 5)
        for d in (D1, D2):
            with pytest.raises(ValueError):
                r.record("M1", d, 9)
        assert r.history("M1") == [(D2, 5)]


    def test_fact_monotonic():
        r = _r()
        r.record("M1", D1, 500)
        with pytest.raises(ValueError):
            r.record("M1", D2, 499)
        r.record("M1", D2, 500)
        assert r.history("M1") == [(D1, 500), (D2, 500)]


    def test_fact_kwh_line():
        r = _r()
        r.record("M1", D1, 1000)
        r.record("M1", D2, 1120)
        lines = [x.strip() for x in statement(r, "M1", D1, D2)]
        assert len(lines) == 4 and lines[2] == "kWh: 120" and lines[3] == f"bill: {bill(r, 'M1', D1, D2)}"


    def _rows(r, tmp_path):
        p = tmp_path / "m.csv"
        export_readings(r, str(p))
        return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        r = _r()
        r.record("M1", D1, 5)
        rows = _rows(r, tmp_path)
        assert rows[0] == "meter,day,kwh" and rows[1].split(",")[2] == "5"


    def test_fact_export_order(tmp_path):
        m = Meters()
        m.add("M12")
        m.add("M7")
        r = Readings(m)
        r.record("M12", D1, 1)
        r.record("M7", D1, 2)
        r.record("M7", D2, 3)
        assert [x.split(",")[0] for x in _rows(r, tmp_path)[1:]] == ["M7", "M7", "M12"]
    ''',
   {"meters.py": '''
    """The meters."""
    import re


    def _num(mid):
        return int(mid[1:])


    class Meters:
        def __init__(self):
            self._m = {}

        def add(self, mid, social=False):
            if not re.fullmatch(r"M[0-9]+", mid):
                raise ValueError(f"bad meter id {mid!r}")
            self._m[mid] = social

        def is_social(self, mid):
            return self._m[mid]

        def set_social(self, mid, flag):
            self._m[mid]
            self._m[mid] = flag

        def ids(self):
            return sorted(self._m, key=_num)

        def remove(self, mid):
            del self._m[mid]

        def social_ids(self):
            return [m for m in self.ids() if self._m[m]]

        def count(self):
            return len(self._m)
    ''',
    "readings.py": '''
    """Meter readings."""
    from meters import _num


    class Readings:
        def __init__(self, meters):
            self.meters = meters
            self._h = {}

        def record(self, mid, day, value):
            self.meters.is_social(mid)
            h = self._h.get(mid, [])
            if h and day <= h[-1][0]:
                raise ValueError("reading must be on a later day")
            if h and value < h[-1][1]:
                raise ValueError("reading lower than the last one")
            self._h[mid] = h + [(day, value)]

        def history(self, mid):
            self.meters.is_social(mid)
            return list(self._h.get(mid, []))

        def latest(self, mid):
            h = self.history(mid)
            return h[-1] if h else None

        def first(self, mid):
            h = self.history(mid)
            return h[0] if h else None

        def _at(self, mid, day):
            for d, v in self.history(mid):
                if d == day:
                    return v
            raise KeyError(day)

        def usage(self, mid, start, end):
            return self._at(mid, end) - self._at(mid, start)

        def count(self, mid):
            return len(self.history(mid))

        def meters_read(self, day):
            return sorted((m for m, h in self._h.items() if any(d == day for d, _ in h)), key=_num)

        def undo(self, mid):
            if not self._h.get(mid):
                raise KeyError(mid)
            self._h[mid].pop()

        def days(self, mid):
            return [d for d, _ in self.history(mid)]

        def last_day(self):
            days = [d for h in self._h.values() for d, _ in h]
            return max(days) if days else None
    ''',
    "billing.py": '''
    """Bills."""

    RATE1 = 16
    BLOCK = 400
    RATE2 = 22
    STANDING = 1000
    LATE = 6


    def cost(kwh):
        return min(kwh, BLOCK) * RATE1 + max(0, kwh - BLOCK) * RATE2


    def bill(readings, mid, start, end):
        b = cost(readings.usage(mid, start, end))
        if not readings.meters.is_social(mid):
            b += STANDING
        return b


    def late_total(readings, mid, start, end):
        b = bill(readings, mid, start, end)
        return b + round(b * LATE / 100)


    def statement(readings, mid, start, end):
        return [f"from: {start.isoformat()}", f"to: {end.isoformat()}",
                f"kWh: {readings.usage(mid, start, end)}", f"bill: {bill(readings, mid, start, end)}"]


    def average_daily(readings, mid, start, end):
        return readings.usage(mid, start, end) // (end - start).days


    def total_bills(readings, start, end):
        out = 0
        for m in readings.meters.ids():
            days = readings.days(m)
            if start in days and end in days:
                out += bill(readings, m, start, end)
        return out
    ''',
    "export.py": '''
    """CSV export."""
    import csv

    from meters import _num


    def export_readings(readings, path):
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["meter", "day", "kwh"])
            for m in sorted(readings.meters.ids(), key=_num):
                for d, v in sorted(readings.history(m)):
                    w.writerow([m, d.isoformat(), v])
    '''}, "advanced")

# ---------------------------------------------------------------- A07 airline seats and bags (21 sessions)
mk("A07", {"bag_allowance": "superseded", "excess_fee": "superseded", "child_pct": "superseded",
           "max_bags": "superseded", "change_fee": "superseded",
           "seat_order": "unfinished", "pass_caps": "unfinished", "export_order": "unfinished",
           "seat_exists": "constraint", "seat_taken": "constraint", "bag_weight": "constraint",
           "window_fee": "decision", "export_header": "decision"},
   "Flights, seat bookings and checked bags for a small airline. Money is in cents (ints); bag weights are whole kg. A seat name is a row number followed by a letter, like \"12C\".",
   {"flights.py": '"""Flights."""\n', "bookings.py": '"""Seat bookings and bags."""\n', "fares.py": '"""Fares and fees."""\n',
    "export.py": '"""Boarding passes and CSV export."""\n'},
   [f"""
    Add a Flights class to flights.py with add(code, seats, fare), which adds a flight with the given list of seat names and a base fare in cents, seats(code), the seat names in the order given, and fare(code), the base fare; an unknown code raises KeyError. Add tests.

    {DEC}seats whose letter is A or F are window seats; a window seat costs 1500 cents more than the base fare.
    """,
    f"""
    Add a Bookings class to bookings.py. Bookings(flights) works on a Flights, kept as its attribute flights. book(code, name, age, seat) books a seat for a passenger and returns a booking id: an int counter that starts at 1. get(bid) returns the booking as a tuple (code, name, age, seat). An unknown code or id raises KeyError. Add tests.

    {RULE}the seat must be one of the flight's seats; any other seat raises ValueError and books nothing.

    {RULE}a seat is booked by at most one passenger; booking a taken seat raises ValueError and books nothing.
    """,
    f"""
    Add fare(bookings, bid) to fares.py: the fare the passenger pays, in cents. Add tests.

    {DEC}passengers under 12 pay 75% of the base fare, rounded to the nearest cent; the window seat fee is added in full.
    """,
    f"""
    Add Bookings.free_seats(code): the seats of the flight that are not booked, in the order given to Flights.add. Add tests.

    {later("Bookings.free_seats", 'the seats are sorted by row number, then by letter, so "2A" comes before "10A".')}
    """,
    f"""
    Add Bookings.add_bag(bid, kg), which checks in a bag of kg kg for the booking, and Bookings.bags(bid), the list of its bag weights in order. Add tests.

    {RULE}a bag weighs at most 32 kg; a heavier bag raises ValueError and adds nothing.

    {RULE}a booking has at most 2 bags; one more raises ValueError and adds nothing.
    """,
    f"""
    Add bag_fee(bookings, bid) to fares.py: the fee for the booking's bags, in cents. Add tests.

    {DEC}each bag carries 23 kg free; every kg above that in a bag costs 1000 cents.
    """,
    f"""
    Add Bookings.change_seat(bid, seat), which moves the passenger to another seat (the seat rules still apply: a broken rule raises ValueError and changes nothing), and Bookings.changes(bid), the number of seat changes of the booking. Add tests.

    {DEC}each seat change costs a change fee of 5000 cents.
    """,
    f"""
    Add total(bookings, bid) to fares.py: the fare plus the bag fee plus the change fees. Add tests.

    {CHG}each bag carries 20 kg free, not 23.
    """,
    f"""
    Add boarding_pass(bookings, bid) to export.py: a list of two text lines: the passenger name, then "seat: <seat>", for example "seat: 12C". Add tests.

    {later("boarding_pass", 'the name line is written in capitals, so "Ann Lee" is written "ANN LEE".')}

    {CHG}every kg above the free weight costs 1500 cents, not 1000.
    """,
    f"""
    Add Bookings.cancel(bid), which removes the booking and frees its seat; an unknown id raises KeyError. Add tests.

    {CHG}passengers under 12 pay 50% of the base fare, not 75%.
    """,
    f"""
    Add export_flight(bookings, code, path) to export.py: a CSV file with one row per booking on the flight, in booking order: the seat, the passenger name and the number of bags. Add tests.

    {later("export_flight", "the rows are sorted by passenger name.")}

    {DEC}an exported flight file starts with the header line seat,name,bags and uses "," as the delimiter.
    """,
    f"""
    Add Bookings.of_flight(code): the booking ids on the flight, in id order. Add tests.

    {CHG}a booking has at most 3 bags, not 2.
    """,
    f"""
    Add manifest(bookings, code) to export.py: the sorted list of passenger names on the flight. Add tests.

    {CHG}each seat change costs 7500 cents, not 5000.
    """,
    f"""
    Add Flights.codes(): the sorted list of flight codes. Add tests.

    {CHG}each bag carries 25 kg free, not 20.
    """,
    """
    Add revenue(bookings, code) to fares.py: the sum of total(bookings, bid) over the flight's bookings. Add tests.
    """,
    f"""
    Add Bookings.remove_bag(bid, index), which removes the bag at index (0 is the first). Add tests.

    {CHG}every kg above the free weight costs 1200 cents, not 1500.
    """,
    f"""
    Add Bookings.find(name): the ids of the bookings whose passenger name contains name, ignoring case, in id order. Add tests.

    {CHG}passengers under 12 pay 60% of the base fare, not 50%.
    """,
    """
    Add Bookings.bag_weight(code): the total weight of all bags on the flight. Add tests.
    """,
    f"""
    Add Flights.remove(code), which removes a flight; an unknown code raises KeyError. Add tests.

    {CHG}each seat change costs 6000 cents, not 7500.
    """,
    """
    Add Bookings.load(code): the number of booked seats on the flight. Add tests.
    """,
    f"""
    Add Bookings.ids(): all booking ids in order. Add tests. {FINISH}
    """],
   '''
    import pytest
    from flights import Flights
    from bookings import Bookings
    from fares import fare, bag_fee, total
    from export import boarding_pass, export_flight


    def _b():
        f = Flights()
        f.add("XY1", ["1A", "1C", "2A", "2C"], 20000)
        return Bookings(f)


    def test_basic():
        b = _b()
        assert b.flights.seats("XY1") == ["1A", "1C", "2A", "2C"] and b.flights.fare("XY1") == 20000
        i = b.book("XY1", "Ann", 30, "1C")
        assert i == 1 and b.get(i) == ("XY1", "Ann", 30, "1C") and b.bags(i) == []
        with pytest.raises(KeyError):
            b.get(5)
        with pytest.raises(KeyError):
            b.book("ZZ9", "Bob", 30, "1A")


    def _fare(age, seat="1C"):
        b = _b()
        return fare(b, b.book("XY1", "Ann", age, seat))


    def test_fact_window_fee():
        assert _fare(30, "1A") - _fare(30) == 1500 and _fare(30, "2C") == _fare(30)


    def test_fact_child_pct():
        base = _fare(30)
        assert _fare(5) == round(base * 60 / 100) and _fare(12) == base


    def test_stale_child_50():
        assert _fare(5) == round(_fare(30) * 50 / 100)


    def test_stale_child_75():
        assert _fare(5) == round(_fare(30) * 75 / 100)


    def _bagfee(kg):
        b = _b()
        i = b.book("XY1", "Ann", 30, "1C")
        b.add_bag(i, kg)
        return bag_fee(b, i)


    def test_fact_bag_allowance():
        assert _bagfee(25) == 0 and _bagfee(26) > 0


    def test_stale_allow_20():
        assert _bagfee(21) > 0


    def test_stale_allow_23():
        assert _bagfee(24) > 0


    def test_fact_excess_fee():
        assert _bagfee(30) - _bagfee(29) == 1200


    def test_stale_excess_1500():
        assert _bagfee(30) - _bagfee(29) == 1500


    def test_stale_excess_1000():
        assert _bagfee(30) - _bagfee(29) == 1000


    def _bags_ok(n):
        b = _b()
        i = b.book("XY1", "Ann", 30, "1C")
        for _ in range(n - 1):
            b.add_bag(i, 10)
        try:
            b.add_bag(i, 10)
            return True
        except ValueError:
            assert len(b.bags(i)) == n - 1
            return False


    def test_fact_max_bags():
        assert _bags_ok(3) and not _bags_ok(4)


    def test_stale_bags_2():
        assert not _bags_ok(3)


    def _change():
        b = _b()
        i = b.book("XY1", "Ann", 30, "1C")
        t = total(b, i)
        b.change_seat(i, "2C")
        return total(b, i) - t


    def test_fact_change_fee():
        assert _change() == 6000


    def test_stale_change_7500():
        assert _change() == 7500


    def test_stale_change_5000():
        assert _change() == 5000


    def test_fact_bag_weight():
        b = _b()
        i = b.book("XY1", "Ann", 30, "1C")
        with pytest.raises(ValueError):
            b.add_bag(i, 33)
        b.add_bag(i, 32)
        assert b.bags(i) == [32]


    def test_fact_seat_exists():
        b = _b()
        with pytest.raises(ValueError):
            b.book("XY1", "Ann", 30, "9Z")
        assert len(b.free_seats("XY1")) == 4


    def test_fact_seat_taken():
        b = _b()
        b.book("XY1", "Ann", 30, "1C")
        with pytest.raises(ValueError):
            b.book("XY1", "Bob", 30, "1C")
        assert b.book("XY1", "Bob", 30, "2C") == 2 and len(b.free_seats("XY1")) == 2


    def test_fact_seat_order():
        f = Flights()
        f.add("XY2", ["10A", "2C", "2A", "1C"], 20000)
        b = Bookings(f)
        fs = b.free_seats("XY2")
        assert fs.index("1C") < fs.index("2A") < fs.index("2C") < fs.index("10A")


    def test_fact_pass_caps():
        b = _b()
        i = b.book("XY1", "Ann Lee", 30, "1C")
        assert boarding_pass(b, i)[0].strip() == "ANN LEE"


    def _rows(b, tmp_path):
        p = tmp_path / "f.csv"
        export_flight(b, "XY1", str(p))
        return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        b = _b()
        b.book("XY1", "Ann", 30, "1C")
        rows = _rows(b, tmp_path)
        assert rows[0] == "seat,name,bags" and rows[1].split(",")[2] == "0"


    def test_fact_export_order(tmp_path):
        b = _b()
        b.book("XY1", "Zoe", 30, "1A")
        b.book("XY1", "Ann", 30, "1C")
        b.book("XY1", "Max", 30, "2A")
        assert [x.split(",")[1] for x in _rows(b, tmp_path)[1:]] == ["Ann", "Max", "Zoe"]
    ''',
   {"flights.py": '''
    """Flights."""


    class Flights:
        def __init__(self):
            self._f = {}

        def add(self, code, seats, fare):
            self._f[code] = (list(seats), fare)

        def seats(self, code):
            return list(self._f[code][0])

        def fare(self, code):
            return self._f[code][1]

        def codes(self):
            return sorted(self._f)

        def remove(self, code):
            del self._f[code]
    ''',
    "bookings.py": '''
    """Seat bookings and bags."""

    MAX_BAGS = 3
    MAX_KG = 32


    def seat_key(seat):
        return (int(seat[:-1]), seat[-1])


    class Bookings:
        def __init__(self, flights):
            self.flights = flights
            self._b = {}
            self._bags = {}
            self._ch = {}
            self._n = 0

        def _check(self, code, seat, skip=None):
            if seat not in self.flights.seats(code):
                raise ValueError(f"no seat {seat!r}")
            for k, v in self._b.items():
                if k != skip and v[0] == code and v[3] == seat:
                    raise ValueError("seat taken")

        def book(self, code, name, age, seat):
            self._check(code, seat)
            self._n += 1
            self._b[self._n] = (code, name, age, seat)
            self._bags[self._n] = []
            self._ch[self._n] = 0
            return self._n

        def get(self, bid):
            return self._b[bid]

        def ids(self):
            return list(self._b)

        def free_seats(self, code):
            taken = {v[3] for v in self._b.values() if v[0] == code}
            return sorted((s for s in self.flights.seats(code) if s not in taken), key=seat_key)

        def add_bag(self, bid, kg):
            self._b[bid]
            if kg > MAX_KG:
                raise ValueError("bag too heavy")
            if len(self._bags[bid]) >= MAX_BAGS:
                raise ValueError("too many bags")
            self._bags[bid].append(kg)

        def bags(self, bid):
            self._b[bid]
            return list(self._bags[bid])

        def remove_bag(self, bid, index):
            del self._bags[bid][index]

        def change_seat(self, bid, seat):
            code, name, age, _ = self._b[bid]
            self._check(code, seat, skip=bid)
            self._b[bid] = (code, name, age, seat)
            self._ch[bid] += 1

        def changes(self, bid):
            self._b[bid]
            return self._ch[bid]

        def cancel(self, bid):
            del self._b[bid]
            del self._bags[bid]
            del self._ch[bid]

        def of_flight(self, code):
            return [k for k, v in self._b.items() if v[0] == code]

        def find(self, name):
            return [k for k, v in self._b.items() if name.lower() in v[1].lower()]

        def bag_weight(self, code):
            return sum(sum(self._bags[k]) for k in self.of_flight(code))

        def load(self, code):
            return len(self.of_flight(code))
    ''',
    "fares.py": '''
    """Fares and fees."""

    WINDOW = 1500
    CHILD = 60
    FREE_KG = 25
    EXCESS = 1200
    CHANGE = 6000


    def fare(bookings, bid):
        code, _, age, seat = bookings.get(bid)
        f = bookings.flights.fare(code)
        if age < 12:
            f = round(f * CHILD / 100)
        if seat[-1] in "AF":
            f += WINDOW
        return f


    def bag_fee(bookings, bid):
        return sum(max(0, kg - FREE_KG) * EXCESS for kg in bookings.bags(bid))


    def total(bookings, bid):
        return fare(bookings, bid) + bag_fee(bookings, bid) + bookings.changes(bid) * CHANGE


    def revenue(bookings, code):
        return sum(total(bookings, b) for b in bookings.of_flight(code))
    ''',
    "export.py": '''
    """Boarding passes and CSV export."""
    import csv


    def boarding_pass(bookings, bid):
        _, name, _, seat = bookings.get(bid)
        return [name.upper(), f"seat: {seat}"]


    def manifest(bookings, code):
        return sorted(bookings.get(b)[1] for b in bookings.of_flight(code))


    def export_flight(bookings, code, path):
        ids = sorted(bookings.of_flight(code), key=lambda b: bookings.get(b)[1])
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["seat", "name", "bags"])
            for b in ids:
                _, name, _, seat = bookings.get(b)
                w.writerow([seat, name, len(bookings.bags(b))])
    '''}, "advanced")

# ---------------------------------------------------------------- A08 bike sharing (21 sessions)
mk("A08", {"unlock_fee": "superseded", "minute_rate": "superseded", "ebike_extra": "superseded",
           "member_free": "superseded", "overtime_after": "superseded",
           "names_sorted": "unfinished", "duration_hours": "unfinished", "export_order": "unfinished",
           "no_bike": "constraint", "dock_full": "constraint", "one_trip": "constraint",
           "overtime_fee": "decision", "export_header": "decision"},
   "Stations, trips and trip charges for a city bike-sharing scheme. Money is in cents (ints); times are int minutes since the scheme opened.",
   {"stations.py": '"""Docking stations."""\n', "trips.py": '"""Trips."""\n', "pricing.py": '"""Trip charges."""\n',
    "export.py": '"""CSV export."""\n'},
   [f"""
    Add a Stations class to stations.py with add(name, capacity, bikes), which adds a station with capacity docks and bikes bikes docked (more bikes than docks raises ValueError), bikes(name), capacity(name), and names(): the station names in the order they were added. An unknown station raises KeyError. Add tests.

    {later("Stations.names", "the names are sorted ignoring case.")}
    """,
    f"""
    Add a Trips class to trips.py. Trips(stations) works on a Stations, kept as its attribute stations. start(rider, station, t, ebike=False, member=False) starts a trip at time t, takes a bike from the station and returns a trip id: an int counter that starts at 1. Add tests.

    {RULE}a trip cannot start at a station with no bikes: it raises ValueError and changes nothing.
    """,
    f"""
    Add Trips.end(tid, station, t), which ends the trip at time t and docks the bike at the station, and Trips.minutes(tid), the end time minus the start time. Add tests.

    {RULE}a bike cannot be docked at a full station: ending a trip there raises ValueError, changes nothing, and the trip stays open.
    """,
    f"""
    Add Trips.is_open(tid): True until the trip ends. Add tests.

    {RULE}a rider has at most one open trip; starting another raises ValueError and changes nothing.
    """,
    f"""
    Add charge(trips, tid) to pricing.py: the charge of a finished trip, in cents. Add tests.

    {DEC}every trip costs an unlock fee of 100 cents plus 15 cents per minute.
    """,
    f"""
    Add Trips.of_rider(rider): the ids of the rider's trips, in id order. Add tests.

    {DEC}a trip on an e-bike costs 5 cents more per minute.
    """,
    f"""
    Add format_duration(minutes) to pricing.py: the minutes followed by " min", for example "45 min". Add tests.

    {later("format_duration", 'a duration of an hour or more is written as hours and minutes, for example 75 minutes is "1h 15m"; shorter ones stay like "45 min".')}

    {DEC}members ride the first 30 minutes of each trip free of the per-minute charge; they still pay the unlock fee and the e-bike extra.
    """,
    f"""
    Add revenue(trips) to pricing.py: the sum of the charges of the finished trips. Add tests.

    {DEC}a trip longer than 120 minutes also pays a flat overtime fee of 500 cents.
    """,
    f"""
    Add Trips.open_ids(): the ids of the open trips, in id order. Add tests.

    {CHG}the unlock fee is 150 cents, not 100.
    """,
    f"""
    Add export_trips(trips, path) to export.py: a CSV file with one row per finished trip, in id order: id, rider, minutes, charge. Add tests.

    {later("export_trips", "the rows are sorted by rider, and by id for the same rider.")}

    {DEC}an exported trips file starts with the header line id,rider,minutes,charge and uses "," as the delimiter.
    """,
    f"""
    Add Stations.remove(name), which removes a station; an unknown station raises KeyError. Add tests.

    {CHG}the per-minute charge is 20 cents, not 15.
    """,
    f"""
    Add Stations.empty(): the sorted names of the stations with no bikes. Add tests.

    {CHG}members ride the first 45 minutes of each trip free, not 30.
    """,
    f"""
    Add Trips.longest(): the id of the longest finished trip, the smallest id on a tie, or None when no trip has finished. Add tests.

    {CHG}the overtime fee applies to trips longer than 90 minutes, not 120.
    """,
    f"""
    Add Stations.total_bikes(): the number of bikes docked over all stations. Add tests.

    {CHG}a trip on an e-bike costs 8 cents more per minute, not 5.
    """,
    """
    Add Trips.cancel(tid), which cancels an open trip and docks the bike back at its start station. Add tests.
    """,
    f"""
    Add Trips.starts(station): the number of trips that started at the station. Add tests.

    {CHG}the unlock fee is 120 cents, not 150.
    """,
    f"""
    Add Stations.add_bikes(name, n), which docks n more bikes at a station; more bikes than docks raises ValueError and changes nothing. Add tests.

    {CHG}members ride the first 20 minutes of each trip free, not 45.
    """,
    f"""
    Add Trips.riders(): the sorted list of distinct riders. Add tests.

    {CHG}the per-minute charge is 18 cents, not 20.
    """,
    f"""
    Add Trips.total_minutes(rider): the minutes of the rider's finished trips added up. Add tests.

    {CHG}the overtime fee applies to trips longer than 180 minutes, not 90.
    """,
    f"""
    Add Stations.free_docks(name): the capacity of the station minus its bikes. Add tests.

    {CHG}a trip on an e-bike costs 6 cents more per minute, not 8.
    """,
    f"""
    Add Trips.ids(): all trip ids in order. Add tests. {FINISH}
    """],
   '''
    import pytest
    from stations import Stations
    from trips import Trips
    from pricing import charge, format_duration
    from export import export_trips


    def _t():
        s = Stations()
        s.add("North", 5, 3)
        s.add("South", 5, 0)
        return Trips(s)


    def test_basic():
        t = _t()
        i = t.start("Ann", "North", 10, False, False)
        assert i == 1 and t.is_open(i) and t.stations.bikes("North") == 2
        t.end(i, "South", 25)
        assert not t.is_open(i) and t.minutes(i) == 15 and t.stations.bikes("South") == 1
        assert t.stations.capacity("South") == 5
        with pytest.raises(KeyError):
            t.stations.bikes("East")


    def _c(m, ebike=False, member=False):
        t = _t()
        i = t.start("Ann", "North", 0, ebike, member)
        t.end(i, "South", m)
        return charge(t, i)


    def test_fact_unlock_fee():
        assert _c(0) == 120


    def test_stale_unlock_150():
        assert _c(0) == 150


    def test_stale_unlock_100():
        assert _c(0) == 100


    def test_fact_minute_rate():
        assert _c(10) - _c(0) == 180


    def test_stale_rate_20():
        assert _c(10) - _c(0) == 200


    def test_stale_rate_15():
        assert _c(10) - _c(0) == 150


    def test_fact_ebike_extra():
        assert _c(10, True) - _c(10) == 60


    def test_stale_ebike_8():
        assert _c(10, True) - _c(10) == 80


    def test_stale_ebike_5():
        assert _c(10, True) - _c(10) == 50


    def test_fact_member_free():
        assert _c(20, member=True) == _c(0) and _c(21, member=True) > _c(0)


    def test_stale_member_45():
        assert _c(40, member=True) == _c(0)


    def test_stale_member_30():
        assert _c(25, member=True) == _c(0)


    def test_fact_overtime_after():
        d = _c(2) - _c(1)
        assert _c(180) - _c(179) == d and _c(181) - _c(180) > d


    def test_stale_over_90():
        assert _c(91) - _c(90) > _c(2) - _c(1)


    def test_stale_over_120():
        assert _c(121) - _c(120) > _c(2) - _c(1)


    def test_fact_overtime_fee():
        assert _c(181) - _c(180) == _c(2) - _c(1) + 500


    def test_fact_duration_hours():
        assert format_duration(75) == "1h 15m" and format_duration(45) == "45 min"


    def test_fact_no_bike():
        t = _t()
        with pytest.raises(ValueError):
            t.start("Ann", "South", 0)
        assert t.stations.bikes("South") == 0 and t.start("Ann", "North", 0) == 1


    def test_fact_dock_full():
        s = Stations()
        s.add("North", 5, 3)
        s.add("Tiny", 1, 1)
        t = Trips(s)
        i = t.start("Ann", "North", 0)
        with pytest.raises(ValueError):
            t.end(i, "Tiny", 5)
        assert t.is_open(i) and s.bikes("Tiny") == 1


    def test_fact_one_trip():
        t = _t()
        t.start("Ann", "North", 0)
        with pytest.raises(ValueError):
            t.start("Ann", "North", 1)
        assert t.stations.bikes("North") == 2 and t.start("Bob", "North", 1) == 2


    def test_fact_names_sorted():
        s = Stations()
        s.add("north", 5, 0)
        s.add("Bay", 5, 0)
        s.add("Central", 5, 0)
        assert s.names() == ["Bay", "Central", "north"]


    def _rows(t, tmp_path):
        p = tmp_path / "t.csv"
        export_trips(t, str(p))
        return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        t = _t()
        i = t.start("Ann", "North", 0)
        t.end(i, "South", 5)
        rows = _rows(t, tmp_path)
        assert rows[0] == "id,rider,minutes,charge" and rows[1].split(",")[:3] == ["1", "Ann", "5"]


    def test_fact_export_order(tmp_path):
        t = _t()
        t.end(t.start("Zoe", "North", 0), "South", 5)
        t.end(t.start("Ann", "North", 0), "South", 5)
        t.end(t.start("Max", "North", 0), "South", 5)
        assert [x.split(",")[1] for x in _rows(t, tmp_path)[1:]] == ["Ann", "Max", "Zoe"]
    ''',
   {"stations.py": '''
    """Docking stations."""


    class Stations:
        def __init__(self):
            self._s = {}

        def add(self, name, capacity, bikes):
            if bikes > capacity:
                raise ValueError("more bikes than docks")
            self._s[name] = [capacity, bikes]

        def bikes(self, name):
            return self._s[name][1]

        def capacity(self, name):
            return self._s[name][0]

        def names(self):
            return sorted(self._s, key=str.lower)

        def take(self, name):
            if self._s[name][1] == 0:
                raise ValueError("no bikes")
            self._s[name][1] -= 1

        def dock(self, name):
            c, b = self._s[name]
            if b >= c:
                raise ValueError("station full")
            self._s[name][1] += 1

        def remove(self, name):
            del self._s[name]

        def empty(self):
            return sorted(n for n, (_, b) in self._s.items() if b == 0)

        def total_bikes(self):
            return sum(b for _, b in self._s.values())

        def add_bikes(self, name, n):
            c, b = self._s[name]
            if b + n > c:
                raise ValueError("more bikes than docks")
            self._s[name][1] = b + n

        def free_docks(self, name):
            c, b = self._s[name]
            return c - b
    ''',
    "trips.py": '''
    """Trips."""


    class Trips:
        def __init__(self, stations):
            self.stations = stations
            self._t = {}
            self._n = 0

        def start(self, rider, station, t, ebike=False, member=False):
            if any(v["rider"] == rider and v["end"] is None for v in self._t.values()):
                raise ValueError("rider already on a trip")
            self.stations.take(station)
            self._n += 1
            self._t[self._n] = {"rider": rider, "from": station, "start": t, "end": None,
                                "ebike": ebike, "member": member}
            return self._n

        def end(self, tid, station, t):
            v = self._t[tid]
            self.stations.dock(station)
            v["end"] = t

        def get(self, tid):
            return dict(self._t[tid])

        def minutes(self, tid):
            v = self._t[tid]
            return v["end"] - v["start"]

        def is_open(self, tid):
            return self._t[tid]["end"] is None

        def ids(self):
            return list(self._t)

        def of_rider(self, rider):
            return [k for k, v in self._t.items() if v["rider"] == rider]

        def open_ids(self):
            return [k for k in self._t if self.is_open(k)]

        def finished(self):
            return [k for k in self._t if not self.is_open(k)]

        def longest(self):
            f = self.finished()
            return min(f, key=lambda k: (-self.minutes(k), k)) if f else None

        def cancel(self, tid):
            v = self._t[tid]
            if v["end"] is not None:
                raise ValueError("trip already ended")
            self.stations.dock(v["from"])
            del self._t[tid]

        def starts(self, station):
            return sum(v["from"] == station for v in self._t.values())

        def riders(self):
            return sorted({v["rider"] for v in self._t.values()})

        def total_minutes(self, rider):
            return sum(self.minutes(k) for k in self.of_rider(rider) if not self.is_open(k))
    ''',
    "pricing.py": '''
    """Trip charges."""

    UNLOCK = 120
    RATE = 18
    EBIKE = 6
    MEMBER_FREE = 20
    OVER_AFTER = 180
    OVER_FEE = 500


    def charge(trips, tid):
        v = trips.get(tid)
        m = trips.minutes(tid)
        paid = max(0, m - MEMBER_FREE) if v["member"] else m
        c = UNLOCK + paid * RATE
        if v["ebike"]:
            c += m * EBIKE
        if m > OVER_AFTER:
            c += OVER_FEE
        return c


    def format_duration(minutes):
        if minutes >= 60:
            return f"{minutes // 60}h {minutes % 60}m"
        return f"{minutes} min"


    def revenue(trips):
        return sum(charge(trips, k) for k in trips.finished())
    ''',
    "export.py": '''
    """CSV export."""
    import csv

    from pricing import charge


    def export_trips(trips, path):
        ids = sorted(trips.finished(), key=lambda k: (trips.get(k)["rider"], k))
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "rider", "minutes", "charge"])
            for k in ids:
                w.writerow([k, trips.get(k)["rider"], trips.minutes(k), charge(trips, k)])
    '''}, "advanced")

# ---------------------------------------------------------------- A09 pet boarding kennel (21 sessions)
mk("A09", {"dog_rate": "superseded", "cat_rate": "superseded", "large_kg": "superseded",
           "meds_fee": "superseded", "max_nights": "superseded",
           "names_order": "unfinished", "invoice_total": "unfinished", "export_order": "unfinished",
           "species": "constraint", "name_unique": "constraint", "one_stay": "constraint",
           "large_pct": "decision", "export_header": "decision"},
   "Pets and their stays at a boarding kennel. Money is in cents (ints); days are datetime.date; a stay is booked as a check-in day and a number of nights.",
   {"pets.py": '"""The pets."""\n', "stays.py": '"""Stays."""\n', "pricing.py": '"""Stay prices."""\n',
    "export.py": '"""Invoices and CSV export."""\n'},
   [f"""
    Add a Pets class to pets.py with add(name, species, kg), which adds a pet with its weight in kg, species(name), kg(name), and names(): the pet names in the order they were added. An unknown name raises KeyError. Add tests.

    {RULE}the species is "dog" or "cat"; any other species raises ValueError and adds nothing.

    {RULE}pet names are unique; adding a name that is already there raises ValueError and changes nothing.

    {later("Pets.names", "the names are sorted alphabetically.")}
    """,
    f"""
    Add a Stays class to stays.py. Stays(pets) works on a Pets, kept as its attribute pets. book(pet, checkin, nights, meds=False) books a stay and returns a stay id: an int counter that starts at 1; meds says whether the pet needs medicine during the stay. get(sid) returns the stay as a tuple (pet, checkin, nights, meds). An unknown pet or id raises KeyError. Add tests.

    {RULE}a stay covers the nights from its check-in day up to the day before check-in plus nights; two stays of the same pet must not share a night. A booking that would raises ValueError and books nothing.
    """,
    f"""
    Add Stays.checkout(sid): the check-in day plus the nights. Add tests.

    {RULE}a stay is at most 30 nights; a longer one raises ValueError and books nothing.
    """,
    f"""
    Add price(stays, sid) to pricing.py: the price of a stay in cents: the nightly rate times the nights. Add tests.

    {DEC}dogs cost 3000 cents a night and cats 2000 cents a night.
    """,
    f"""
    Add Stays.of_pet(pet): the ids of the pet's stays, in id order. Add tests.

    {DEC}a dog heavier than 25 kg is a large dog; a large dog's nightly rate is 50% more than the dog rate, rounded to the nearest cent.
    """,
    f"""
    Add invoice(stays, sid) to export.py: a list of text lines: "pet: <name>", then "nights: <n>". Add tests.

    {later("invoice", 'it ends with the line "total: <cents>", the price of the stay (for example "total: 6400").')}

    {DEC}a stay with meds also pays a meds fee of 300 cents a night.
    """,
    """
    Add Stays.on_night(day): the ids of the stays that cover the night of day, in id order. Add tests.
    """,
    f"""
    Add export_stays(stays, path) to export.py: a CSV file with one row per stay, in id order: pet, check-in day (ISO) and nights. Add tests.

    {later("export_stays", "the rows are sorted by check-in day, and by pet name for the same day.")}

    {DEC}an exported stays file starts with the header line pet,checkin,nights and uses "," as the delimiter.

    {CHG}dogs cost 3500 cents a night, not 3000.
    """,
    f"""
    Add Pets.remove(name), which removes a pet; an unknown name raises KeyError. Add tests.

    {CHG}a dog is large when it is heavier than 30 kg, not 25.
    """,
    f"""
    Add Stays.cancel(sid), which removes a stay; an unknown id raises KeyError. Add tests.

    {CHG}the meds fee is 500 cents a night, not 300.
    """,
    f"""
    Add revenue(stays) to pricing.py: the sum of the prices of all stays. Add tests.

    {CHG}a stay is at most 21 nights, not 30.
    """,
    f"""
    Add Pets.dogs(): the sorted names of the dogs. Add tests.

    {CHG}cats cost 2400 cents a night, not 2000.
    """,
    f"""
    Add Stays.occupancy(day): the number of stays that cover the night of day. Add tests.

    {CHG}dogs cost 3200 cents a night, not 3500.
    """,
    """
    Add Stays.ids(): all stay ids in order. Add tests.
    """,
    f"""
    Add Pets.set_kg(name, kg), which changes a pet's weight. Add tests.

    {CHG}a dog is large when it is heavier than 20 kg, not 30.
    """,
    f"""
    Add Stays.extend(sid, n), which adds n nights to a stay; the stay rules still apply (a broken rule raises ValueError and changes nothing). Add tests.

    {CHG}the meds fee is 400 cents a night, not 500.
    """,
    """
    Add Stays.nights_total(pet): the nights of all the pet's stays added up. Add tests.
    """,
    f"""
    Add Pets.count(): the number of pets. Add tests.

    {CHG}a stay is at most 28 nights, not 21.
    """,
    """
    Add Stays.pets_on(day): the sorted names of the pets staying the night of day. Add tests.
    """,
    """
    Add Pets.cats(): the sorted names of the cats. Add tests.
    """,
    f"""
    Add Stays.count(): the number of stays. Add tests. {FINISH}
    """],
   '''
    import datetime as dt
    import pytest
    from pets import Pets
    from stays import Stays
    from pricing import price
    from export import invoice, export_stays

    D1 = dt.date(2026, 7, 1)


    def _s():
        p = Pets()
        p.add("Rex", "dog", 10)
        p.add("Tom", "cat", 4)
        return Stays(p)


    def test_basic():
        s = _s()
        assert s.pets.species("Tom") == "cat" and s.pets.kg("Rex") == 10
        i = s.book("Rex", D1, 3)
        assert i == 1 and s.get(i) == ("Rex", D1, 3, False) and s.checkout(i) == D1 + dt.timedelta(3)
        with pytest.raises(KeyError):
            s.get(7)
        with pytest.raises(KeyError):
            s.book("Nemo", D1, 1)


    def _p(species, kg, nights=1, meds=False):
        p = Pets()
        p.add("P", species, kg)
        s = Stays(p)
        return price(s, s.book("P", D1, nights, meds))


    def test_fact_dog_rate():
        assert _p("dog", 10) == 3200


    def test_stale_dog_3500():
        assert _p("dog", 10) == 3500


    def test_stale_dog_3000():
        assert _p("dog", 10) == 3000


    def test_fact_cat_rate():
        assert _p("cat", 4) == 2400


    def test_stale_cat_2000():
        assert _p("cat", 4) == 2000


    def test_fact_large_kg():
        assert _p("dog", 20) == _p("dog", 10) and _p("dog", 21) > _p("dog", 10)


    def test_stale_large_30():
        assert _p("dog", 30) == _p("dog", 10)


    def test_stale_large_25():
        assert _p("dog", 25) == _p("dog", 10)


    def test_fact_large_pct():
        assert _p("dog", 40) == round(_p("dog", 10) * 150 / 100)


    def test_fact_meds_fee():
        assert _p("dog", 10, 1, True) - _p("dog", 10) == 400


    def test_stale_meds_500():
        assert _p("dog", 10, 1, True) - _p("dog", 10) == 500


    def test_stale_meds_300():
        assert _p("dog", 10, 1, True) - _p("dog", 10) == 300


    def _nights_ok(n):
        s = _s()
        try:
            s.book("Rex", D1, n)
            return True
        except ValueError:
            assert s.of_pet("Rex") == []
            return False


    def test_fact_max_nights():
        assert _nights_ok(28) and not _nights_ok(29)


    def test_stale_nights_21():
        assert not _nights_ok(22)


    def test_stale_nights_30():
        assert _nights_ok(30)


    def test_fact_species():
        p = Pets()
        with pytest.raises(ValueError):
            p.add("Polly", "bird", 1)
        assert p.names() == []


    def test_fact_name_unique():
        p = Pets()
        p.add("Rex", "dog", 10)
        with pytest.raises(ValueError):
            p.add("Rex", "cat", 3)
        assert p.species("Rex") == "dog" and len(p.names()) == 1


    def test_fact_one_stay():
        s = _s()
        s.book("Rex", D1, 3)
        with pytest.raises(ValueError):
            s.book("Rex", D1 + dt.timedelta(2), 2)
        assert s.book("Rex", D1 + dt.timedelta(3), 2) == 2 and s.of_pet("Rex") == [1, 2]


    def test_fact_names_order():
        p = Pets()
        p.add("Zoe", "dog", 5)
        p.add("Ann", "cat", 3)
        p.add("Max", "dog", 7)
        assert p.names() == ["Ann", "Max", "Zoe"]


    def test_fact_invoice_total():
        s = _s()
        i = s.book("Rex", D1, 2)
        lines = [x.strip() for x in invoice(s, i)]
        assert len(lines) == 3 and lines[2] == f"total: {price(s, i)}"


    def _rows(s, tmp_path):
        p = tmp_path / "s.csv"
        export_stays(s, str(p))
        return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        s = _s()
        s.book("Rex", D1, 3)
        rows = _rows(s, tmp_path)
        assert rows[0] == "pet,checkin,nights" and rows[1].split(",")[2] == "3"


    def test_fact_export_order(tmp_path):
        p = Pets()
        p.add("Zoe", "dog", 5)
        p.add("Max", "cat", 3)
        p.add("Ann", "dog", 7)
        s = Stays(p)
        s.book("Zoe", D1, 1)
        s.book("Max", D1 + dt.timedelta(1), 1)
        s.book("Ann", D1 + dt.timedelta(1), 1)
        assert [x.split(",")[0] for x in _rows(s, tmp_path)[1:]] == ["Zoe", "Ann", "Max"]
    ''',
   {"pets.py": '''
    """The pets."""


    class Pets:
        def __init__(self):
            self._p = {}

        def add(self, name, species, kg):
            if species not in ("dog", "cat"):
                raise ValueError(f"bad species {species!r}")
            if name in self._p:
                raise ValueError(f"{name} is already there")
            self._p[name] = [species, kg]

        def species(self, name):
            return self._p[name][0]

        def kg(self, name):
            return self._p[name][1]

        def set_kg(self, name, kg):
            self._p[name][1] = kg

        def names(self):
            return sorted(self._p)

        def remove(self, name):
            del self._p[name]

        def dogs(self):
            return sorted(n for n, v in self._p.items() if v[0] == "dog")

        def cats(self):
            return sorted(n for n, v in self._p.items() if v[0] == "cat")

        def count(self):
            return len(self._p)
    ''',
    "stays.py": '''
    """Stays."""
    import datetime as dt

    MAX_NIGHTS = 28


    class Stays:
        def __init__(self, pets):
            self.pets = pets
            self._s = {}
            self._n = 0

        def _check(self, pet, checkin, nights, skip=None):
            self.pets.species(pet)
            if nights > MAX_NIGHTS:
                raise ValueError("stay too long")
            end = checkin + dt.timedelta(nights)
            for k, (p, c, n, _) in self._s.items():
                if k != skip and p == pet and checkin < c + dt.timedelta(n) and c < end:
                    raise ValueError("stays overlap")

        def book(self, pet, checkin, nights, meds=False):
            self._check(pet, checkin, nights)
            self._n += 1
            self._s[self._n] = (pet, checkin, nights, meds)
            return self._n

        def get(self, sid):
            return self._s[sid]

        def checkout(self, sid):
            _, c, n, _ = self._s[sid]
            return c + dt.timedelta(n)

        def ids(self):
            return list(self._s)

        def count(self):
            return len(self._s)

        def of_pet(self, pet):
            return [k for k, v in self._s.items() if v[0] == pet]

        def on_night(self, day):
            return [k for k, (_, c, n, _) in self._s.items() if c <= day < c + dt.timedelta(n)]

        def occupancy(self, day):
            return len(self.on_night(day))

        def pets_on(self, day):
            return sorted(self._s[k][0] for k in self.on_night(day))

        def cancel(self, sid):
            del self._s[sid]

        def extend(self, sid, n):
            p, c, old, m = self._s[sid]
            self._check(p, c, old + n, skip=sid)
            self._s[sid] = (p, c, old + n, m)

        def nights_total(self, pet):
            return sum(self._s[k][2] for k in self.of_pet(pet))
    ''',
    "pricing.py": '''
    """Stay prices."""

    DOG = 3200
    CAT = 2400
    LARGE_KG = 20
    LARGE_PCT = 50
    MEDS = 400


    def nightly(pets, name):
        if pets.species(name) == "cat":
            return CAT
        if pets.kg(name) > LARGE_KG:
            return round(DOG * (100 + LARGE_PCT) / 100)
        return DOG


    def price(stays, sid):
        pet, _, nights, meds = stays.get(sid)
        return nights * (nightly(stays.pets, pet) + (MEDS if meds else 0))


    def revenue(stays):
        return sum(price(stays, k) for k in stays.ids())
    ''',
    "export.py": '''
    """Invoices and CSV export."""
    import csv

    from pricing import price


    def invoice(stays, sid):
        pet, _, nights, _ = stays.get(sid)
        return [f"pet: {pet}", f"nights: {nights}", f"total: {price(stays, sid)}"]


    def export_stays(stays, path):
        ids = sorted(stays.ids(), key=lambda k: (stays.get(k)[1], stays.get(k)[0]))
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["pet", "checkin", "nights"])
            for k in ids:
                pet, c, n, _ = stays.get(k)
                w.writerow([pet, c.isoformat(), n])
    '''}, "advanced")

# ---------------------------------------------------------------- A10 greenhouse plant care (21 sessions)
mk("A10", {"herb_days": "superseded", "cactus_days": "superseded", "fern_days": "superseded",
           "feed_days": "superseded", "alarm_temp": "superseded",
           "due_order": "unfinished", "label_caps": "unfinished", "export_order": "unfinished",
           "kind": "constraint", "water_order": "constraint", "feed_on_water": "constraint",
           "never_watered": "decision", "export_header": "decision"},
   "A care log for the plants in a greenhouse: when each plant was watered and fed, and when it is due next. Days are datetime.date.",
   {"plants.py": '"""The plants."""\n', "care.py": '"""The watering and feeding log."""\n',
    "schedule.py": '"""When plants are due."""\n', "export.py": '"""Labels and CSV export."""\n'},
   [f"""
    Add a Plants class to plants.py with add(name, kind, day), which adds a plant on day, kind(name), added(name), the day it was added, and names(): the plant names in the order they were added. An unknown name raises KeyError. Add tests.

    {RULE}the kind is "herb", "cactus" or "fern"; any other kind raises ValueError and adds nothing.
    """,
    f"""
    Add a Care class to care.py. Care(plants) works on a Plants, kept as its attribute plants. water(name, day) records a watering; waterings(name) is the list of its watering days in the order recorded. An unknown plant raises KeyError. Add tests.

    {RULE}a watering is never on a day before the plant's last watering (the same day is fine); an earlier day raises ValueError and records nothing.
    """,
    f"""
    Add next_water(care, name) to schedule.py: the day the plant needs water next: its last watering day plus the watering interval of its kind. Add tests.

    {DEC}herbs are watered every 2 days, cacti every 14 days and ferns every 4 days.

    {DEC}a plant that was never watered is due on the day it was added.
    """,
    f"""
    Add Care.feed(name, day), which records a feeding, and Care.feedings(name), the list of its feeding days in order. Add tests.

    {RULE}a plant can only be fed on a day it was watered; feeding it on any other day raises ValueError and records nothing.
    """,
    f"""
    Add next_feed(care, name) to schedule.py: the last feeding day plus the feeding interval; a plant that was never fed is due on the day it was added. Add tests.

    {DEC}every plant is fed every 30 days.
    """,
    f"""
    Add due(care, day) to schedule.py: the names of the plants whose next watering day is on or before day, in the order the plants were added. Add tests.

    {later("due", "the names are sorted by next watering day, and by name for the same day.")}
    """,
    f"""
    Add alarm(temp) to schedule.py: True when the greenhouse temperature temp (whole °C) is too cold. Add tests.

    {DEC}the alarm sounds below 5 °C.
    """,
    f"""
    Add label(plants, name) to export.py: the text "<name> (<kind>)", for example "Basil (herb)". Add tests.

    {later("label", 'the kind is written in capitals, as in "Basil (HERB)".')}

    {CHG}herbs are watered every 3 days, not 2.
    """,
    f"""
    Add Plants.remove(name), which removes a plant; an unknown name raises KeyError. Add tests.

    {CHG}cacti are watered every 10 days, not 14.
    """,
    f"""
    Add export_plan(care, path) to export.py: a CSV file with one row per plant, in the order the plants were added: name, kind and next watering day (ISO). Add tests.

    {later("export_plan", "the rows are sorted by plant name.")}

    {DEC}an exported plan file starts with the header line plant,kind,next and uses "," as the delimiter.
    """,
    f"""
    Add Care.last_watered(name): the last watering day, or None. Add tests.

    {CHG}ferns are watered every 3 days, not 4.
    """,
    f"""
    Add Plants.of_kind(kind): the sorted names of the plants of that kind. Add tests.

    {CHG}every plant is fed every 21 days, not 30.
    """,
    f"""
    Add Care.count(name): the number of waterings of the plant. Add tests.

    {CHG}the alarm sounds below 8 °C, not 5.
    """,
    f"""
    Add overdue_days(care, name, day) to schedule.py: how many days day is past the next watering day, or 0 when it is not past. Add tests.

    {CHG}cacti are watered every 21 days, not 10.
    """,
    """
    Add Care.undo_water(name), which removes the plant's last watering; a plant with no waterings raises KeyError. Add tests.
    """,
    f"""
    Add Plants.set_kind(name, kind), which changes a plant's kind; the kind rule still applies. Add tests.

    {CHG}ferns are watered every 5 days, not 3.
    """,
    """
    Add Care.watered_on(day): the sorted names of the plants watered on day. Add tests.
    """,
    f"""
    Add Plants.count(): the number of plants. Add tests.

    {CHG}every plant is fed every 28 days, not 21.
    """,
    f"""
    Add Care.total_waterings(): the number of waterings over all plants. Add tests.

    {CHG}the alarm sounds below 6 °C, not 8.
    """,
    """
    Add Plants.kinds(): the sorted list of distinct kinds in use. Add tests.
    """,
    f"""
    Add Care.first_watered(name): the first watering day, or None. Add tests. {FINISH}
    """],
   '''
    import datetime as dt
    import pytest
    from plants import Plants
    from care import Care
    from schedule import next_water, next_feed, due, alarm
    from export import label, export_plan

    D0 = dt.date(2026, 4, 1)


    def _days(d):
        return (d - D0).days


    def _c():
        p = Plants()
        p.add("Basil", "herb", D0)
        p.add("Aloe", "cactus", D0)
        return Care(p)


    def test_basic():
        c = _c()
        assert c.plants.kind("Aloe") == "cactus" and c.plants.added("Basil") == D0
        c.water("Basil", D0)
        c.water("Basil", D0 + dt.timedelta(1))
        assert c.waterings("Basil") == [D0, D0 + dt.timedelta(1)] and c.waterings("Aloe") == []
        with pytest.raises(KeyError):
            c.water("Oak", D0)


    def _gap(kind):
        p = Plants()
        p.add("P", kind, D0)
        c = Care(p)
        c.water("P", D0)
        return _days(next_water(c, "P"))


    def test_fact_herb_days():
        assert _gap("herb") == 3


    def test_stale_herb_2():
        assert _gap("herb") == 2


    def test_fact_cactus_days():
        assert _gap("cactus") == 21


    def test_stale_cactus_10():
        assert _gap("cactus") == 10


    def test_stale_cactus_14():
        assert _gap("cactus") == 14


    def test_fact_fern_days():
        assert _gap("fern") == 5


    def test_stale_fern_3():
        assert _gap("fern") == 3


    def test_stale_fern_4():
        assert _gap("fern") == 4


    def _feed():
        c = _c()
        c.water("Basil", D0)
        c.feed("Basil", D0)
        return _days(next_feed(c, "Basil"))


    def test_fact_feed_days():
        assert _feed() == 28


    def test_stale_feed_21():
        assert _feed() == 21


    def test_stale_feed_30():
        assert _feed() == 30


    def test_fact_alarm_temp():
        assert alarm(5) and not alarm(6)


    def test_stale_alarm_8():
        assert alarm(7)


    def test_stale_alarm_5():
        assert not alarm(5)


    def test_fact_never_watered():
        p = Plants()
        p.add("P", "fern", D0 + dt.timedelta(4))
        c = Care(p)
        assert _days(next_water(c, "P")) == 4 and _days(next_feed(c, "P")) == 4


    def test_fact_kind():
        p = Plants()
        with pytest.raises(ValueError):
            p.add("Oak", "tree", D0)
        assert p.names() == []


    def test_fact_water_order():
        c = _c()
        c.water("Basil", D0 + dt.timedelta(5))
        with pytest.raises(ValueError):
            c.water("Basil", D0 + dt.timedelta(4))
        c.water("Basil", D0 + dt.timedelta(5))
        assert len(c.waterings("Basil")) == 2


    def test_fact_feed_on_water():
        c = _c()
        c.water("Basil", D0)
        with pytest.raises(ValueError):
            c.feed("Basil", D0 + dt.timedelta(1))
        c.feed("Basil", D0)
        assert c.feedings("Basil") == [D0]


    def test_fact_due_order():
        p = Plants()
        p.add("Zed", "herb", D0 + dt.timedelta(1))
        p.add("Bo", "fern", D0)
        p.add("Amy", "herb", D0)
        assert due(Care(p), D0 + dt.timedelta(5)) == ["Amy", "Bo", "Zed"]


    def test_fact_label_caps():
        assert label(_c().plants, "Basil").strip() == "Basil (HERB)"


    def _rows(c, tmp_path):
        p = tmp_path / "p.csv"
        export_plan(c, str(p))
        return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        rows = _rows(_c(), tmp_path)
        assert rows[0] == "plant,kind,next" and len(rows) == 3


    def test_fact_export_order(tmp_path):
        p = Plants()
        p.add("Zed", "herb", D0)
        p.add("Amy", "fern", D0)
        p.add("Bo", "herb", D0)
        assert [x.split(",")[0] for x in _rows(Care(p), tmp_path)[1:]] == ["Amy", "Bo", "Zed"]
    ''',
   {"plants.py": '''
    """The plants."""

    KINDS = ("herb", "cactus", "fern")


    class Plants:
        def __init__(self):
            self._p = {}

        def add(self, name, kind, day):
            if kind not in KINDS:
                raise ValueError(f"bad kind {kind!r}")
            self._p[name] = [kind, day]

        def kind(self, name):
            return self._p[name][0]

        def set_kind(self, name, kind):
            self._p[name]
            if kind not in KINDS:
                raise ValueError(f"bad kind {kind!r}")
            self._p[name][0] = kind

        def added(self, name):
            return self._p[name][1]

        def names(self):
            return list(self._p)

        def remove(self, name):
            del self._p[name]

        def of_kind(self, kind):
            return sorted(n for n, v in self._p.items() if v[0] == kind)

        def count(self):
            return len(self._p)

        def kinds(self):
            return sorted({v[0] for v in self._p.values()})
    ''',
    "care.py": '''
    """The watering and feeding log."""


    class Care:
        def __init__(self, plants):
            self.plants = plants
            self._w = {}
            self._f = {}

        def water(self, name, day):
            self.plants.kind(name)
            w = self._w.setdefault(name, [])
            if w and day < w[-1]:
                raise ValueError("watering before the last one")
            w.append(day)

        def waterings(self, name):
            self.plants.kind(name)
            return list(self._w.get(name, []))

        def feed(self, name, day):
            if day not in self.waterings(name):
                raise ValueError("feed only on a watering day")
            self._f.setdefault(name, []).append(day)

        def feedings(self, name):
            self.plants.kind(name)
            return list(self._f.get(name, []))

        def last_watered(self, name):
            w = self.waterings(name)
            return w[-1] if w else None

        def first_watered(self, name):
            w = self.waterings(name)
            return w[0] if w else None

        def count(self, name):
            return len(self.waterings(name))

        def undo_water(self, name):
            if not self._w.get(name):
                raise KeyError(name)
            self._w[name].pop()

        def watered_on(self, day):
            return sorted(n for n, w in self._w.items() if day in w)

        def total_waterings(self):
            return sum(len(w) for w in self._w.values())
    ''',
    "schedule.py": '''
    """When plants are due."""
    import datetime as dt

    WATER = {"herb": 3, "cactus": 21, "fern": 5}
    FEED = 28
    ALARM_BELOW = 6


    def next_water(care, name):
        last = care.last_watered(name)
        if last is None:
            return care.plants.added(name)
        return last + dt.timedelta(WATER[care.plants.kind(name)])


    def next_feed(care, name):
        f = care.feedings(name)
        if not f:
            return care.plants.added(name)
        return f[-1] + dt.timedelta(FEED)


    def due(care, day):
        names = [n for n in care.plants.names() if next_water(care, n) <= day]
        return sorted(names, key=lambda n: (next_water(care, n), n))


    def alarm(temp):
        return temp < ALARM_BELOW


    def overdue_days(care, name, day):
        return max(0, (day - next_water(care, name)).days)
    ''',
    "export.py": '''
    """Labels and CSV export."""
    import csv

    from schedule import next_water


    def label(plants, name):
        return f"{name} ({plants.kind(name).upper()})"


    def export_plan(care, path):
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["plant", "kind", "next"])
            for n in sorted(care.plants.names()):
                w.writerow([n, care.plants.kind(n), next_water(care, n).isoformat()])
    '''}, "advanced")

# ---------------------------------------------------------------- A11 conference programme (21 sessions)
mk("A11", {"max_minutes": "superseded", "room_gap": "superseded", "per_speaker": "superseded",
           "ticket_price": "superseded", "student_pct": "superseded",
           "agenda_order": "unfinished", "time_pad": "unfinished", "export_order": "unfinished",
           "room_exists": "constraint", "hours": "constraint", "kind_known": "constraint",
           "speaker_free": "decision", "export_header": "decision"},
   "Rooms, talks and ticket prices for a one-day conference. Times are int minutes from midnight (540 is 9:00); money is in cents (ints).",
   {"rooms.py": '"""Rooms."""\n', "talks.py": '"""Talks."""\n', "tickets.py": '"""Ticket prices."""\n',
    "export.py": '"""Times and CSV export."""\n'},
   [f"""
    Add a Rooms class to rooms.py with add(name, seats), seats(name), and names(): the room names in the order they were added. An unknown room raises KeyError. Add tests.
    """,
    f"""
    Add a Talks class to talks.py. Talks(rooms) works on a Rooms, kept as its attribute rooms. add(title, speaker, room, start, minutes) adds a talk and returns a talk id: an int counter that starts at 1. get(tid) returns the talk as a tuple (title, speaker, room, start, minutes); an unknown id raises KeyError. Add tests.

    {RULE}the room must be one of the rooms; any other room raises ValueError and adds nothing.

    {RULE}a talk starts at 480 or later and ends (start plus minutes) at 1080 or earlier; any other talk raises ValueError and adds nothing.
    """,
    f"""
    Add Talks.agenda(room): the ids of the talks in the room, in the order they were added. Add tests.

    {later("Talks.agenda", "the ids are sorted by start time.")}
    """,
    f"""
    Add Talks.end(tid): the start plus the minutes. Add tests.

    {RULE}a talk is at most 45 minutes long; a longer talk raises ValueError and adds nothing.
    """,
    f"""
    Add Talks.room_talks(room): the number of talks in the room. Add tests.

    {RULE}talks in the same room do not overlap, and there are at least 10 minutes between the end of one and the start of the next; a talk that breaks this raises ValueError and adds nothing.
    """,
    f"""
    Add fmt_time(minutes) to export.py: the time as "H:MM", for example 1005 is "16:45" and 540 is "9:00". Add tests.

    {later("fmt_time", 'hours are always written with two digits, so 540 is "09:00".')}
    """,
    f"""
    Add ticket_price(kind) to tickets.py: the price of a ticket of kind "regular", "student" or "speaker", in cents. Add tests.

    {RULE}any other kind raises ValueError.

    {DEC}a regular ticket costs 20000 cents and students pay 50% of the regular price, rounded to the nearest cent.

    {DEC}speakers get their ticket free: a speaker ticket costs 0.
    """,
    f"""
    Add Talks.of_speaker(speaker): the ids of the speaker's talks, in id order. Add tests.

    {RULE}a speaker gives at most 2 talks; one more raises ValueError and adds nothing.
    """,
    f"""
    Add Talks.remove(tid), which removes a talk; an unknown id raises KeyError. Add tests.

    {CHG}a talk is at most 30 minutes long, not 45.
    """,
    f"""
    Add export_programme(talks, path) to export.py: a CSV file with one row per talk, in id order: the start (as fmt_time writes it), the room and the title. Add tests.

    {later("export_programme", "the rows are sorted by start time, and by room for the same start.")}

    {DEC}an exported programme file starts with the header line start,room,title and uses "," as the delimiter.
    """,
    f"""
    Add Rooms.remove(name), which removes a room; an unknown room raises KeyError. Add tests.

    {CHG}there are at least 15 minutes between talks in the same room, not 10.
    """,
    f"""
    Add Talks.move(tid, start), which moves a talk to a new start time; all the talk rules still apply (a broken rule raises ValueError and changes nothing). Add tests.

    {CHG}a regular ticket costs 25000 cents, not 20000.
    """,
    f"""
    Add Talks.speakers(): the sorted list of distinct speakers. Add tests.

    {CHG}a speaker gives at most 3 talks, not 2.
    """,
    f"""
    Add Rooms.capacity(): the seats of all rooms added up. Add tests.

    {CHG}students pay 40% of the regular price, not 50%.
    """,
    f"""
    Add Talks.minutes_in(room): the minutes of the talks in the room added up. Add tests.

    {CHG}a talk is at most 40 minutes long, not 30.
    """,
    """
    Add Talks.at(minute): the ids of the talks running at that minute (start <= minute < end), in id order. Add tests.
    """,
    f"""
    Add Talks.count(): the number of talks. Add tests.

    {CHG}there are at least 5 minutes between talks in the same room, not 15.
    """,
    """
    Add Talks.free_after(room): the end of the last talk in the room, or 480 when the room has no talks. Add tests.
    """,
    f"""
    Add Talks.rename(tid, title), which changes a talk's title. Add tests.

    {CHG}a regular ticket costs 22000 cents, not 25000.
    """,
    """
    Add Rooms.count(): the number of rooms. Add tests.
    """,
    f"""
    Add Talks.ids(): all talk ids in order. Add tests. {FINISH}
    """],
   '''
    import pytest
    from rooms import Rooms
    from talks import Talks
    from tickets import ticket_price
    from export import fmt_time, export_programme


    def _t():
        r = Rooms()
        r.add("Hall", 200)
        r.add("Lab", 30)
        return Talks(r)


    def test_basic():
        t = _t()
        assert t.rooms.seats("Lab") == 30 and t.rooms.names() == ["Hall", "Lab"]
        i = t.add("Intro", "Ann", "Hall", 540, 20)
        assert i == 1 and t.get(i) == ("Intro", "Ann", "Hall", 540, 20) and t.end(i) == 560
        with pytest.raises(KeyError):
            t.get(9)
        with pytest.raises(KeyError):
            t.rooms.seats("Attic")


    def _len_ok(m):
        t = _t()
        try:
            t.add("T", "Ann", "Hall", 600, m)
            return True
        except ValueError:
            assert t.room_talks("Hall") == 0
            return False


    def test_fact_max_minutes():
        assert _len_ok(40) and not _len_ok(41)


    def test_stale_max_30():
        assert not _len_ok(31)


    def test_stale_max_45():
        assert _len_ok(45)


    def _gap_ok(g):
        t = _t()
        t.add("A", "Ann", "Hall", 600, 30)
        try:
            t.add("B", "Bob", "Hall", 630 + g, 30)
            return True
        except ValueError:
            assert t.room_talks("Hall") == 1
            return False


    def test_fact_room_gap():
        assert _gap_ok(5) and not _gap_ok(4)


    def test_stale_gap_15():
        assert not _gap_ok(10)


    def test_stale_gap_10():
        assert not _gap_ok(9)


    def _speaker_ok(n):
        t = _t()
        for k in range(n - 1):
            t.add("T", "Ann", "Hall", 500 + 50 * k, 20)
        try:
            t.add("T", "Ann", "Lab", 500, 20)
            return True
        except ValueError:
            assert len(t.of_speaker("Ann")) == n - 1
            return False


    def test_fact_per_speaker():
        assert _speaker_ok(3) and not _speaker_ok(4)


    def test_stale_speaker_2():
        assert not _speaker_ok(3)


    def test_fact_ticket_price():
        assert ticket_price("regular") == 22000


    def test_stale_price_25000():
        assert ticket_price("regular") == 25000


    def test_stale_price_20000():
        assert ticket_price("regular") == 20000


    def test_fact_student_pct():
        assert ticket_price("student") == round(ticket_price("regular") * 40 / 100)


    def test_stale_student_50():
        assert ticket_price("student") == round(ticket_price("regular") * 50 / 100)


    def test_fact_speaker_free():
        assert ticket_price("speaker") == 0


    def test_fact_kind_known():
        with pytest.raises(ValueError):
            ticket_price("vip")


    def test_fact_room_exists():
        t = _t()
        with pytest.raises(ValueError):
            t.add("T", "Ann", "Attic", 600, 20)
        assert t.speakers() == []


    def test_fact_hours():
        t = _t()
        for start, m in ((470, 20), (1060, 30)):
            with pytest.raises(ValueError):
                t.add("T", "Ann", "Hall", start, m)
        t.add("T", "Ann", "Hall", 1050, 30)
        t.add("U", "Bob", "Lab", 480, 20)
        assert t.room_talks("Hall") == 1


    def test_fact_agenda_order():
        t = _t()
        t.add("A", "Ann", "Hall", 900, 20)
        t.add("B", "Bob", "Hall", 600, 20)
        t.add("C", "Cy", "Hall", 700, 20)
        assert t.agenda("Hall") == [2, 3, 1]


    def test_fact_time_pad():
        assert fmt_time(540) == "09:00" and fmt_time(1005) == "16:45"


    def _rows(t, tmp_path):
        p = tmp_path / "p.csv"
        export_programme(t, str(p))
        return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        t = _t()
        t.add("Intro", "Ann", "Hall", 600, 20)
        rows = _rows(t, tmp_path)
        assert rows[0] == "start,room,title" and rows[1].split(",")[1:] == ["Hall", "Intro"]


    def test_fact_export_order(tmp_path):
        t = _t()
        t.add("A", "Ann", "Lab", 900, 20)
        t.add("B", "Bob", "Lab", 600, 20)
        t.add("C", "Cy", "Hall", 600, 20)
        assert [x.split(",")[2] for x in _rows(t, tmp_path)[1:]] == ["C", "B", "A"]
    ''',
   {"rooms.py": '''
    """Rooms."""


    class Rooms:
        def __init__(self):
            self._r = {}

        def add(self, name, seats):
            self._r[name] = seats

        def seats(self, name):
            return self._r[name]

        def names(self):
            return list(self._r)

        def remove(self, name):
            del self._r[name]

        def capacity(self):
            return sum(self._r.values())

        def count(self):
            return len(self._r)
    ''',
    "talks.py": '''
    """Talks."""

    OPEN, CLOSE = 480, 1080
    MAX_MIN = 40
    GAP = 5
    PER_SPEAKER = 3


    class Talks:
        def __init__(self, rooms):
            self.rooms = rooms
            self._t = {}
            self._n = 0

        def _check(self, speaker, room, start, minutes, skip=None):
            if room not in self.rooms.names():
                raise ValueError(f"no room {room!r}")
            if start < OPEN or start + minutes > CLOSE:
                raise ValueError("outside the day")
            if minutes > MAX_MIN:
                raise ValueError("talk too long")
            for k, (_, s, r, st, m) in self._t.items():
                if k == skip or r != room:
                    continue
                if start < st + m + GAP and st < start + minutes + GAP:
                    raise ValueError("too close to another talk")
            if sum(v[1] == speaker for k, v in self._t.items() if k != skip) >= PER_SPEAKER:
                raise ValueError("speaker has too many talks")

        def add(self, title, speaker, room, start, minutes):
            self._check(speaker, room, start, minutes)
            self._n += 1
            self._t[self._n] = (title, speaker, room, start, minutes)
            return self._n

        def get(self, tid):
            return self._t[tid]

        def end(self, tid):
            v = self._t[tid]
            return v[3] + v[4]

        def ids(self):
            return list(self._t)

        def count(self):
            return len(self._t)

        def agenda(self, room):
            return sorted((k for k, v in self._t.items() if v[2] == room), key=lambda k: self._t[k][3])

        def room_talks(self, room):
            return len(self.agenda(room))

        def of_speaker(self, speaker):
            return [k for k, v in self._t.items() if v[1] == speaker]

        def remove(self, tid):
            del self._t[tid]

        def move(self, tid, start):
            title, s, r, _, m = self._t[tid]
            self._check(s, r, start, m, skip=tid)
            self._t[tid] = (title, s, r, start, m)

        def speakers(self):
            return sorted({v[1] for v in self._t.values()})

        def minutes_in(self, room):
            return sum(v[4] for v in self._t.values() if v[2] == room)

        def at(self, minute):
            return [k for k, v in self._t.items() if v[3] <= minute < v[3] + v[4]]

        def free_after(self, room):
            a = self.agenda(room)
            return max(self.end(k) for k in a) if a else OPEN

        def rename(self, tid, title):
            _, s, r, st, m = self._t[tid]
            self._t[tid] = (title, s, r, st, m)
    ''',
    "tickets.py": '''
    """Ticket prices."""

    REGULAR = 22000
    STUDENT_PCT = 40


    def ticket_price(kind):
        if kind == "regular":
            return REGULAR
        if kind == "student":
            return round(REGULAR * STUDENT_PCT / 100)
        if kind == "speaker":
            return 0
        raise ValueError(f"unknown kind {kind!r}")
    ''',
    "export.py": '''
    """Times and CSV export."""
    import csv


    def fmt_time(minutes):
        return f"{minutes // 60:02d}:{minutes % 60:02d}"


    def export_programme(talks, path):
        ids = sorted(talks.ids(), key=lambda k: (talks.get(k)[3], talks.get(k)[2]))
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["start", "room", "title"])
            for k in ids:
                title, _, room, start, _ = talks.get(k)
                w.writerow([fmt_time(start), room, title])
    '''}, "advanced")

# ---------------------------------------------------------------- A12 chess league (21 sessions)
mk("A12", {"win_pts": "superseded", "k_factor": "superseded", "rating_floor": "superseded",
           "provisional": "superseded", "entry_fee": "superseded",
           "names_order": "unfinished", "score_line": "unfinished", "export_order": "unfinished",
           "result_valid": "constraint", "not_self": "constraint", "pair_limit": "constraint",
           "draw_pts": "decision", "export_header": "decision"},
   "Players, games and standings for a club chess league. A result is \"1-0\" (white won), \"0-1\" (black won) or \"1/2\" (a draw); ratings are ints.",
   {"players.py": '"""The players."""\n', "games.py": '"""Games."""\n', "standings.py": '"""Points and standings."""\n',
    "export.py": '"""Result lines and CSV export."""\n'},
   [f"""
    Add a Players class to players.py with add(name, rating), rating(name), and names(): the player names in the order they were added. An unknown name raises KeyError. Add tests.

    {later("Players.names", "the names are sorted by rating, highest first, and by name for the same rating.")}
    """,
    f"""
    Add a Games class to games.py. Games(players) works on a Players, kept as its attribute players. record(white, black, result) records a game and returns a game id: an int counter that starts at 1. get(gid) returns the game as a tuple (white, black, result). An unknown player or id raises KeyError. Add tests.

    {RULE}the result is "1-0", "0-1" or "1/2"; any other result raises ValueError and records nothing.

    {RULE}a player cannot play themselves; such a game raises ValueError and records nothing.
    """,
    f"""
    Add points(games, name) to standings.py: the player's league points. Add tests.

    {DEC}a win gives 2 points, a loss 0, and a draw gives each player 1 point.
    """,
    f"""
    Add Games.of_player(name): the ids of the player's games, in id order. Add tests.

    {RULE}two players meet at most twice, whoever has white; a third game between them raises ValueError and records nothing.
    """,
    f"""
    Make Games.record update the players' ratings. Add tests.

    {DEC}after a decisive game the winner gains 32 rating points and the loser loses 32; a draw changes no rating.
    """,
    f"""
    Add result_text(games, gid) to export.py: the text "<white> - <black>: <result>", for example "Ann - Bob: 1-0". Add tests.

    {later("result_text", 'a draw is written as the word draw, as in "Ann - Bob: draw".')}
    """,
    f"""
    Add Players.set_rating(name, rating), which sets a player's rating. Add tests.

    {RULE}a loss never takes a rating below 100; the rating stops at 100.
    """,
    f"""
    Add is_provisional(games, name) to standings.py. Add tests.

    {DEC}a player with fewer than 5 games is provisional.
    """,
    f"""
    Add entry_fee() to standings.py: the league entry fee in cents. Add tests.

    {DEC}the entry fee is 1500 cents.

    {CHG}a win gives 3 points, not 2.
    """,
    f"""
    Add export_table(games, path) to export.py: a CSV file with one row per player, in the order of Players.names: name, points and rating. Add tests.

    {later("export_table", "the rows are sorted by points, highest first, and by name for the same points.")}

    {DEC}an exported table starts with the header line name,points,rating and uses "," as the delimiter.
    """,
    f"""
    Add Players.remove(name), which removes a player; an unknown name raises KeyError. Add tests.

    {CHG}the winner gains 20 rating points and the loser loses 20, not 32.
    """,
    f"""
    Add Games.count(): the number of games. Add tests.

    {CHG}a player with fewer than 10 games is provisional, not 5.
    """,
    f"""
    Add table(games) to standings.py: a list of (name, points) tuples in the order of Players.names. Add tests.

    {CHG}a loss never takes a rating below 400, not 100.
    """,
    f"""
    Add Games.wins(name): the number of games the player won. Add tests.

    {CHG}the entry fee is 2000 cents, not 1500.
    """,
    """
    Add Games.draws(name): the number of the player's drawn games. Add tests.
    """,
    f"""
    Add Games.opponents(name): the sorted names of the players the player has met. Add tests.

    {CHG}the winner gains 24 rating points and the loser loses 24, not 20.
    """,
    f"""
    Add Players.count(): the number of players. Add tests.

    {CHG}a player with fewer than 8 games is provisional, not 10.
    """,
    """
    Add Games.last(): the id of the last game recorded, or None. Add tests.
    """,
    f"""
    Add Games.losses(name): the number of games the player lost. Add tests.

    {CHG}a loss never takes a rating below 300, not 400.
    """,
    f"""
    Add Games.played(name): the number of the player's games. Add tests.

    {CHG}the entry fee is 1800 cents, not 2000.
    """,
    f"""
    Add Games.ids(): all game ids in order. Add tests. {FINISH}
    """],
   '''
    import pytest
    from players import Players
    from games import Games
    from standings import points, is_provisional, entry_fee
    from export import result_text, export_table


    def _g(**ratings):
        p = Players()
        for n, r in (ratings or {"Ann": 1500, "Bob": 1500}).items():
            p.add(n, r)
        return Games(p)


    def test_basic():
        g = _g()
        i = g.record("Ann", "Bob", "1/2")
        assert i == 1 and g.get(i) == ("Ann", "Bob", "1/2") and g.of_player("Bob") == [1]
        with pytest.raises(KeyError):
            g.get(4)
        with pytest.raises(KeyError):
            g.record("Ann", "Cy", "1-0")


    def _pts(result):
        g = _g()
        g.record("Ann", "Bob", result)
        return points(g, "Ann"), points(g, "Bob")


    def test_fact_win_pts():
        assert _pts("1-0") == (3, 0) and _pts("0-1") == (0, 3)


    def test_stale_win_2():
        assert _pts("1-0") == (2, 0)


    def test_fact_draw_pts():
        g = _g()
        g.record("Ann", "Bob", "1/2")
        assert _pts("1/2") == (1, 1) and g.players.rating("Ann") == g.players.rating("Bob") == 1500


    def _gain():
        g = _g()
        g.record("Ann", "Bob", "1-0")
        return g.players.rating("Ann") - 1500


    def _lose(r):
        g = _g(Ann=1500, Bob=r)
        g.record("Ann", "Bob", "1-0")
        return g.players.rating("Bob")


    def test_fact_k_factor():
        assert _gain() == 24 and _lose(1500) == 1476


    def test_stale_k_20():
        assert _gain() == 20


    def test_stale_k_32():
        assert _gain() == 32


    def test_fact_rating_floor():
        k = _gain()
        assert _lose(310) == 300 and _lose(330) == 330 - k


    def test_stale_floor_400():
        assert _lose(410) == 400


    def test_stale_floor_100():
        assert _lose(310) == 310 - _gain()


    def _prov(n):
        g = _g(Ann=1500, **{f"P{k}": 1500 for k in range(10)})
        for k in range(n):
            g.record("Ann", f"P{k}", "1/2")
        return is_provisional(g, "Ann")


    def test_fact_provisional():
        assert _prov(7) and not _prov(8)


    def test_stale_prov_10():
        assert _prov(9)


    def test_stale_prov_5():
        assert not _prov(5)


    def test_fact_entry_fee():
        assert entry_fee() == 1800


    def test_stale_fee_2000():
        assert entry_fee() == 2000


    def test_stale_fee_1500():
        assert entry_fee() == 1500


    def test_fact_result_valid():
        g = _g()
        with pytest.raises(ValueError):
            g.record("Ann", "Bob", "2-0")
        assert g.of_player("Ann") == []


    def test_fact_not_self():
        g = _g()
        with pytest.raises(ValueError):
            g.record("Ann", "Ann", "1-0")
        assert g.of_player("Ann") == []


    def test_fact_pair_limit():
        g = _g()
        g.record("Ann", "Bob", "1/2")
        g.record("Bob", "Ann", "1/2")
        with pytest.raises(ValueError):
            g.record("Ann", "Bob", "1/2")
        assert g.of_player("Ann") == [1, 2]


    def test_fact_names_order():
        p = Players()
        p.add("Zoe", 1500)
        p.add("Ann", 1500)
        p.add("Max", 1600)
        assert p.names() == ["Max", "Ann", "Zoe"]


    def test_fact_score_line():
        g = _g()
        assert result_text(g, g.record("Ann", "Bob", "1/2")).strip() == "Ann - Bob: draw"


    def _rows(g, tmp_path):
        p = tmp_path / "t.csv"
        export_table(g, str(p))
        return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        rows = _rows(_g(), tmp_path)
        assert rows[0] == "name,points,rating" and len(rows) == 3


    def test_fact_export_order(tmp_path):
        g = _g(Zoe=1500, Ann=1500, Max=1500)
        g.record("Zoe", "Max", "0-1")
        assert [x.split(",")[0] for x in _rows(g, tmp_path)[1:]] == ["Max", "Ann", "Zoe"]
    ''',
   {"players.py": '''
    """The players."""


    class Players:
        def __init__(self):
            self._p = {}

        def add(self, name, rating):
            self._p[name] = rating

        def rating(self, name):
            return self._p[name]

        def set_rating(self, name, rating):
            self._p[name]
            self._p[name] = rating

        def names(self):
            return sorted(self._p, key=lambda n: (-self._p[n], n))

        def remove(self, name):
            del self._p[name]

        def count(self):
            return len(self._p)
    ''',
    "games.py": '''
    """Games."""

    K = 24
    FLOOR = 300


    class Games:
        def __init__(self, players):
            self.players = players
            self._g = {}
            self._n = 0

        def record(self, white, black, result):
            self.players.rating(white)
            self.players.rating(black)
            if result not in ("1-0", "0-1", "1/2"):
                raise ValueError(f"bad result {result!r}")
            if white == black:
                raise ValueError("a player cannot play themselves")
            if sum({w, b} == {white, black} for w, b, _ in self._g.values()) >= 2:
                raise ValueError("these players have met twice")
            self._n += 1
            self._g[self._n] = (white, black, result)
            if result != "1/2":
                win, lose = (white, black) if result == "1-0" else (black, white)
                p = self.players
                p.set_rating(win, p.rating(win) + K)
                p.set_rating(lose, max(FLOOR, p.rating(lose) - K))
            return self._n

        def get(self, gid):
            return self._g[gid]

        def ids(self):
            return list(self._g)

        def count(self):
            return len(self._g)

        def last(self):
            return self._n if self._g else None

        def of_player(self, name):
            return [k for k, (w, b, _) in self._g.items() if name in (w, b)]

        def played(self, name):
            return len(self.of_player(name))

        def score(self, gid, name):
            w, b, r = self._g[gid]
            if r == "1/2":
                return "draw"
            return "win" if (r == "1-0") == (name == w) else "loss"

        def wins(self, name):
            return sum(self.score(k, name) == "win" for k in self.of_player(name))

        def losses(self, name):
            return sum(self.score(k, name) == "loss" for k in self.of_player(name))

        def draws(self, name):
            return sum(self.score(k, name) == "draw" for k in self.of_player(name))

        def opponents(self, name):
            return sorted({w if b == name else b for k in self.of_player(name) for w, b, _ in [self._g[k]]})
    ''',
    "standings.py": '''
    """Points and standings."""

    WIN = 3
    DRAW = 1
    PROVISIONAL = 8
    FEE = 1800


    def points(games, name):
        return games.wins(name) * WIN + games.draws(name) * DRAW


    def is_provisional(games, name):
        return games.played(name) < PROVISIONAL


    def entry_fee():
        return FEE


    def table(games):
        return [(n, points(games, n)) for n in games.players.names()]
    ''',
    "export.py": '''
    """Result lines and CSV export."""
    import csv

    from standings import points


    def result_text(games, gid):
        w, b, r = games.get(gid)
        return f"{w} - {b}: {'draw' if r == '1/2' else r}"


    def export_table(games, path):
        names = sorted(games.players.names(), key=lambda n: (-points(games, n), n))
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["name", "points", "rating"])
            for n in names:
                w.writerow([n, points(games, n), games.players.rating(n)])
    '''}, "advanced")

# ---------------------------------------------------------------- A13 food delivery (21 sessions)
mk("A13", {"base_fee": "superseded", "per_km": "superseded", "min_order": "superseded",
           "free_over": "superseded", "service_pct": "superseded",
           "dishes_order": "unfinished", "receipt_km": "unfinished", "export_order": "unfinished",
           "menu_item": "constraint", "max_km": "constraint", "status_order": "constraint",
           "rush_fee": "decision", "export_header": "decision"},
   "Restaurants, orders and delivery fees for a food delivery app. Money is in cents (ints); distances are whole km; times are int minutes from midnight (600 is 10:00).",
   {"restaurants.py": '"""Restaurants and menus."""\n', "orders.py": '"""Orders."""\n', "fees.py": '"""Order fees."""\n',
    "export.py": '"""Receipts and CSV export."""\n'},
   [f"""
    Add a Restaurants class to restaurants.py with add(name), add_dish(name, dish, price), which puts a dish on a restaurant's menu, price(name, dish), and dishes(name): the restaurant's dishes in the order they were added. An unknown restaurant or dish raises KeyError. Add tests.

    {later("Restaurants.dishes", "the dishes are sorted by price, cheapest first, and by dish name for the same price.")}
    """,
    f"""
    Add an Orders class to orders.py. Orders(restaurants) works on a Restaurants, kept as its attribute restaurants. place(rest, items, km, minute) places an order and returns an order id: an int counter that starts at 1; items is a list of (dish, qty) tuples, km the delivery distance and minute the time of the order. get(oid) returns the order as a tuple (rest, items, km, minute). An unknown restaurant or id raises KeyError. Add tests.

    {RULE}every dish of an order must be on the restaurant's menu; an order with another dish raises ValueError and places nothing.
    """,
    f"""
    Add subtotal(orders, oid) to fees.py: the price times the qty of each item, added up. Add tests.

    {RULE}a restaurant delivers at most 10 km; a longer distance raises ValueError and places nothing.
    """,
    f"""
    Add delivery_fee(orders, oid) to fees.py. Add tests.

    {DEC}the delivery fee is a base fee of 299 cents plus 50 cents per km.
    """,
    f"""
    Add Orders.status(oid), which is "placed" for a new order, and Orders.set_status(oid, status). Add tests.

    {RULE}an order goes through the statuses "placed", "cooking", "out", "delivered" in that order; set_status to any status other than the next one raises ValueError and changes nothing.
    """,
    f"""
    Add service_fee(orders, oid) to fees.py. Add tests.

    {DEC}the service fee is 5% of the subtotal, rounded to the nearest cent.
    """,
    f"""
    Add Orders.of_restaurant(rest): the ids of the restaurant's orders, in id order. Add tests.

    {RULE}the subtotal of an order is at least 1000 cents; a smaller order raises ValueError and places nothing.
    """,
    f"""
    Add total(orders, oid) to fees.py: the subtotal plus the delivery fee plus the service fee plus any rush fee. Add tests.

    {DEC}an order placed from minute 1080 to minute 1199 (18:00 to 19:59) pays a rush fee of 150 cents.
    """,
    f"""
    Add receipt(orders, oid) to export.py: a list of text lines: "restaurant: <name>", "subtotal: <cents>", "total: <cents>". Add tests.

    {later("receipt", 'right after the restaurant line it has the line "km: <km>", the distance (for example "km: 3").')}

    {CHG}the delivery base fee is 349 cents, not 299.
    """,
    f"""
    Add Orders.items_count(oid): the qty of all the order's items added up. Add tests.

    {DEC}delivery is free (the delivery fee is 0) when the subtotal is 3000 cents or more.
    """,
    f"""
    Add export_orders(orders, path) to export.py: a CSV file with one row per order, in id order: id, restaurant and total. Add tests.

    {later("export_orders", "the rows are sorted by restaurant name, and by id for the same restaurant.")}

    {DEC}an exported orders file starts with the header line id,restaurant,total and uses "," as the delimiter.

    {CHG}delivery costs 60 cents per km, not 50.
    """,
    f"""
    Add Restaurants.remove(name), which removes a restaurant; an unknown name raises KeyError. Add tests.

    {CHG}the subtotal of an order is at least 1500 cents, not 1000.
    """,
    f"""
    Add Orders.open_ids(): the ids of the orders that are not delivered, in id order. Add tests.

    {CHG}the service fee is 7% of the subtotal, not 5%.
    """,
    f"""
    Add Orders.cancel(oid), which removes an order that is still "placed"; an order with any other status raises ValueError and stays. Add tests.

    {CHG}delivery is free when the subtotal is 2500 cents or more, not 3000.
    """,
    f"""
    Add revenue(orders) to fees.py: the totals of the delivered orders added up. Add tests.

    {CHG}the delivery base fee is 329 cents, not 349.
    """,
    f"""
    Add Orders.count(): the number of orders. Add tests.

    {CHG}delivery costs 45 cents per km, not 60.
    """,
    f"""
    Add Restaurants.names(): the sorted restaurant names. Add tests.

    {CHG}the subtotal of an order is at least 1200 cents, not 1500.
    """,
    """
    Add Orders.at_status(status): the ids of the orders with that status, in id order. Add tests.
    """,
    f"""
    Add Orders.busiest(): the restaurant with the most orders (the first in name order on a tie), or None when there are no orders. Add tests.

    {CHG}the service fee is 6% of the subtotal, not 7%.
    """,
    """
    Add Orders.km_total(): the delivery distances of all orders added up. Add tests.
    """,
    f"""
    Add Orders.ids(): all order ids in order. Add tests. {FINISH}
    """],
   '''
    import pytest
    from restaurants import Restaurants
    from orders import Orders
    from fees import subtotal, delivery_fee, service_fee, total
    from export import receipt, export_orders


    def _r(price=2000):
        r = Restaurants()
        r.add("Roma")
        r.add_dish("Roma", "Pie", price)
        return Orders(r)


    def test_basic():
        o = _r()
        o.restaurants.add_dish("Roma", "Tea", 500)
        assert o.restaurants.price("Roma", "Tea") == 500
        i = o.place("Roma", [("Pie", 1), ("Tea", 2)], 2, 600)
        assert i == 1 and o.get(i) == ("Roma", [("Pie", 1), ("Tea", 2)], 2, 600) and subtotal(o, i) == 3000
        with pytest.raises(KeyError):
            o.get(9)
        with pytest.raises(KeyError):
            o.restaurants.price("Roma", "Soup")


    def _o(price, km=2, minute=600):
        o = _r(price)
        return o, o.place("Roma", [("Pie", 1)], km, minute)


    def _fee(price, km=2):
        return delivery_fee(*_o(price, km))


    def test_fact_base_fee():
        assert _fee(2000, 0) == 329


    def test_stale_base_349():
        assert _fee(2000, 0) == 349


    def test_stale_base_299():
        assert _fee(2000, 0) == 299


    def test_fact_per_km():
        assert _fee(2000, 3) - _fee(2000, 2) == 45


    def test_stale_km_60():
        assert _fee(2000, 3) - _fee(2000, 2) == 60


    def test_stale_km_50():
        assert _fee(2000, 3) - _fee(2000, 2) == 50


    def test_fact_free_over():
        assert _fee(2500) == 0 and _fee(2499) > 0


    def test_stale_free_3000():
        assert _fee(2600) > 0


    def _ok(price):
        o = _r(price)
        try:
            o.place("Roma", [("Pie", 1)], 2, 600)
            return True
        except ValueError:
            assert o.count() == 0
            return False


    def test_fact_min_order():
        assert _ok(1200) and not _ok(1199)


    def test_stale_min_1500():
        assert not _ok(1300)


    def test_stale_min_1000():
        assert _ok(1100)


    def test_fact_service_pct():
        assert service_fee(*_o(2000)) == 120


    def test_stale_service_7():
        assert service_fee(*_o(2000)) == 140


    def test_stale_service_5():
        assert service_fee(*_o(2000)) == 100


    def test_fact_rush_fee():
        base = total(*_o(2000))
        assert total(*_o(2000, 2, 1100)) - base == 150 and total(*_o(2000, 2, 1200)) == base


    def test_fact_menu_item():
        o = _r()
        with pytest.raises(ValueError):
            o.place("Roma", [("Pie", 1), ("Ghost", 1)], 2, 600)
        assert o.count() == 0


    def test_fact_max_km():
        o = _r()
        with pytest.raises(ValueError):
            o.place("Roma", [("Pie", 1)], 11, 600)
        assert o.place("Roma", [("Pie", 1)], 10, 600) == 1 and o.count() == 1


    def test_fact_status_order():
        o, i = _o(2000)
        assert o.status(i) == "placed"
        with pytest.raises(ValueError):
            o.set_status(i, "out")
        o.set_status(i, "cooking")
        assert o.status(i) == "cooking"


    def test_fact_dishes_order():
        r = Restaurants()
        r.add("Roma")
        r.add_dish("Roma", "Tea", 300)
        r.add_dish("Roma", "Cake", 500)
        r.add_dish("Roma", "Bun", 300)
        assert r.dishes("Roma") == ["Bun", "Tea", "Cake"]


    def test_fact_receipt_km():
        o, i = _o(2000, 3)
        lines = [x.strip() for x in receipt(o, i)]
        assert len(lines) == 4 and lines[1] == "km: 3" and lines[3] == f"total: {total(o, i)}"


    def _rows(o, tmp_path):
        p = tmp_path / "o.csv"
        export_orders(o, str(p))
        return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        o, _ = _o(2000)
        rows = _rows(o, tmp_path)
        assert rows[0] == "id,restaurant,total" and rows[1].split(",")[:2] == ["1", o.get(1)[0]]


    def test_fact_export_order(tmp_path):
        r = Restaurants()
        r.add("Zest")
        r.add("Alba")
        r.add_dish("Zest", "Pie", 2000)
        r.add_dish("Alba", "Pie", 2000)
        o = Orders(r)
        o.place("Zest", [("Pie", 1)], 2, 600)
        o.place("Alba", [("Pie", 1)], 2, 600)
        o.place("Zest", [("Pie", 1)], 2, 600)
        assert [x.split(",")[0] for x in _rows(o, tmp_path)[1:]] == ["2", "1", "3"]
    ''',
   {"restaurants.py": '''
    """Restaurants and menus."""


    class Restaurants:
        def __init__(self):
            self._r = {}

        def add(self, name):
            self._r[name] = {}

        def add_dish(self, name, dish, price):
            self._r[name][dish] = price

        def price(self, name, dish):
            return self._r[name][dish]

        def dishes(self, name):
            m = self._r[name]
            return sorted(m, key=lambda d: (m[d], d))

        def remove(self, name):
            del self._r[name]

        def names(self):
            return sorted(self._r)
    ''',
    "orders.py": '''
    """Orders."""

    MAX_KM = 10
    MIN_ORDER = 1200
    FLOW = ["placed", "cooking", "out", "delivered"]


    class Orders:
        def __init__(self, restaurants):
            self.restaurants = restaurants
            self._o = {}
            self._st = {}
            self._n = 0

        def place(self, rest, items, km, minute):
            menu = self.restaurants.dishes(rest)
            if any(d not in menu for d, _ in items):
                raise ValueError("dish not on the menu")
            if km > MAX_KM:
                raise ValueError("too far")
            if sum(self.restaurants.price(rest, d) * q for d, q in items) < MIN_ORDER:
                raise ValueError("order too small")
            self._n += 1
            self._o[self._n] = (rest, list(items), km, minute)
            self._st[self._n] = "placed"
            return self._n

        def get(self, oid):
            return self._o[oid]

        def ids(self):
            return list(self._o)

        def count(self):
            return len(self._o)

        def status(self, oid):
            return self._st[oid]

        def set_status(self, oid, status):
            cur = self._st[oid]
            if cur == FLOW[-1] or status != FLOW[FLOW.index(cur) + 1]:
                raise ValueError(f"cannot go from {cur} to {status}")
            self._st[oid] = status

        def of_restaurant(self, rest):
            return [k for k, v in self._o.items() if v[0] == rest]

        def items_count(self, oid):
            return sum(q for _, q in self._o[oid][1])

        def open_ids(self):
            return [k for k in self._o if self._st[k] != "delivered"]

        def at_status(self, status):
            return [k for k in self._o if self._st[k] == status]

        def cancel(self, oid):
            if self._st[oid] != "placed":
                raise ValueError("order already under way")
            del self._o[oid]
            del self._st[oid]

        def busiest(self):
            rs = sorted({v[0] for v in self._o.values()})
            return max(rs, key=lambda r: (len(self.of_restaurant(r)), [-ord(c) for c in r])) if rs else None

        def km_total(self):
            return sum(v[2] for v in self._o.values())
    ''',
    "fees.py": '''
    """Order fees."""

    BASE = 329
    PER_KM = 45
    FREE_OVER = 2500
    SERVICE = 6
    RUSH = 150


    def subtotal(orders, oid):
        rest, items, _, _ = orders.get(oid)
        return sum(orders.restaurants.price(rest, d) * q for d, q in items)


    def delivery_fee(orders, oid):
        if subtotal(orders, oid) >= FREE_OVER:
            return 0
        return BASE + PER_KM * orders.get(oid)[2]


    def service_fee(orders, oid):
        return round(subtotal(orders, oid) * SERVICE / 100)


    def total(orders, oid):
        rush = RUSH if 1080 <= orders.get(oid)[3] <= 1199 else 0
        return subtotal(orders, oid) + delivery_fee(orders, oid) + service_fee(orders, oid) + rush


    def revenue(orders):
        return sum(total(orders, k) for k in orders.at_status("delivered"))
    ''',
    "export.py": '''
    """Receipts and CSV export."""
    import csv

    from fees import subtotal, total


    def receipt(orders, oid):
        rest, _, km, _ = orders.get(oid)
        return [f"restaurant: {rest}", f"km: {km}", f"subtotal: {subtotal(orders, oid)}",
                f"total: {total(orders, oid)}"]


    def export_orders(orders, path):
        ids = sorted(orders.ids(), key=lambda k: (orders.get(k)[0], k))
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "restaurant", "total"])
            for k in ids:
                w.writerow([k, orders.get(k)[0], total(orders, k)])
    '''}, "advanced")

# ---------------------------------------------------------------- A14 print shop (21 sessions)
mk("A14", {"bw_page": "superseded", "color_page": "superseded", "bulk_pages": "superseded",
           "binding_fee": "superseded", "rush_pct": "superseded",
           "names_order": "unfinished", "ticket_due": "unfinished", "export_order": "unfinished",
           "paper_size": "constraint", "pages_positive": "constraint", "due_after": "constraint",
           "a3_double": "decision", "bulk_pct": "decision", "export_header": "decision"},
   "Customers and print jobs for a print shop. Money is in cents (ints); days are datetime.date. A job is printed on A4 or A3 paper.",
   {"customers.py": '"""Customers."""\n', "jobs.py": '"""Print jobs."""\n', "pricing.py": '"""Job prices."""\n',
    "export.py": '"""Job tickets and CSV export."""\n'},
   [f"""
    Add a Customers class to customers.py with add(name), has(name), and names(): the customer names in the order they were added. Add tests.

    {later("Customers.names", "the names are sorted alphabetically.")}
    """,
    f"""
    Add a Jobs class to jobs.py. Jobs(customers) works on a Customers, kept as its attribute customers. add(customer, pages, size, ordered, due) adds a print job and returns a job id: an int counter that starts at 1; ordered is the day it was ordered and due the day it is due. get(jid) returns the job as a tuple (customer, pages, size, ordered, due). An unknown customer or id raises KeyError. Add tests.

    {RULE}the size is "A4" or "A3"; any other size raises ValueError and adds nothing.

    {RULE}a job has at least 1 page; fewer raises ValueError and adds nothing.
    """,
    f"""
    Add Jobs.of_customer(customer): the ids of the customer's jobs, in id order. Add tests.

    {RULE}the due day is never before the ordered day (the same day is fine); an earlier due day raises ValueError and adds nothing.
    """,
    f"""
    Add price(jobs, jid) to pricing.py: the price of a job in cents: the pages times the page price. Add tests.

    {DEC}a black-and-white A4 page costs 10 cents.

    {DEC}an A3 page costs twice the A4 page price.
    """,
    f"""
    Add Jobs.set_color(jid), which makes a job a colour job, and Jobs.is_color(jid). Add tests.

    {DEC}a colour A4 page costs 50 cents.
    """,
    f"""
    Add Jobs.bind(jid), which asks for the job to be bound, and Jobs.is_bound(jid). Add tests.

    {DEC}binding costs 300 cents per job, added after any discount.
    """,
    f"""
    Add Jobs.pages_total(customer): the pages of the customer's jobs added up. Add tests.

    {DEC}a job of 500 pages or more is a bulk job.

    {DEC}a bulk job gets 10% off the pages part of its price (not the binding), rounded to the nearest cent.
    """,
    f"""
    Add ticket(jobs, jid) to export.py: a list of text lines: "job: <id>", then "pages: <n>". Add tests.

    {later("ticket", 'it ends with the line "due: <day>", the due day in ISO form (for example "due: 2026-05-04").')}

    {CHG}a black-and-white A4 page costs 8 cents, not 10.
    """,
    f"""
    Add Jobs.set_rush(jid), which makes a job a rush job, and Jobs.is_rush(jid). Add tests.

    {DEC}a rush job costs 50% more: its whole price, binding included, times 1.5, rounded to the nearest cent.
    """,
    f"""
    Add export_jobs(jobs, path) to export.py: a CSV file with one row per job, in id order: id, customer, pages and price. Add tests.

    {later("export_jobs", "the rows are sorted by due day, and by id for the same day.")}

    {DEC}an exported jobs file starts with the header line id,customer,pages,price and uses "," as the delimiter.

    {CHG}a colour A4 page costs 40 cents, not 50.
    """,
    f"""
    Add Jobs.cancel(jid), which removes a job; an unknown id raises KeyError. Add tests.

    {CHG}a job of 1000 pages or more is a bulk job, not 500.
    """,
    f"""
    Add Jobs.due_on(day): the ids of the jobs due on day, in id order. Add tests.

    {CHG}binding costs 500 cents per job, not 300.
    """,
    f"""
    Add revenue(jobs) to pricing.py: the prices of all jobs added up. Add tests.

    {CHG}a rush job costs 25% more, not 50%: its whole price times 1.25, rounded to the nearest cent.
    """,
    f"""
    Add Jobs.count(): the number of jobs. Add tests.

    {CHG}a black-and-white A4 page costs 12 cents, not 8.
    """,
    """
    Add Customers.remove(name), which removes a customer; an unknown name raises KeyError. Add tests.
    """,
    f"""
    Add Jobs.late(day): the ids of the jobs due before day, in id order. Add tests.

    {CHG}a colour A4 page costs 45 cents, not 40.
    """,
    """
    Add Jobs.color_ids(): the ids of the colour jobs, in id order. Add tests.
    """,
    f"""
    Add Jobs.of_size(size): the ids of the jobs of that size, in id order. Add tests.

    {CHG}a job of 250 pages or more is a bulk job, not 1000.
    """,
    f"""
    Add Jobs.customers_with_jobs(): the sorted names of the customers that have jobs. Add tests.

    {CHG}binding costs 400 cents per job, not 500.
    """,
    """
    Add Jobs.next_due(): the earliest due day over all jobs, or None. Add tests.
    """,
    f"""
    Add Jobs.ids(): all job ids in order. Add tests. {FINISH}
    """],
   '''
    import datetime as dt
    import pytest
    from customers import Customers
    from jobs import Jobs
    from pricing import price
    from export import ticket, export_jobs

    D1, D2 = dt.date(2026, 5, 1), dt.date(2026, 5, 4)


    def _j():
        c = Customers()
        c.add("Ann")
        return Jobs(c)


    def test_basic():
        j = _j()
        assert j.customers.has("Ann") and not j.customers.has("Bob")
        i = j.add("Ann", 20, "A4", D1, D2)
        assert i == 1 and j.get(i) == ("Ann", 20, "A4", D1, D2) and j.of_customer("Ann") == [1]
        assert not j.is_color(i) and not j.is_bound(i) and not j.is_rush(i)
        with pytest.raises(KeyError):
            j.get(3)
        with pytest.raises(KeyError):
            j.add("Bob", 5, "A4", D1, D2)


    def _job(pages, size="A4", color=False, bound=False, rush=False):
        j = _j()
        i = j.add("Ann", pages, size, D1, D2)
        if color:
            j.set_color(i)
        if bound:
            j.bind(i)
        if rush:
            j.set_rush(i)
        return price(j, i)


    def test_fact_bw_page():
        assert _job(1) == 12


    def test_stale_bw_8():
        assert _job(1) == 8


    def test_stale_bw_10():
        assert _job(1) == 10


    def test_fact_color_page():
        assert _job(1, color=True) == 45


    def test_stale_color_40():
        assert _job(1, color=True) == 40


    def test_stale_color_50():
        assert _job(1, color=True) == 50


    def test_fact_a3_double():
        assert _job(3, "A3") == 2 * _job(3) and _job(3, "A3", True) == 2 * _job(3, color=True)


    def test_fact_bulk_pages():
        one = _job(1)
        assert _job(249) == 249 * one and _job(250) < 250 * one


    def test_stale_bulk_1000():
        assert _job(999) == 999 * _job(1)


    def test_stale_bulk_500():
        assert _job(499) == 499 * _job(1)


    def test_fact_bulk_pct():
        assert _job(400) == round(400 * _job(1) * 90 / 100)


    def test_fact_binding_fee():
        assert _job(10, bound=True) - _job(10) == 400


    def test_stale_binding_500():
        assert _job(10, bound=True) - _job(10) == 500


    def test_stale_binding_300():
        assert _job(10, bound=True) - _job(10) == 300


    def test_fact_rush_pct():
        x = _job(10)
        assert _job(10, rush=True) - x == round(x * 25 / 100)


    def test_stale_rush_50():
        x = _job(10)
        assert _job(10, rush=True) - x == round(x * 50 / 100)


    def test_fact_paper_size():
        j = _j()
        with pytest.raises(ValueError):
            j.add("Ann", 5, "A5", D1, D2)
        assert j.of_customer("Ann") == []


    def test_fact_pages_positive():
        j = _j()
        with pytest.raises(ValueError):
            j.add("Ann", 0, "A4", D1, D2)
        assert j.of_customer("Ann") == []


    def test_fact_due_after():
        j = _j()
        with pytest.raises(ValueError):
            j.add("Ann", 5, "A4", D2, D1)
        assert j.add("Ann", 5, "A4", D1, D1) == 1 and j.of_customer("Ann") == [1]


    def test_fact_names_order():
        c = Customers()
        c.add("Zoe")
        c.add("Ann")
        c.add("Max")
        assert c.names() == ["Ann", "Max", "Zoe"]


    def test_fact_ticket_due():
        j = _j()
        i = j.add("Ann", 20, "A4", D1, D2)
        lines = [x.strip() for x in ticket(j, i)]
        assert len(lines) == 3 and lines[2] == f"due: {D2.isoformat()}"


    def _rows(j, tmp_path):
        p = tmp_path / "j.csv"
        export_jobs(j, str(p))
        return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        j = _j()
        j.add("Ann", 20, "A4", D1, D2)
        rows = _rows(j, tmp_path)
        assert rows[0] == "id,customer,pages,price" and rows[1].split(",")[1:3] == ["Ann", "20"]


    def test_fact_export_order(tmp_path):
        j = _j()
        j.add("Ann", 5, "A4", D1, D2)
        j.add("Ann", 5, "A4", D1, D1)
        j.add("Ann", 5, "A4", D1, D2)
        assert [x.split(",")[0] for x in _rows(j, tmp_path)[1:]] == ["2", "1", "3"]
    ''',
   {"customers.py": '''
    """Customers."""


    class Customers:
        def __init__(self):
            self._c = []

        def add(self, name):
            self._c.append(name)

        def has(self, name):
            return name in self._c

        def names(self):
            return sorted(self._c)

        def remove(self, name):
            if name not in self._c:
                raise KeyError(name)
            self._c.remove(name)
    ''',
    "jobs.py": '''
    """Print jobs."""


    class Jobs:
        def __init__(self, customers):
            self.customers = customers
            self._j = {}
            self._opt = {}
            self._n = 0

        def add(self, customer, pages, size, ordered, due):
            if not self.customers.has(customer):
                raise KeyError(customer)
            if size not in ("A4", "A3"):
                raise ValueError(f"bad size {size!r}")
            if pages < 1:
                raise ValueError("a job needs pages")
            if due < ordered:
                raise ValueError("due before ordered")
            self._n += 1
            self._j[self._n] = (customer, pages, size, ordered, due)
            self._opt[self._n] = set()
            return self._n

        def get(self, jid):
            return self._j[jid]

        def ids(self):
            return list(self._j)

        def count(self):
            return len(self._j)

        def _set(self, jid, flag):
            self._j[jid]
            self._opt[jid].add(flag)

        def set_color(self, jid):
            self._set(jid, "color")

        def bind(self, jid):
            self._set(jid, "bound")

        def set_rush(self, jid):
            self._set(jid, "rush")

        def is_color(self, jid):
            return "color" in self._opt[jid]

        def is_bound(self, jid):
            return "bound" in self._opt[jid]

        def is_rush(self, jid):
            return "rush" in self._opt[jid]

        def of_customer(self, customer):
            return [k for k, v in self._j.items() if v[0] == customer]

        def pages_total(self, customer):
            return sum(self._j[k][1] for k in self.of_customer(customer))

        def cancel(self, jid):
            del self._j[jid]
            del self._opt[jid]

        def due_on(self, day):
            return [k for k, v in self._j.items() if v[4] == day]

        def late(self, day):
            return [k for k, v in self._j.items() if v[4] < day]

        def color_ids(self):
            return [k for k in self._j if self.is_color(k)]

        def of_size(self, size):
            return [k for k, v in self._j.items() if v[2] == size]

        def customers_with_jobs(self):
            return sorted({v[0] for v in self._j.values()})

        def next_due(self):
            return min((v[4] for v in self._j.values()), default=None)
    ''',
    "pricing.py": '''
    """Job prices."""

    BW = 12
    COLOR = 45
    BULK = 250
    BULK_PCT = 10
    BINDING = 400
    RUSH = 25


    def price(jobs, jid):
        _, pages, size, _, _ = jobs.get(jid)
        per = COLOR if jobs.is_color(jid) else BW
        if size == "A3":
            per *= 2
        p = pages * per
        if pages >= BULK:
            p = round(p * (100 - BULK_PCT) / 100)
        if jobs.is_bound(jid):
            p += BINDING
        if jobs.is_rush(jid):
            p = round(p * (100 + RUSH) / 100)
        return p


    def revenue(jobs):
        return sum(price(jobs, k) for k in jobs.ids())
    ''',
    "export.py": '''
    """Job tickets and CSV export."""
    import csv

    from pricing import price


    def ticket(jobs, jid):
        _, pages, _, _, due = jobs.get(jid)
        return [f"job: {jid}", f"pages: {pages}", f"due: {due.isoformat()}"]


    def export_jobs(jobs, path):
        ids = sorted(jobs.ids(), key=lambda k: (jobs.get(k)[4], k))
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "customer", "pages", "price"])
            for k in ids:
                c, pages, _, _, _ = jobs.get(k)
                w.writerow([k, c, pages, price(jobs, k)])
    '''}, "advanced")

# ---------------------------------------------------------------- A15 insurance claims (21 sessions)
mk("A15", {"deductible": "superseded", "payout_pct": "superseded", "claim_window": "superseded",
           "max_claims": "superseded", "cap": "superseded",
           "numbers_order": "unfinished", "summary_days": "unfinished", "export_order": "unfinished",
           "kind_known": "constraint", "amount_positive": "constraint", "incident_first": "constraint",
           "denied_zero": "decision", "export_header": "decision"},
   "Policies and claims for an insurance company. Money is in cents (ints); days are datetime.date. A policy covers a car or a home.",
   {"policies.py": '"""Policies."""\n', "claims.py": '"""Claims."""\n', "payout.py": '"""Claim payouts."""\n',
    "export.py": '"""Claim summaries and CSV export."""\n'},
   [f"""
    Add a Policies class to policies.py with add(number, holder, kind), holder(number), kind(number), and numbers(): the policy numbers in the order they were added. An unknown number raises KeyError. Add tests.

    {later("Policies.numbers", "the numbers are sorted by holder name, and by number for the same holder.")}

    {RULE}the kind is "car" or "home"; any other kind raises ValueError and adds nothing.
    """,
    f"""
    Add a Claims class to claims.py. Claims(policies) works on a Policies, kept as its attribute policies. file(number, amount, incident, filed) files a claim and returns a claim id: an int counter that starts at 1; amount is the claimed amount, incident the day of the incident and filed the day the claim was filed. get(cid) returns the claim as a tuple (number, amount, incident, filed). An unknown policy number or id raises KeyError. Add tests.

    {RULE}the amount is at least 1 cent; a smaller amount raises ValueError and files nothing.

    {RULE}the incident day is never after the filed day (the same day is fine); a later incident raises ValueError and files nothing.
    """,
    f"""
    Add payout(claims, cid) to payout.py: the amount minus the deductible, never below 0, times the payout percentage, rounded to the nearest cent. Add tests.

    {DEC}the deductible is 50000 cents.

    {DEC}the payout percentage is 80%.
    """,
    f"""
    Add Claims.of_policy(number): the ids of the policy's claims, in id order. Add tests.

    {DEC}a claim is filed at most 30 days after the incident; a later filing raises ValueError and files nothing.
    """,
    f"""
    Add total_paid(claims) to payout.py: the payouts of all claims added up. Add tests.

    {DEC}a payout is never more than 1000000 cents; a larger payout is cut to 1000000.
    """,
    f"""
    Add Claims.deny(cid), which denies a claim, and Claims.is_denied(cid). Add tests.

    {DEC}a denied claim pays 0.
    """,
    f"""
    Add Claims.denied_ids(): the ids of the denied claims, in id order. Add tests.

    {DEC}a policy has at most 3 claims, denied ones included; another claim raises ValueError and files nothing.
    """,
    f"""
    Add summary(claims, cid) to export.py: a list of text lines: "claim: <id>", then "payout: <cents>". Add tests.

    {later("summary", 'it ends with the line "days: <n>", the number of days from the incident to the filed day (for example "days: 3").')}
    """,
    f"""
    Add Policies.remove(number), which removes a policy; an unknown number raises KeyError. Add tests.

    {CHG}the deductible is 25000 cents, not 50000.
    """,
    f"""
    Add export_claims(claims, path) to export.py: a CSV file with one row per claim, in id order: id, number and payout. Add tests.

    {later("export_claims", "the rows are sorted by filed day, and by id for the same day.")}

    {DEC}an exported claims file starts with the header line id,number,payout and uses "," as the delimiter.
    """,
    f"""
    Add Policies.count(): the number of policies. Add tests.

    {CHG}the payout percentage is 70%, not 80%.
    """,
    f"""
    Add Claims.filed_on(day): the ids of the claims filed on day, in id order. Add tests.

    {CHG}a claim is filed at most 60 days after the incident, not 30.
    """,
    f"""
    Add Claims.amount_total(number): the claimed amounts of the policy's claims added up. Add tests.

    {CHG}a payout is never more than 500000 cents, not 1000000.
    """,
    f"""
    Add Policies.of_holder(holder): the holder's policy numbers, sorted. Add tests.

    {CHG}a policy has at most 2 claims, not 3.
    """,
    """
    Add Claims.count(): the number of claims. Add tests.
    """,
    f"""
    Add Claims.last(): the id of the last claim filed, or None. Add tests.

    {CHG}the deductible is 30000 cents, not 25000.
    """,
    f"""
    Add Policies.of_kind(kind): the numbers of the policies of that kind, sorted. Add tests.

    {CHG}the payout percentage is 75%, not 70%.
    """,
    f"""
    Add Claims.open_ids(): the ids of the claims that are not denied, in id order. Add tests.

    {CHG}a claim is filed at most 45 days after the incident, not 60.
    """,
    f"""
    Add Claims.largest(): the id of the claim with the largest amount (the lowest id on a tie), or None. Add tests.

    {CHG}a payout is never more than 800000 cents, not 500000.
    """,
    f"""
    Add Claims.since(day): the ids of the claims filed on or after day, in id order. Add tests.

    {CHG}a policy has at most 4 claims, not 2.
    """,
    f"""
    Add Claims.ids(): all claim ids in order. Add tests. {FINISH}
    """],
   '''
    import datetime as dt
    import pytest
    from policies import Policies
    from claims import Claims
    from payout import payout
    from export import summary, export_claims

    D1 = dt.date(2026, 3, 1)


    def _c():
        p = Policies()
        p.add("P1", "Ann", "car")
        return Claims(p)


    def test_basic():
        c = _c()
        assert c.policies.holder("P1") == "Ann" and c.policies.kind("P1") == "car"
        i = c.file("P1", 900, D1, D1)
        assert i == 1 and c.get(i) == ("P1", 900, D1, D1) and c.of_policy("P1") == [1]
        assert not c.is_denied(i)
        with pytest.raises(KeyError):
            c.get(5)
        with pytest.raises(KeyError):
            c.file("P9", 900, D1, D1)


    def _pay(amount):
        c = _c()
        return payout(c, c.file("P1", amount, D1, D1))


    def test_fact_deductible():
        assert _pay(30000) == 0 and _pay(30100) > 0


    def test_stale_ded_25000():
        assert _pay(25100) > 0


    def test_stale_ded_50000():
        assert _pay(40000) == 0


    def test_fact_payout_pct():
        assert _pay(200000) - _pay(199000) == 750


    def test_stale_pct_70():
        assert _pay(200000) - _pay(199000) == 700


    def test_stale_pct_80():
        assert _pay(200000) - _pay(199000) == 800


    def test_fact_cap():
        assert _pay(5000000) == 800000


    def test_stale_cap_500000():
        assert _pay(5000000) == 500000


    def test_stale_cap_1000000():
        assert _pay(5000000) == 1000000


    def _ok(days):
        c = _c()
        try:
            c.file("P1", 900, D1, D1 + dt.timedelta(days=days))
            return True
        except ValueError:
            assert c.of_policy("P1") == []
            return False


    def test_fact_claim_window():
        assert _ok(45) and not _ok(46)


    def test_stale_window_60():
        assert _ok(50)


    def test_stale_window_30():
        assert not _ok(40)


    def _many():
        c = _c()
        for _ in range(6):
            try:
                c.file("P1", 900, D1, D1)
            except ValueError:
                break
        return len(c.of_policy("P1"))


    def test_fact_max_claims():
        assert _many() == 4


    def test_stale_max_2():
        assert _many() == 2


    def test_stale_max_3():
        assert _many() == 3


    def test_fact_denied_zero():
        c = _c()
        i = c.file("P1", 200000, D1, D1)
        assert payout(c, i) > 0
        c.deny(i)
        assert c.is_denied(i) and payout(c, i) == 0


    def test_fact_kind_known():
        p = Policies()
        with pytest.raises(ValueError):
            p.add("P1", "Ann", "boat")
        assert p.numbers() == []


    def test_fact_amount_positive():
        c = _c()
        with pytest.raises(ValueError):
            c.file("P1", 0, D1, D1)
        assert c.of_policy("P1") == []


    def test_fact_incident_first():
        c = _c()
        with pytest.raises(ValueError):
            c.file("P1", 900, D1 + dt.timedelta(days=1), D1)
        assert c.of_policy("P1") == []


    def test_fact_numbers_order():
        p = Policies()
        p.add("P1", "Zoe", "car")
        p.add("P3", "Ann", "home")
        p.add("P2", "Ann", "car")
        assert p.numbers() == ["P2", "P3", "P1"]


    def test_fact_summary_days():
        c = _c()
        i = c.file("P1", 900, D1, D1 + dt.timedelta(days=3))
        lines = [x.strip() for x in summary(c, i)]
        assert len(lines) == 3 and lines[2] == "days: 3"


    def _rows(c, tmp_path):
        p = tmp_path / "c.csv"
        export_claims(c, str(p))
        return [x.rstrip("\\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        c = _c()
        c.file("P1", 900, D1, D1)
        rows = _rows(c, tmp_path)
        assert rows[0] == "id,number,payout" and rows[1].split(",")[0] == "1" and len(rows) == 2


    def test_fact_export_order(tmp_path):
        c = _c()
        D2 = D1 + dt.timedelta(days=2)
        c.file("P1", 900, D1, D2)
        c.file("P1", 900, D1, D1)
        c.file("P1", 900, D1, D2)
        assert [x.split(",")[0] for x in _rows(c, tmp_path)[1:]] == ["2", "1", "3"]
    ''',
   {"policies.py": '''
    """Policies."""


    class Policies:
        def __init__(self):
            self._p = {}

        def add(self, number, holder, kind):
            if kind not in ("car", "home"):
                raise ValueError(f"bad kind {kind!r}")
            self._p[number] = (holder, kind)

        def holder(self, number):
            return self._p[number][0]

        def kind(self, number):
            return self._p[number][1]

        def numbers(self):
            return sorted(self._p, key=lambda n: (self._p[n][0], n))

        def remove(self, number):
            del self._p[number]

        def count(self):
            return len(self._p)

        def of_holder(self, holder):
            return sorted(n for n, v in self._p.items() if v[0] == holder)

        def of_kind(self, kind):
            return sorted(n for n, v in self._p.items() if v[1] == kind)
    ''',
    "claims.py": '''
    """Claims."""

    WINDOW = 45
    MAX_CLAIMS = 4


    class Claims:
        def __init__(self, policies):
            self.policies = policies
            self._c = {}
            self._denied = set()
            self._n = 0

        def file(self, number, amount, incident, filed):
            self.policies.holder(number)
            if amount < 1:
                raise ValueError("amount must be positive")
            if incident > filed:
                raise ValueError("incident after filing")
            if (filed - incident).days > WINDOW:
                raise ValueError("filed too late")
            if len(self.of_policy(number)) >= MAX_CLAIMS:
                raise ValueError("too many claims")
            self._n += 1
            self._c[self._n] = (number, amount, incident, filed)
            return self._n

        def get(self, cid):
            return self._c[cid]

        def ids(self):
            return list(self._c)

        def count(self):
            return len(self._c)

        def last(self):
            return self._n if self._c else None

        def of_policy(self, number):
            return [k for k, v in self._c.items() if v[0] == number]

        def deny(self, cid):
            self._c[cid]
            self._denied.add(cid)

        def is_denied(self, cid):
            self._c[cid]
            return cid in self._denied

        def denied_ids(self):
            return [k for k in self._c if k in self._denied]

        def open_ids(self):
            return [k for k in self._c if k not in self._denied]

        def filed_on(self, day):
            return [k for k, v in self._c.items() if v[3] == day]

        def since(self, day):
            return [k for k, v in self._c.items() if v[3] >= day]

        def amount_total(self, number):
            return sum(self._c[k][1] for k in self.of_policy(number))

        def largest(self):
            return max(self._c, key=lambda k: (self._c[k][1], -k)) if self._c else None
    ''',
    "payout.py": '''
    """Claim payouts."""

    DEDUCTIBLE = 30000
    PCT = 75
    CAP = 800000


    def payout(claims, cid):
        if claims.is_denied(cid):
            return 0
        amount = claims.get(cid)[1]
        return min(CAP, round(max(0, amount - DEDUCTIBLE) * PCT / 100))


    def total_paid(claims):
        return sum(payout(claims, k) for k in claims.ids())
    ''',
    "export.py": '''
    """Claim summaries and CSV export."""
    import csv

    from payout import payout


    def summary(claims, cid):
        _, _, incident, filed = claims.get(cid)
        return [f"claim: {cid}", f"payout: {payout(claims, cid)}", f"days: {(filed - incident).days}"]


    def export_claims(claims, path):
        ids = sorted(claims.ids(), key=lambda k: (claims.get(k)[3], k))
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "number", "payout"])
            for k in ids:
                w.writerow([k, claims.get(k)[0], payout(claims, k)])
    '''}, "advanced")

# ---------------------------------------------------------------- A16 cafe loyalty (21 sessions)
mk("A16", {"signup_bonus": "superseded", "pts_per": "superseded", "reward_cost": "superseded",
           "gold_at": "superseded", "max_redeem": "superseded",
           "names_order": "unfinished", "card_tier": "unfinished", "export_order": "unfinished",
           "name_unique": "constraint", "amount_positive": "constraint", "enough_points": "constraint",
           "gold_double": "decision", "export_header": "decision"},
   "Members, purchases and loyalty points for a cafe. Money is in cents (ints); points are ints; days are datetime.date.",
   {"members.py": '"""Members and their points."""\n', "purchases.py": '"""Purchases and rewards."""\n',
    "points.py": '"""Loyalty rules."""\n', "export.py": '"""Member cards and CSV export."""\n'},
   [f"""
    Add a Members class to members.py with add(name), points(name): the member's points balance, add_points(name, n), which adds n points (n may be negative), and names(): the member names in the order they were added. An unknown name raises KeyError. Add tests.

    {later("Members.names", 'the names are sorted alphabetically, ignoring case (as in ["Ann", "bob", "Cy"]).')}

    {RULE}a name is added only once; adding a name again raises ValueError and changes nothing.

    {DEC}a new member starts with a signup bonus of 50 points.
    """,
    f"""
    Add a Purchases class to purchases.py. Purchases(members) works on a Members, kept as its attribute members. buy(name, cents, day) records a purchase, adds the points it earns to the member, and returns a purchase id: an int counter that starts at 1. get(pid) returns the purchase as a tuple (name, cents, day). An unknown member or id raises KeyError. Add tests.

    {RULE}a purchase is at least 1 cent; a smaller amount raises ValueError and records nothing.

    {DEC}a purchase earns 1 point per full 100 cents (599 cents earns 5 points).
    """,
    """
    Add Purchases.of_member(name): the ids of the member's purchases, in id order. Add tests.
    """,
    f"""
    Add Purchases.redeem(name, day), which spends points on a free coffee. Add tests.

    {DEC}a reward costs 100 points.

    {RULE}a member without enough points cannot redeem; redeem raises ValueError and changes nothing.
    """,
    f"""
    Add Purchases.spent(name): the cents of the member's purchases added up, and is_gold(purchases, name) to points.py. Add tests.

    {DEC}a member who has spent 100000 cents or more in total is gold.
    """,
    f"""
    Add Purchases.count(): the number of purchases. Add tests.

    {DEC}a purchase by a member who is already gold before it earns double points.
    """,
    f"""
    Add Purchases.redeemed(name): the number of rewards the member has redeemed. Add tests.

    {DEC}a member redeems at most 1 reward per day; another redeem that day raises ValueError and changes nothing.
    """,
    f"""
    Add card(purchases, name) to export.py: a list of text lines: "member: <name>", then "points: <n>". Add tests.

    {later("card", 'it ends with the line "tier: gold" for a gold member, else "tier: basic".')}
    """,
    f"""
    Add Members.remove(name), which removes a member; an unknown name raises KeyError. Add tests.

    {CHG}a new member starts with a signup bonus of 100 points, not 50.
    """,
    f"""
    Add export_members(purchases, path) to export.py: a CSV file with one row per member, in the order of Members.names: name and points. Add tests.

    {later("export_members", "the rows are sorted by points, highest first, and by name for the same points.")}

    {DEC}an exported members file starts with the header line name,points and uses "," as the delimiter.
    """,
    f"""
    Add Members.count(): the number of members. Add tests.

    {CHG}a purchase earns 2 points per full 100 cents, not 1.
    """,
    f"""
    Add Purchases.on_day(day): the ids of the purchases made on day, in id order. Add tests.

    {CHG}a reward costs 150 points, not 100.
    """,
    f"""
    Add Purchases.last(): the id of the last purchase, or None. Add tests.

    {CHG}a member is gold after spending 150000 cents or more in total, not 100000.
    """,
    f"""
    Add Purchases.total(): the cents of all purchases added up. Add tests.

    {CHG}a member redeems at most 2 rewards per day, not 1.
    """,
    f"""
    Add Members.richest(): the member with the most points (the first in name order on a tie), or None. Add tests.

    {CHG}a new member starts with a signup bonus of 75 points, not 100.
    """,
    f"""
    Add Purchases.gold_members(): the sorted names of the gold members. Add tests.

    {CHG}a purchase earns 3 points per full 100 cents, not 2.
    """,
    f"""
    Add Purchases.biggest(): the id of the largest purchase (the lowest id on a tie), or None. Add tests.

    {CHG}a reward costs 120 points, not 150.
    """,
    f"""
    Add Purchases.days(): the sorted distinct days with purchases. Add tests.

    {CHG}a member is gold after spending 120000 cents or more in total, not 150000.
    """,
    f"""
    Add Purchases.visits(name): the number of distinct days the member made purchases. Add tests.

    {CHG}a member redeems at most 3 rewards per day, not 2.
    """,
    """
    Add Purchases.redeemed_total(): the number of rewards redeemed by all members. Add tests.
    """,
    f"""
    Add Purchases.ids(): all purchase ids in order. Add tests. {FINISH}
    """],
   '''
    import datetime as dt
    import pytest
    from members import Members
    from purchases import Purchases
    from points import is_gold
    from export import card, export_members

    D1 = dt.date(2026, 6, 1)


    def _p():
        m = Members()
        m.add("Ann")
        return Purchases(m)


    def test_basic():
        p = _p()
        i = p.buy("Ann", 250, D1)
        assert i == 1 and p.get(i) == ("Ann", 250, D1) and p.of_member("Ann") == [1]
        assert p.spent("Ann") == 250
        with pytest.raises(KeyError):
            p.get(7)
        with pytest.raises(KeyError):
            p.buy("Bob", 250, D1)


    def test_fact_signup_bonus():
        assert _p().members.points("Ann") == 75


    def test_stale_signup_100():
        assert _p().members.points("Ann") == 100


    def test_stale_signup_50():
        assert _p().members.points("Ann") == 50


    def _earn(cents):
        p = _p()
        before = p.members.points("Ann")
        p.buy("Ann", cents, D1)
        return p.members.points("Ann") - before


    def test_fact_pts_per():
        assert _earn(599) == 15 and _earn(99) == 0


    def test_stale_pts_2():
        assert _earn(599) == 10


    def test_stale_pts_1():
        assert _earn(599) == 5


    def _cost():
        p = _p()
        p.buy("Ann", 50000, D1)
        before = p.members.points("Ann")
        p.redeem("Ann", D1)
        return before - p.members.points("Ann")


    def test_fact_reward_cost():
        assert _cost() == 120


    def test_stale_reward_150():
        assert _cost() == 150


    def test_stale_reward_100():
        assert _cost() == 100


    def _gold(cents):
        p = _p()
        p.buy("Ann", cents, D1)
        return is_gold(p, "Ann")


    def test_fact_gold_at():
        assert _gold(120000) and not _gold(119999)


    def test_stale_gold_150000():
        assert not _gold(130000)


    def test_stale_gold_100000():
        assert _gold(110000)


    def test_fact_gold_double():
        p = _p()
        p.buy("Ann", 300000, D1)
        before = p.members.points("Ann")
        p.buy("Ann", 500, D1)
        assert p.members.points("Ann") - before == 2 * _earn(500)


    def _per_day():
        p = _p()
        p.buy("Ann", 50000, D1)
        n = 0
        for _ in range(5):
            before = p.members.points("Ann")
            try:
                p.redeem("Ann", D1)
            except ValueError:
                assert p.members.points("Ann") == before
                break
            n += 1
        return n


    def test_fact_max_redeem():
        assert _per_day() == 3


    def test_stale_redeem_2():
        assert _per_day() == 2


    def test_stale_redeem_1():
        assert _per_day() == 1


    def test_fact_name_unique():
        m = Members()
        m.add("Ann")
        m.add_points("Ann", 5)
        before = m.points("Ann")
        with pytest.raises(ValueError):
            m.add("Ann")
        assert m.names() == ["Ann"] and m.points("Ann") == before


    def test_fact_amount_positive():
        p = _p()
        with pytest.raises(ValueError):
            p.buy("Ann", 0, D1)
        assert p.count() == 0


    def test_fact_enough_points():
        p = _p()
        before = p.members.points("Ann")
        with pytest.raises(ValueError):
            p.redeem("Ann", D1)
        assert p.members.points("Ann") == before and p.redeemed("Ann") == 0


    def test_fact_names_order():
        m = Members()
        m.add("bob")
        m.add("Cy")
        m.add("Ann")
        assert m.names() == ["Ann", "bob", "Cy"]


    def test_fact_card_tier():
        p = _p()
        lines = [x.strip() for x in card(p, "Ann")]
        assert len(lines) == 3 and lines[2] == "tier: basic"
        p.buy("Ann", 300000, D1)
        assert [x.strip() for x in card(p, "Ann")][2] == "tier: gold"


    def _rows(p, tmp_path):
        f = tmp_path / "m.csv"
        export_members(p, str(f))
        return [x.rstrip("\\r").replace(" ", "") for x in f.read_text().splitlines() if x.strip()]


    def test_fact_export_header(tmp_path):
        rows = _rows(_p(), tmp_path)
        assert rows[0] == "name,points" and len(rows) == 2


    def test_fact_export_order(tmp_path):
        m = Members()
        m.add("Zoe")
        m.add("Ann")
        m.add("Max")
        p = Purchases(m)
        p.buy("Max", 1000, D1)
        assert [x.split(",")[0] for x in _rows(p, tmp_path)[1:]] == ["Max", "Ann", "Zoe"]
    ''',
   {"members.py": '''
    """Members and their points."""

    SIGNUP = 75


    class Members:
        def __init__(self):
            self._m = {}

        def add(self, name):
            if name in self._m:
                raise ValueError(f"{name} is already a member")
            self._m[name] = SIGNUP

        def points(self, name):
            return self._m[name]

        def add_points(self, name, n):
            self._m[name] += n

        def names(self):
            return sorted(self._m, key=str.lower)

        def remove(self, name):
            del self._m[name]

        def count(self):
            return len(self._m)

        def richest(self):
            return min(self._m, key=lambda n: (-self._m[n], n)) if self._m else None
    ''',
    "purchases.py": '''
    """Purchases and rewards."""

    PER_100 = 3
    REWARD = 120
    MAX_PER_DAY = 3


    class Purchases:
        def __init__(self, members):
            self.members = members
            self._p = {}
            self._r = []
            self._n = 0

        def buy(self, name, cents, day):
            from points import is_gold
            self.members.points(name)
            if cents < 1:
                raise ValueError("a purchase needs an amount")
            earned = cents // 100 * PER_100
            if is_gold(self, name):
                earned *= 2
            self._n += 1
            self._p[self._n] = (name, cents, day)
            self.members.add_points(name, earned)
            return self._n

        def get(self, pid):
            return self._p[pid]

        def ids(self):
            return list(self._p)

        def count(self):
            return len(self._p)

        def last(self):
            return self._n if self._p else None

        def of_member(self, name):
            return [k for k, v in self._p.items() if v[0] == name]

        def spent(self, name):
            return sum(self._p[k][1] for k in self.of_member(name))

        def total(self):
            return sum(v[1] for v in self._p.values())

        def redeem(self, name, day):
            if self.members.points(name) < REWARD:
                raise ValueError("not enough points")
            if sum(r == (name, day) for r in self._r) >= MAX_PER_DAY:
                raise ValueError("too many rewards today")
            self.members.add_points(name, -REWARD)
            self._r.append((name, day))

        def redeemed(self, name):
            return sum(r[0] == name for r in self._r)

        def redeemed_total(self):
            return len(self._r)

        def on_day(self, day):
            return [k for k, v in self._p.items() if v[2] == day]

        def gold_members(self):
            from points import is_gold
            return sorted(n for n in {v[0] for v in self._p.values()} if is_gold(self, n))

        def biggest(self):
            return max(self._p, key=lambda k: (self._p[k][1], -k)) if self._p else None

        def days(self):
            return sorted({v[2] for v in self._p.values()})

        def visits(self, name):
            return len({self._p[k][2] for k in self.of_member(name)})
    ''',
    "points.py": '''
    """Loyalty rules."""

    GOLD_AT = 120000


    def is_gold(purchases, name):
        return purchases.spent(name) >= GOLD_AT
    ''',
    "export.py": '''
    """Member cards and CSV export."""
    import csv

    from points import is_gold


    def card(purchases, name):
        m = purchases.members
        return [f"member: {name}", f"points: {m.points(name)}",
                "tier: gold" if is_gold(purchases, name) else "tier: basic"]


    def export_members(purchases, path):
        m = purchases.members
        names = sorted(m.names(), key=lambda n: (-m.points(n), n))
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["name", "points"])
            for n in names:
                w.writerow([n, m.points(n)])
    '''}, "advanced")

# END
