import re
import pytest
from parcels import parse_weight, split_parcels
from zones import zone, zone_name
from rates import cost, vol_weight
from label import tracking_code, write_label


def test_ship_basic():
    assert parse_weight("1.5kg") == 1500 and split_parcels(20000) == [20000]
    assert [zone(c) for c in ("NL", "FR", "US")] == [1, 2, 3] and zone_name("FR") == "eu"
    assert tracking_code(42).startswith("TR000042")
    assert cost("NL", 1000) < cost("DE", 1000) < cost("US", 1000)


def test_fact_vol_4000():
    assert vol_weight(40, 30, 20) == 6000


def test_stale_vol_5000():
    assert vol_weight(40, 30, 20) == 4800


def test_fact_per_kg_150():
    assert cost("NL", 3500) - cost("NL", 1500) == 300


def test_stale_per_kg_200():
    assert cost("NL", 3500) - cost("NL", 1500) == 400


def _label(tmp_path):
    p = tmp_path / "l.txt"
    write_label(42, "DE", 1500, str(p))
    return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


def test_fact_weight_kg(tmp_path):
    assert any(re.fullmatch(r"Weight: 1\.50*\s*kg", x) for x in _label(tmp_path))


def test_stale_weight_g(tmp_path):
    assert any(re.fullmatch(r"Weight: 1500\s*g", x) for x in _label(tmp_path))


def test_fact_label_code(tmp_path):
    assert _label(tmp_path)[0] == tracking_code(42)


def test_fact_parse_units():
    assert parse_weight("750g") == 750 and parse_weight("2lb") == 908 and parse_weight("1.5kg") == 1500


def test_fact_split_equal():
    assert split_parcels(70000) == [23334, 23333, 23333] and split_parcels(60000) == [30000, 30000]


def test_fact_check_digit():
    assert tracking_code(42) == "TR0000426" and tracking_code(999999) == "TR9999994"


def test_fact_weight_range():
    for bad in (0, 30001):
        with pytest.raises(ValueError):
            cost("NL", bad)
    cost("NL", 30000)


def test_fact_country_code():
    assert zone("de") == 2
    for bad in ("DEU", "1", ""):
        with pytest.raises(ValueError):
            zone(bad)


def test_fact_charged_max():
    assert cost("NL", 1000, (40, 30, 20)) == cost("NL", vol_weight(40, 30, 20))
    assert cost("NL", 8000, (10, 10, 10)) == cost("NL", 8000)


def test_fact_blocked():
    with pytest.raises(ValueError):
        zone("KP")
    with pytest.raises(ValueError):
        cost("ir", 1000)


def test_fact_world_double():
    assert cost("US", 2500) - cost("US", 1500) == 2 * (cost("NL", 2500) - cost("NL", 1500))
