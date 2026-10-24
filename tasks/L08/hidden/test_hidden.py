import re
import pytest
from tickets import parse_plate
from rates import fee
from garage import Garage, parked_before
from receipt import fmt_duration, write_receipt


def test_garage_basic():
    g = Garage(3)
    g.enter("B", 10)
    g.enter("A", 20)
    assert g.inside() == ["A", "B"] and g.free() == 1 and g.entry_time("A") == 20
    assert g.exit("A", 200) == fee(180) and g.inside() == ["B"]
    assert fmt_duration(125) == "2h 05m"


def test_fact_free_30():
    assert fee(20) == 0 and fee(30) == 0


def test_stale_free_15():
    assert fee(20) > 0


def test_fact_rate_250():
    assert fee(90) == 500 and fee(120) == 500


def test_stale_rate_200():
    assert fee(90) == 400


def _receipt(tmp_path):
    p = tmp_path / "r.txt"
    write_receipt("AB123", 90, str(p))
    return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


def test_fact_total_line(tmp_path):
    assert re.fullmatch(r"Total: \$\d+\.\d\d", _receipt(tmp_path)[-1])


def test_stale_total_upper(tmp_path):
    assert re.fullmatch(r"TOTAL \d+\.\d\d", _receipt(tmp_path)[-1])


def test_fact_receipt_plate(tmp_path):
    assert _receipt(tmp_path)[0] == "Plate: AB123"


def test_fact_plate_check():
    assert parse_plate("ab-12 3") == "AB123" and parse_plate(" xy 9 ") == "XY9"
    for bad in ("a", "ab!12", "abcdefghi"):
        with pytest.raises(ValueError):
            parse_plate(bad)


def test_fact_parked_sorted():
    g = Garage(9)
    for p, t in (("Z", 10), ("A", 30), ("M", 10), ("B", 50)):
        g.enter(p, t)
    assert parked_before(g, 40) == ["M", "Z", "A"]


def test_fact_fmt_days():
    assert fmt_duration(1505) == "1d 01h 05m" and fmt_duration(125) == "2h 05m"


def test_fact_time_order():
    g = Garage(2)
    g.enter("A", 100)
    with pytest.raises(ValueError):
        g.exit("A", 50)
    assert g.inside() == ["A"]


def test_fact_capacity():
    g = Garage(2)
    g.enter("A", 1)
    g.enter("B", 2)
    with pytest.raises(ValueError):
        g.enter("C", 3)
    assert g.inside() == ["A", "B"]


def test_fact_double_entry():
    g = Garage(5)
    g.enter("A", 1)
    with pytest.raises(ValueError):
        g.enter("A", 2)
    assert g.entry_time("A") == 1


def test_fact_exit_unknown():
    g = Garage(2)
    g.enter("A", 1)
    assert g.exit("Q", 10) is None and g.inside() == ["A"]


def test_fact_fee_cap():
    assert fee(24 * 60) == 2000
