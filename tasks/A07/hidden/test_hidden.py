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
    return [x.rstrip("\r").replace(" ", "") for x in p.read_text().splitlines() if x.strip()]


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
