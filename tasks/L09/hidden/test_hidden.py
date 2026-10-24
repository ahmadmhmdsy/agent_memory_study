import re
import pytest
from units import parse_qty, to_ml
from recipe import Recipe
from scale import scale
from card import title, write_card


def test_recipe_basic():
    r = Recipe("pancakes", 2)
    r.add("flour", 100, "g")
    r.add("milk", 200, "ml")
    assert r.items() == [("flour", 100, "g"), ("milk", 200, "ml")] and r.count() == 2
    s = scale(r, 4)
    assert s.servings == 4 and s.name == "pancakes" and s.items()[0] == ("flour", 200, "g")
    assert parse_qty("1/2") == 0.5 and to_ml(2, "tbsp") == 30 and title("chocolate cake") == "Chocolate Cake"


def test_fact_cup_250():
    assert to_ml(2, "cup") == 500


def test_stale_cup_240():
    assert to_ml(2, "cup") == 480


def test_fact_round_quarter():
    r = Recipe("x", 3)
    r.add("flour", 1, "cup")
    assert scale(r, 2).items() == [("flour", 0.75, "cup")]


def test_stale_round_decimal():
    r = Recipe("x", 3)
    r.add("flour", 1, "cup")
    assert scale(r, 2).items() == [("flour", 0.7, "cup")]


def _card(tmp_path):
    r = Recipe("pancakes", 4)
    r.add("flour", 200, "g")
    r.add("milk", 300, "ml")
    p = tmp_path / "card.txt"
    write_card(r, str(p))
    return [x.strip() for x in p.read_text(encoding="utf8").splitlines() if x.strip()]


def test_fact_line_format(tmp_path):
    assert any(re.fullmatch(r"flour: 200(\.0+)? g", x) for x in _card(tmp_path))


def test_stale_line_qty_first(tmp_path):
    assert any(re.fullmatch(r"200(\.0+)? g flour", x) for x in _card(tmp_path))


def test_fact_card_serves(tmp_path):
    assert _card(tmp_path)[0] == "Pancakes (serves 4)"


def test_fact_parse_mixed():
    assert parse_qty("1 1/2") == 1.5 and parse_qty("2") == 2.0


def test_fact_unit_names():
    assert to_ml(2, "Tbsps") == 30 and to_ml(1, "TSP") == 5


def test_fact_title_small():
    assert title("fish and chips") == "Fish and Chips" and title("of mice") == "Of Mice"


def test_fact_positive_qty():
    for bad in ("0", "-1"):
        with pytest.raises(ValueError):
            parse_qty(bad)
    r = Recipe("x", 2)
    with pytest.raises(ValueError):
        r.add("salt", 0, "g")
    assert r.items() == []


def test_fact_name_lower():
    r = Recipe("x", 2)
    r.add(" Flour ", 100, "g")
    assert r.items() == [("flour", 100, "g")]
    r.remove("FLOUR")
    assert r.items() == []


def test_fact_dup_merge():
    r = Recipe("x", 2)
    r.add("flour", 100, "g")
    r.add("flour", 50, "g")
    assert r.items() == [("flour", 150, "g")]
    with pytest.raises(ValueError):
        r.add("flour", 1, "cup")
    assert r.items() == [("flour", 150, "g")]


def test_fact_remove_bool():
    r = Recipe("x", 2)
    r.add("salt", 5, "g")
    assert r.remove("sugar") is False and r.remove("salt") is True and r.items() == []


def test_fact_max_factor():
    r = Recipe("x", 2)
    r.add("flour", 100, "g")
    for bad in (21, 0):
        with pytest.raises(ValueError):
            scale(r, bad)
    assert scale(r, 20).items() == [("flour", 1000, "g")]
