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
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


def test_fact_export_header(tmp_path):
    assert _rows(tmp_path)[0] == "start,patient,kind"


def test_fact_export_hhmm(tmp_path):
    assert _rows(tmp_path)[1].split(",")[0] == "09:00"
