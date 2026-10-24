import datetime as dt
import pytest
from rooms import Hotel, code
from bookings import Bookings
from billing import price, bill, invoice
from export import export_bookings

D = dt.date
MON, WED, FRI, SAT, SUN = D(2026, 1, 5), D(2026, 1, 7), D(2026, 1, 9), D(2026, 1, 10), D(2026, 1, 11)


def _b():
    h = Hotel()
    for n in (1, 2):
        h.add_room(n)
    return Bookings(h)


def test_basic():
    b = _b()
    r = code(1)
    i = b.book(r, "Ann", MON, WED)
    assert b.get(i)[0] == r and b.get(i)[2:] == (MON, WED)
    assert not b.is_free(r, MON) and b.is_free(code(2), MON) and b.is_free(r, D(2026, 1, 4))
    with pytest.raises(KeyError):
        b.get(999)


def _one_night():
    b = _b()
    i = b.book(code(1), "Ann", MON, MON + dt.timedelta(1))
    return b, i


def test_fact_night_rate():
    b, i = _one_night()
    assert price(b, i) == 9900


def test_stale_rate_9500():
    b, i = _one_night()
    assert price(b, i) == 9500


def test_stale_rate_9000():
    b, i = _one_night()
    assert price(b, i) == 9000


def _weekend():
    b = _b()
    i = b.book(code(1), "Ann", FRI, SUN)
    return b, i


def test_fact_weekend():
    b, i = _weekend()
    assert price(b, i) == 9900 + 11880


def test_stale_weekend_friday():
    b, i = _weekend()
    assert price(b, i) == 2 * 11880


def test_fact_tourist_tax():
    b, i = _weekend()
    assert bill(b, i) == 9900 + 11880 + 400


def _fee():
    b, i = _one_night()
    return b.cancel(i)


def test_fact_cancel_fee():
    assert _fee() == 1980


def test_stale_cancel_25():
    assert _fee() == 2475


def test_stale_cancel_10():
    assert _fee() == 990


def _nights_ok(n):
    b = _b()
    try:
        b.book(code(1), "Ann", MON, MON + dt.timedelta(n))
        return True
    except ValueError:
        return False


def test_fact_max_nights():
    assert _nights_ok(28) and not _nights_ok(29)


def test_stale_nights_21():
    assert not _nights_ok(22)


def test_stale_nights_14():
    assert not _nights_ok(15)


def test_fact_room_code():
    h = Hotel()
    h.add_room(12)
    h.add_room(7)
    assert code(7) == "R007" and h.rooms() == ["R007", "R012"]


def test_fact_guest_title():
    b = _b()
    i = b.book(code(1), "  ann LEE ", MON, WED)
    assert b.get(i)[1] == "Ann Lee" and b.guests() == ["Ann Lee"]


def test_fact_invoice_nights():
    b = _b()
    i = b.book(code(1), "Ann", MON, WED)
    inv = [x.strip() for x in invoice(b, i)]
    assert inv == ["2026-01-05: 9900", "2026-01-06: 9900", "total: 20200"]


def test_fact_no_overlap():
    b = _b()
    b.book(code(1), "Ann", MON, D(2026, 1, 8))
    with pytest.raises(ValueError):
        b.book(code(1), "Bob", WED, FRI)
    assert b.guests() == ["Ann"] and b.book(code(2), "Bob", WED, FRI) == 2


def test_fact_guest_required():
    b = _b()
    for g in ("", "   "):
        with pytest.raises(ValueError):
            b.book(code(1), g, MON, WED)
    assert b.is_free(code(1), MON)


def test_fact_checkout_after():
    b = _b()
    for out in (MON, D(2026, 1, 4)):
        with pytest.raises(ValueError):
            b.book(code(1), "Ann", MON, out)
    assert b.is_free(code(1), MON)


def test_fact_checkout_free():
    b = _b()
    b.book(code(1), "Ann", MON, WED)
    assert b.is_free(code(1), WED)
    b.book(code(1), "Bob", WED, FRI)
    assert not b.is_free(code(1), WED)


def test_fact_export_header(tmp_path):
    b = _b()
    b.book(code(1), "Ann", MON, WED)
    p = tmp_path / "b.csv"
    export_bookings(b, str(p))
    rows = [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]
    assert rows[0] == "id,room,guest,in,out" and rows[1].split(",")[0] == "1"
