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
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


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
