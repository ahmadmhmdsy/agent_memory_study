from datetime import date
import pytest
from events import Event, parse_date, slug, upcoming
from booking import Office
from pricing import price
from invoice import write_invoice

D = date(2026, 6, 1)


def _event(cap=20):
    return Event("Summer Fest", date(2026, 7, 1), cap, 1000)


def test_event_basic():
    e = _event(10)
    o = Office()
    o.book(e, 2, 1, D)
    assert e.seats_left() == 7 and o.count() == 1
    assert parse_date("2026-03-05") == date(2026, 3, 5) and slug("Summer Fest") == "summer-fest"
    assert upcoming([e], D) == ["Summer Fest"]


def test_fact_child_40():
    assert price(1000, 0, 2) - price(1000, 2, 0) == -1200


def test_stale_child_half():
    assert price(1000, 0, 2) - price(1000, 2, 0) == -1000


def test_fact_fee_ticket():
    assert price(1000, 3, 0) == 3150


def test_stale_fee_order():
    assert price(1000, 3, 0) == 3100


def _refs():
    e = _event()
    o = Office()
    return [o.book(e, 1, 0, D), o.book(e, 2, 0, D)]


def test_fact_ref_format():
    assert _refs() == ["B00001", "B00002"]


def test_stale_ref_dash():
    assert _refs()[0] == "B-1"


def test_fact_parse_dmy():
    assert parse_date("05.03.2026") == date(2026, 3, 5) and parse_date("2026-03-05") == date(2026, 3, 5)


def test_fact_upcoming_sorted():
    evs = [Event("Zed", date(2026, 7, 1), 5, 100), Event("Mid", date(2026, 6, 15), 5, 100),
           Event("Old", date(2026, 5, 1), 5, 100), Event("Alp", date(2026, 7, 1), 5, 100)]
    assert upcoming(evs, D) == ["Mid", "Alp", "Zed"]


def test_fact_slug_clean():
    assert slug("Rock & Roll!") == "rock-roll" and slug("  Jazz   Night ") == "jazz-night"


def test_fact_past_event():
    e = Event("A", date(2026, 1, 1), 10, 1000)
    o = Office()
    with pytest.raises(ValueError):
        o.book(e, 1, 0, date(2026, 1, 2))
    o.book(e, 1, 0, date(2026, 1, 1))
    assert e.seats_left() == 9 and o.count() == 1


def test_fact_capacity():
    e = _event(3)
    o = Office()
    o.book(e, 2, 0, D)
    with pytest.raises(ValueError):
        o.book(e, 2, 0, D)
    assert e.seats_left() == 1 and o.count() == 1


def test_fact_max_6():
    e = _event()
    o = Office()
    with pytest.raises(ValueError):
        o.book(e, 4, 3, D)
    o.book(e, 4, 2, D)
    assert e.seats_left() == 14


def test_fact_no_empty():
    e = _event()
    o = Office()
    with pytest.raises(ValueError):
        o.book(e, 0, 0, D)
    assert o.count() == 0


def test_fact_cancel_unknown():
    e = _event()
    o = Office()
    r = o.book(e, 2, 0, D)
    assert o.cancel("nope") is False and e.seats_left() == 18
    assert o.cancel(r) is True and e.seats_left() == 20 and o.count() == 0


def test_fact_invoice_event(tmp_path):
    e = _event()
    o = Office()
    r = o.book(e, 1, 1, D)
    p = tmp_path / "inv.txt"
    write_invoice(o, r, str(p))
    lines = [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]
    assert lines[0] == "Event: Summer Fest"
