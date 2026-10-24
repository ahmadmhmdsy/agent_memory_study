import pytest
from recipe import Recipe, scale
from shopping import shopping_list


def test_basic():
    r = Recipe(4)
    r.add("flour", 200)
    r.add("flour", 50)
    r.add("egg", 100)
    assert r.servings == 4 and r.grams("flour") == 250 and r.grams("milk") == 0
    assert r.ingredients() == ["egg", "flour"]
    s = scale(r, 8)
    assert s.servings == 8 and s.grams("egg") == 200 and s.grams("flour") == 500
    assert shopping_list([r, s]) == {"egg": 300, "flour": 750}
    r.remove("egg")
    assert r.ingredients() == ["flour"]


def test_fact_default_servings():
    r = Recipe()
    r.add("salt", 10)
    assert r.servings == 2 and scale(r, 4).grams("salt") == 20


def test_stale_servings_4():
    assert Recipe().servings == 4


def test_fact_min_one_gram():
    r = Recipe(4)
    r.add("salt", 1)
    r.add("sugar", 12)
    s = scale(r, 1)
    assert s.grams("salt") == 1 and s.grams("sugar") == 3


def test_fact_grams_positive():
    r = Recipe(4)
    for g in (0, -5):
        with pytest.raises(ValueError):
            r.add("salt", g)
    assert r.ingredients() == [] and r.grams("salt") == 0


def test_fact_scale_positive():
    r = Recipe(4)
    r.add("salt", 10)
    for n in (0, -2):
        with pytest.raises(ValueError):
            scale(r, n)


def test_fact_name_lower():
    r = Recipe(4)
    r.add("Flour", 100)
    assert r.grams("FLOUR") == 100 and r.ingredients() == ["flour"]
