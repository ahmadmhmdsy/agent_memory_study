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
